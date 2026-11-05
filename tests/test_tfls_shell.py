"""Behavioral regressions for study intake and configured TFL delivery."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from docx import Document
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'tfls-shell' / 'scripts'


class TflsShellTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def call(self, *extra, config=None, script='recommend_then_generate.py'):
        args = [sys.executable, '-X', 'utf8', str(SCRIPTS/script), '--json']
        if script != 'validate_outputs.py':
            args += ['--no-figures', '--output-dir', str(self.base/'out')]
        if config is not None:
            path = self.base/'config.json'
            path.write_text(json.dumps(config, ensure_ascii=False), encoding='utf-8')
            args += ['--config', str(path)]
        env = dict(os.environ)
        env.pop('PYTHONPATH', None)
        result = subprocess.run([*args, *extra], cwd=self.base, env=env, capture_output=True,
            text=True, encoding='utf-8', timeout=120)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def config(self, **delivery):
        return {'study': {'phase':'phase-ii', 'area':'oncology', 'endpoints':['PFS'],
            'populations':['ITT'], 'groups':['Active','Placebo'], 'timepoints':['Baseline'],
            'shell_ids':['T14.1.1'], 'shell_overrides':{'T14.1.1':{'population':'ITT'}}},
            'delivery': delivery}

    def test_missing_file_and_empty_material_never_publish(self):
        for args in [[], ['--input-file', str(self.base/'missing.txt')], ['--text',' ']]:
            code, payload = self.call(*args)
            self.assertEqual(code, 2)
            self.assertEqual(payload['status'], 'needs_information')
            self.assertTrue(payload['ambiguity_state']['needs_user_confirmation'])
            self.assertFalse((self.base/'out').exists())

    def test_pfs_and_chinese_signals_include_efficacy(self):
        for text in ['Phase II oncology PFS safety population', 'II期肿瘤研究，主要终点为无进展生存期，安全性集。']:
            code, payload = self.call('--text', text, '--mode', 'recommend', '--generic-template')
            self.assertEqual(code, 0)
            self.assertIn('14.2', payload['recommendation_summary']['sections'])
            self.assertEqual(payload['interpreted_context']['study_phase'], 'Phase II')
            self.assertFalse((self.base/'out').exists())

    def test_study_missing_groups_and_timepoints_stops(self):
        code, payload = self.call('--text', 'Phase II oncology primary endpoint PFS safety population')
        self.assertEqual(code, 2)
        self.assertIn('groups', payload['required_information'])
        self.assertIn('timepoints', payload['required_information'])

    def test_configured_three_outputs_no_duplicate_titles_and_no_overwrite(self):
        cfg = self.config(document_version='1.2', paper='a4', orientation='portrait', font='Arial',
            protocol='PROTO-42', sponsor='Sponsor X', study_title='Study X',
            group_labels=['Arm A','Arm B','Arm C'])
        cfg['study']['groups'] = ['Treatment A','Treatment B','Treatment C']
        code, payload = self.call(config=cfg)
        self.assertEqual(code, 0, payload)
        self.assertTrue(payload['validation_results']['passed'])
        self.assertEqual(payload['generator_version'], '2.1.0')
        self.assertEqual(payload['document_version'], '1.2')
        artifacts = {a['kind']: Path(a['path']) for a in payload['generation_results']['artifacts']}
        doc = Document(artifacts['docx'])
        headings = [p.text for p in doc.paragraphs if p.style.name == 'Heading 4']
        self.assertEqual(len(headings), 1)
        self.assertFalse(any(p.text == 'Table 14.1.1' for p in doc.paragraphs))
        self.assertIn('PROTO-42', doc.sections[0].header.paragraphs[0].text)
        self.assertTrue(doc._element.xpath('.//w:fldChar'))
        headers = [c.text for c in doc.tables[0].rows[0].cells]
        self.assertTrue(all(any(g in h for h in headers) for g in ['Arm A','Arm B','Arm C']))
        self.assertTrue(any('Overall' in h for h in headers))
        self.assertTrue(all(len(row.cells)==len(headers) for row in doc.tables[0].rows))
        self.assertTrue(all('v1.2' in path.name for path in artifacts.values()))
        original = artifacts['docx'].read_bytes()
        code, rejected = self.call(config=cfg)
        self.assertEqual(code, 2)
        self.assertEqual(rejected['status'], 'error')
        self.assertEqual(artifacts['docx'].read_bytes(), original)
        manifest = payload['generation_results']['contract_path']
        code, checked = self.call('--contract', manifest, script='validate_outputs.py')
        self.assertEqual(code, 0, checked)
        wb = load_workbook(artifacts['xlsx'])
        wb['TOC_Master'].cell(2,1).value = 'TAMPERED'
        wb.save(artifacts['xlsx'])
        wb.close()
        code, checked = self.call('--contract', manifest, script='validate_outputs.py')
        self.assertEqual(code, 1)
        self.assertFalse(checked['passed'])

    def test_single_arm_has_no_second_treatment_column(self):
        cfg = self.config(group_labels=['Single arm'])
        cfg['study']['groups'] = ['Single arm']
        code, payload = self.call('--type','all', config=cfg)
        self.assertEqual(code, 0, payload)
        doc = Document(payload['generation_results']['artifacts'][0]['path'])
        headers = [c.text for c in doc.tables[0].rows[0].cells]
        self.assertEqual(sum('Single arm' in h for h in headers), 1)
        self.assertFalse(any('Group 2' in h or h=='...' for h in headers))

    def test_localization_is_complete_before_publication(self):
        cfg = self.config(language='zh', font='SimSun')
        code, payload = self.call('--type','all', config=cfg)
        self.assertEqual(code, 2)
        self.assertEqual(payload['status'], 'needs_localization')
        self.assertFalse((self.base/'out').exists())
        # Synthetic translations test exact mapping application, not linguistic quality.
        cfg['translations'] = {s:f'译文第{i}项' for i,s in enumerate(payload['localization_strings'])}
        code, payload = self.call('--type','all', config=cfg)
        self.assertEqual(code, 0, payload)
        self.assertTrue(payload['validation_results']['passed'])
        doc = Document(payload['generation_results']['artifacts'][0]['path'])
        self.assertTrue(all(p.text.startswith('译文') for p in doc.paragraphs if p.style.name=='Heading 4'))
        self.assertTrue(doc._element.xpath('.//w:fldChar'))

    def test_bilingual_workbook_keeps_ids_and_translates_labels(self):
        cfg = self.config(language='bilingual')
        code, payload = self.call('--type','xlsx', config=cfg)
        self.assertEqual(code, 2)
        cfg['translations'] = {s:f'译文第{i}项' for i,s in enumerate(payload['localization_strings'])}
        code, payload = self.call('--type','xlsx', config=cfg)
        self.assertEqual(code, 0, payload)
        wb = load_workbook(payload['generation_results']['artifacts'][0]['path'])
        self.assertEqual(wb['TOC_Master'].cell(2,1).value, 'T14.1.1')
        self.assertIn('\n译文', wb['TOC_Master'].cell(1,1).value)
        wb.close()

    def test_unsupported_template_and_invalid_configuration_are_explicit(self):
        cfg = self.config(sponsor_template='sponsor.docx')
        code, payload = self.call(config=cfg)
        self.assertEqual(code, 2)
        self.assertIn('sponsor_template_mapping', payload['required_information'])
        cfg = self.config(document_version='../bad')
        code, payload = self.call(config=cfg)
        self.assertEqual(code, 2)
        self.assertEqual(payload['status'], 'error')

    def test_full_generic_catalog_uses_delivery_contract(self):
        code, payload = self.call('--generic-template','--type','all', script='generate_project_aligned_outputs.py')
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload['recommendation_summary']['total_items'], 206)
        self.assertTrue(payload['validation_results']['passed'])


if __name__ == '__main__':
    unittest.main()
