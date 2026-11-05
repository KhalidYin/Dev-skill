"""Study intake and configurable delivery around the upstream Product generators."""

from copy import copy
import json
from pathlib import Path
import re
import tempfile

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.shared import Inches
from docx.oxml.ns import qn
from openpyxl import load_workbook

from tflshell import __version__
from tflshell.data.definitions import build_catalog
from tflshell.models.catalog import TFLCatalog
from tflshell.recommend import InputSource, RecommendRequest, recommend_shells
from runtime.wrappers.docx_wrapper import generate as docx_generate
from runtime.wrappers.xlsx_wrapper import generate as xlsx_generate
from runtime.wrappers.sop_wrapper import generate as sop_generate
from alignment_contracts import _expected_docx_items


def add_arguments(parser):
    parser.add_argument('--config', help='UTF-8 JSON: study, delivery and translations')
    parser.add_argument('--mode', choices=['recommend', 'generate'], default='generate')
    parser.add_argument('--generic-template', action='store_true')
    parser.add_argument('--document-version')


def load_settings(args):
    raw = json.loads(Path(args.config).read_text(encoding='utf-8')) if args.config else {}
    if not isinstance(raw, dict) or not isinstance(raw.get('study', {}), dict) or not isinstance(raw.get('delivery', {}), dict):
        raise ValueError('Configuration, study and delivery must be objects')
    unknown = set(raw) - {'study', 'delivery', 'translations'}
    if unknown:
        raise ValueError(f'Unknown configuration keys: {sorted(unknown)}')
    settings = {'study': raw.get('study', {}), 'delivery': {
        'document_version': '0.1-draft', 'language': 'en', 'paper': 'letter',
        'orientation': 'landscape', 'margin_inches': 0.75, 'font': 'Times New Roman',
        'presentation_profile': args.presentation_profile,
        **raw.get('delivery', {}),
    }, 'translations': raw.get('translations', {})}
    d = settings['delivery']
    unknown = set(d) - {'document_version', 'language', 'paper', 'orientation', 'margin_inches',
        'font', 'presentation_profile', 'sponsor', 'protocol', 'study_title', 'group_labels',
        'header_labels', 'sponsor_template'}
    if unknown:
        raise ValueError(f'Unsupported delivery settings: {sorted(unknown)}')
    if args.document_version:
        d['document_version'] = args.document_version
    for key in ('sponsor', 'protocol'):
        if getattr(args, key, None):
            d[key] = getattr(args, key)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}', d['document_version']):
        raise ValueError('document_version must be a safe filename token (1-64 characters)')
    if d['language'] not in ('en', 'zh', 'bilingual'):
        raise ValueError('language must be en, zh or bilingual')
    if d['paper'] not in ('letter', 'a4') or d['orientation'] not in ('landscape', 'portrait'):
        raise ValueError('Unsupported paper or orientation')
    if not isinstance(d['margin_inches'], (int, float)) or not 0.2 <= d['margin_inches'] <= 2:
        raise ValueError('margin_inches must be between 0.2 and 2')
    if d['presentation_profile'] not in ('csr_standard', 'compact_review', 'authoring_shell'):
        raise ValueError('Unsupported presentation_profile')
    if not isinstance(d['font'], str) or not d['font'].strip():
        raise ValueError('font must be a nonempty string')
    if not isinstance(d.get('header_labels', {}), dict) or not all(
        isinstance(k,str) and isinstance(v,str) and k and v for k,v in d.get('header_labels', {}).items()
    ):
        raise ValueError('header_labels must map nonempty strings to nonempty strings')
    groups = d.get('group_labels')
    if groups is not None and (not isinstance(groups, list) or not groups or
        not all(isinstance(v, str) and v.strip() for v in groups) or len(set(groups)) != len(groups)):
        raise ValueError('group_labels must be a nonempty list of unique names')
    if not isinstance(settings['translations'], dict) or not all(
        isinstance(k, str) and isinstance(v, str) and v.strip()
        for k, v in settings['translations'].items()
    ):
        raise ValueError('translations must map exact source strings to nonempty translated strings')
    return settings


def intake(args, settings, full=False):
    sources = [InputSource(content_text=text) for text in getattr(args, 'text', []) or []]
    sources += [InputSource(file_path=path) for path in getattr(args, 'input_file', []) or []]
    study = settings['study']
    allowed = {'phase', 'area', 'endpoints', 'populations', 'groups', 'timepoints', 'shell_ids', 'sections', 'shell_overrides'}
    if set(study) - allowed:
        raise ValueError(f'Unsupported study settings: {sorted(set(study)-allowed)}')
    for key in ('endpoints', 'populations', 'groups', 'timepoints', 'shell_ids', 'sections'):
        if key in study and (not isinstance(study[key], list) or not all(isinstance(x, str) and x.strip() for x in study[key])):
            raise ValueError(f'study.{key} must be an array of nonempty strings')
    generic = args.generic_template
    # Material interpretation belongs to the agent. These common bilingual signals
    # prevent known heuristic omissions; the explicit study fields remain authoritative.
    content = '\n'.join(s.content_text for s in sources)
    for source in sources:
        if source.file_path and Path(source.file_path).is_file():
            content += '\n' + Path(source.file_path).read_text(encoding='utf-8')
    normalized = content
    for cn, en in {'非肿瘤':'non oncology', '肿瘤':'oncology', 'III期':'phase iii',
        'II期':'phase ii', 'I期':'phase i', '无进展生存期':'primary endpoint PFS',
        '总生存期':'primary endpoint OS', '安全性集':'safety population',
        '全分析集':'full analysis set', '主要终点':'primary endpoint'}.items():
        normalized = normalized.replace(cn, ' ' + en + ' ')
    explicit = ' '.join(study.get('endpoints', []) + study.get('populations', []))
    if re.search(r'\b(PFS|OS|ORR|DCR|BOR)\b', normalized + ' ' + explicit, re.I):
        explicit += ' primary endpoint efficacy'
    # Keep unreadable sources visible rather than replacing them with synthetic material.
    if normalized.strip() or explicit.strip():
        sources.append(InputSource(content_text=normalized + ' ' + explicit))
    phase = study.get('phase', getattr(args, 'phase', 'unknown'))
    area = study.get('area', getattr(args, 'area', 'unknown'))
    if phase not in ('phase-i', 'phase-ii', 'phase-iii', 'mixed', 'unknown'):
        raise ValueError('Unsupported study.phase')
    if area not in ('oncology', 'non-oncology', 'all', 'unknown'):
        raise ValueError('Unsupported study.area')
    r = recommend_shells(RecommendRequest(
        sources=sources or [InputSource()], study_phase_hint=phase, therapeutic_area_hint=area,
        section_scope=study.get('sections', getattr(args, 'section', []) or []),
        include_figures=not args.no_figures, include_listings=not getattr(args, 'no_listings', False),
    ))
    missing = []
    if not generic:
        missing.extend(r.ambiguity_state['missing_fields'])
        if not (study.get('endpoints') or r.interpreted_context['primary_endpoints']):
            missing.append('endpoints')
        if not (study.get('populations') or r.interpreted_context['analysis_populations']):
            missing.append('populations')
        for key in ('groups', 'timepoints'):
            if not study.get(key):
                missing.append(key)
        if not any(s.get('usable') for s in r.ingestion_state['recognized_sources']) and not study:
            missing.append('usable_study_material')
    if r.ingestion_state['unreadable_sources'] and (getattr(args, 'input_file', None) or getattr(args, 'text', None)):
        missing.append('unreadable_sources')
    if r.ambiguity_state['conflicts']:
        missing.append('conflicts')
    if settings['delivery'].get('sponsor_template'):
        missing.append('sponsor_template_mapping')
    if study.get('groups') and not settings['delivery'].get('group_labels'):
        settings['delivery']['group_labels'] = study['groups']
    if study.get('groups') and len(settings['delivery'].get('group_labels', [])) != len(study['groups']):
        missing.append('group_label_count_conflict')
    if not args.no_figures and settings['delivery']['language'] != 'en':
        missing.append('localized_figure_assets_or_no_figures')
    r.ambiguity_state['missing_fields'] = sorted(set(missing))
    r.ambiguity_state['needs_user_confirmation'] = bool(missing)
    catalog = build_catalog()
    ids = study.get('shell_ids')
    if ids:
        unknown = [key for key in ids if catalog.get(key) is None]
        if unknown or len(set(ids)) != len(ids):
            raise ValueError(f'Unknown or duplicate shell IDs: {unknown}')
        items = [catalog.get(key) for key in ids]
    elif full and generic:
        items = catalog.all()
    else:
        items = [catalog.get(key) for key in r.recommendation_state['base_package']['shell_ids']]
    if study.get('sections') and set(study['sections']) - {'14.1','14.2','14.3','14.4','16.2'}:
        raise ValueError('Unknown study.sections')
    if not items:
        missing.append('empty_selection')
    overrides = study.get('shell_overrides', {})
    if not isinstance(overrides, dict):
        raise ValueError('shell_overrides must be an object keyed by selected shell ID')
    selected = {item.id: item for item in items}
    for key, values in overrides.items():
        if key not in selected or not isinstance(values, dict) or set(values)-{'title','population','table_notes'}:
            raise ValueError(f'Unsupported override for {key}')
        for field, value in values.items():
            if not isinstance(value,str) or not value.strip():
                raise ValueError(f'Empty override {key}.{field}')
            setattr(selected[key], field, value)
    r.ambiguity_state['missing_fields'] = sorted(set(missing))
    r.ambiguity_state['needs_user_confirmation'] = bool(missing)
    return r, TFLCatalog(items), sorted(set(missing))


def configure_groups(catalog, groups):
    """Change only generic treatment columns, preserving analytic columns and row alignment."""
    if not groups:
        return
    for item in catalog.all():
        headers = item.placeholder_columns
        positions = [i for i, h in enumerate(headers) if re.match(r'Group [12](?:\n|$)', h)]
        if not positions:
            continue
        first = positions[0]
        removed = set(positions)
        # Only the expansion marker following generic treatment columns is structural.
        if max(positions)+1 < len(headers) and headers[max(positions)+1] == '...':
            removed.add(max(positions)+1)
        suffix = headers[first].split('\n', 1)[1] if '\n' in headers[first] else ''
        new_headers = [g + ('\n'+suffix if suffix else '') for g in groups]
        indexes = []
        final = []
        for i, h in enumerate(headers):
            if i == first:
                final.extend(new_headers)
                indexes.extend([first] * len(groups))
            if i not in removed:
                final.append(h)
                indexes.append(i)
        rows = []
        for row in item.shell_data_rows_rich:
            cells = [row['label']] + row['values']
            row['values'] = [cells[i] if i < len(cells) else item.placeholder_example for i in indexes[1:]]
            rows.append(row)
        item.placeholder_columns = final
        item.shell_rows = rows


def _paragraphs(doc, include_tables=True):
    yield from doc.paragraphs
    for table in doc.tables if include_tables else []:
        for row in table.rows:
            for cell in row.cells:
                yield from cell.paragraphs
    for section in doc.sections:
        yield from section.header.paragraphs
        yield from section.footer.paragraphs


def _remove_duplicate_titles(doc, items):
    # Product emits Heading 4 followed by the same ID/title in the metadata block.
    # Delete only that exact pair within its shell block; preserve Heading 4 and TOC.
    lookup = {f'{item.display_label}  {item.title}': item for item in items}
    current = None
    for p in list(doc.paragraphs):
        if p.style.name == 'Heading 4':
            current = lookup.get(p.text)
        elif current and p.text in (current.display_label, current.title):
            p._element.getparent().remove(p._element)


def _layout(d):
    width, height = (8.27, 11.69) if d['paper'] == 'a4' else (8.5, 11)
    return (height, width) if d['orientation'] == 'landscape' else (width, height)


def _replace(text, d):
    text = text.replace(__version__, d['document_version'])
    text = text.replace('[Protocol Number]', d.get('protocol') or '[Protocol Number]')
    text = text.replace('[Sponsor Name]', d.get('sponsor') or '[Sponsor Name]')
    text = text.replace('[Study Title / Compound Name]', d.get('study_title') or '[Study Title / Compound Name]')
    for old, new in d.get('header_labels', {}).items():
        text = text.replace(old, new)
    groups = d.get('group_labels', [])
    for index, group in enumerate(groups[:2], 1):
        text = text.replace(f'Group {index}', group)
    if len(groups) == 1:
        # Single-arm tables retain an explicit unused column only when no mapping
        # exists; require a structural choice before publishing instead of guessing.
        text = text.replace('Group 2', '[Not applicable]')
    return text


def _localize(text, settings, missing):
    if settings['delivery']['language'] == 'en' or not re.search('[A-Za-z]{2}', text) or re.fullmatch(r'[\sXx\d.,%()\[\]/+−–-]+', text):
        return text
    translated = settings['translations'].get(text)
    if translated is None:
        missing.add(text)
        return text
    return translated if settings['delivery']['language'] == 'zh' else text + '\n' + translated


def customize(path, kind, catalog, settings, missing):
    d = settings['delivery']
    if kind == 'xlsx':
        wb = load_workbook(path)
        for sheet in wb:
            for row in sheet:
                for cell in row:
                    if isinstance(cell.value, str):
                        # Stable identifiers, not language-dependent display text.
                        value = _replace(cell.value, d)
                        if not re.fullmatch(r'[TFL]?\d+(?:\.\d+)+', value):
                            value = _localize(value, settings, missing)
                        cell.value = value
                        font = copy(cell.font)
                        font.name = d['font']
                        cell.font = font
                        if value.startswith(('=', '+', '-', '@')):
                            cell.data_type = 's'
            sheet.page_setup.paperSize = '9' if d['paper'] == 'a4' else '1'
            sheet.page_setup.orientation = d['orientation']
            for edge in ('top', 'bottom', 'left', 'right'):
                setattr(sheet.page_margins, edge, d['margin_inches'])
        wb.save(path)
        wb.close()
        return
    doc = Document(path)
    if kind == 'docx':
        _remove_duplicate_titles(doc, catalog.all())
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                source = _replace(cell.text, d)
                # Product may insert visual wrapping in a header. Translate the
                # whole cell using normalized whitespace, not fragmented runs.
                if d['language'] != 'en':
                    source = ' '.join(source.split())
                new = _localize(source, settings, missing)
                if new != cell.text:
                    cell.text = new
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.font.name = d['font']
                        run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), d['font'])
    for p in _paragraphs(doc, include_tables=False):
        if p._element.xpath('.//w:fldChar | .//w:fldSimple'):
            # Translate around dynamic page/TOC fields without moving field nodes.
            for run in p.runs:
                if run.text:
                    run.text = _localize(_replace(run.text, d), settings, missing)
                run.font.name = d['font']
                run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), d['font'])
            continue
        old = p.text
        new = _localize(_replace(old, d), settings, missing)
        if new != old:
            # Change text runs only; retain page-number and TOC field nodes.
            text_runs = [run for run in p.runs if run.text]
            if text_runs:
                text_runs[0].text = new
                for run in text_runs[1:]:
                    run.text = ''
        for run in p.runs:
            run.font.name = d['font']
            run._element.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), d['font'])
    width, height = _layout(d)
    for section in doc.sections:
        section.page_width, section.page_height = Inches(width), Inches(height)
        section.orientation = WD_ORIENT.LANDSCAPE if d['orientation']=='landscape' else WD_ORIENT.PORTRAIT
        for edge in ('top', 'bottom', 'left', 'right'):
            setattr(section, edge + '_margin', Inches(d['margin_inches']))
    doc.core_properties.version = d['document_version']
    doc.core_properties.title = _localize(_replace(doc.core_properties.title, d), settings, missing)
    doc.save(path)


def expected_contract(catalog, settings):
    missing = set()
    def text(value):
        return _localize(_replace(value, settings['delivery']), settings, missing)
    ordered = _expected_docx_items(catalog)
    from alignment_contracts import XLSX_CATALOG_COLUMNS
    return {
        'settings': settings['delivery'], 'generator_version': __version__,
        'template_contract_version': 'dev-skill-delivery-v2',
        'shell_ids': [item.id for item in catalog.all()],
        'headings': [text(f'{item.display_label}  {item.title}') for item in ordered],
        'populations': [text(f'Analysis Set: {item.population}') for item in ordered],
        'redundant_titles': [text(item.title) for item in ordered],
        'table_headers': [[text(' '.join(c.split())) if settings['delivery']['language'] != 'en' else text(c) for c in item.placeholder_columns] for item in ordered if item.tfl_type.value != 'Figure'],
        'xlsx_headers': [text(c) for c in XLSX_CATALOG_COLUMNS],
        'xlsx_titles': [text(item.title) for item in catalog.all()],
    }


def validate_delivery(artifacts, contract):
    checks = {}
    d = contract['settings']
    width, height = _layout(d)
    for artifact in artifacts:
        path, kind = artifact['path'], artifact['kind']
        if not Path(path).is_file():
            checks[kind] = {'present': False}
            continue
        if kind == 'xlsx':
            wb = load_workbook(path)
            sheet = wb['TOC_Master']
            checks[kind] = {
                'headers_match': [c.value for c in sheet[1]] == contract['xlsx_headers'],
                'ids_match': [row[0] for row in sheet.iter_rows(min_row=2, values_only=True)] == contract['shell_ids'],
                'titles_match': [row[2] for row in sheet.iter_rows(min_row=2, values_only=True)] == contract['xlsx_titles'],
                'font_matches': all(c.font.name == d['font'] for row in sheet for c in row if c.value),
                'print_layout_matches': all(str(s.page_setup.paperSize) == ('9' if d['paper']=='a4' else '1') and s.page_setup.orientation == d['orientation'] for s in wb),
            }
            wb.close()
        else:
            doc = Document(path)
            checks[kind] = {
                'version_matches': doc.core_properties.version == d['document_version'],
                'page_matches': all(abs(s.page_width.inches-width) < .02 and abs(s.page_height.inches-height) < .02 for s in doc.sections),
                'orientation_matches': all(s.orientation == (WD_ORIENT.LANDSCAPE if d['orientation']=='landscape' else WD_ORIENT.PORTRAIT) for s in doc.sections),
                'margins_match': all(abs(getattr(s, e+'_margin').inches-d['margin_inches']) < .01 for s in doc.sections for e in ('top','bottom','left','right')),
            }
            if kind == 'docx':
                headings = [p.text for p in doc.paragraphs if p.style.name == 'Heading 4']
                checks[kind]['headings_match'] = headings == contract['headings']
                checks[kind]['populations_match'] = [p.text for p in doc.paragraphs if p.text in contract['populations']] == contract['populations']
                checks[kind]['titles_not_repeated'] = not any(p.text in contract['redundant_titles'] for p in doc.paragraphs)
                normalize = lambda rows: [[' '.join(c.split()) for c in row] for row in rows]
                checks[kind]['table_headers_match'] = normalize([[c.text for c in t.rows[0].cells] for t in doc.tables]) == normalize(contract['table_headers'])
                if d.get('protocol'):
                    checks[kind]['protocol_in_page_header'] = all(d['protocol'] in s.header.paragraphs[0].text for s in doc.sections)
    return {'passed': bool(checks) and all(all(v.values()) for v in checks.values()), 'checks': checks}


def execute(args, full=False):
    settings = load_settings(args)
    r, catalog, missing = intake(args, settings, full)
    result = r.to_dict()
    result['resolved_settings'] = settings
    result['generator_version'] = __version__
    result['document_version'] = settings['delivery']['document_version']
    result['template_contract_version'] = 'dev-skill-delivery-v2'
    result['recommendation_summary'] = {'shell_ids': [i.id for i in catalog.all()], 'total_items': len(catalog.all()), 'sections': sorted({i.section.number for i in catalog.all()})}
    result['generation_results'] = {'generated': False, 'artifacts': []}
    if missing:
        result.update(status='needs_information', required_information=missing)
        return result
    if args.mode == 'recommend':
        result.update(status='recommended', task_mode='recommend')
        return result
    d = settings['delivery']
    configure_groups(catalog, d.get('group_labels'))
    # No existing artifact is overwritten. All outputs are staged and checked before publication.
    root = Path(args.output_dir).resolve()
    kinds = ['docx', 'xlsx', 'sop'] if args.type == 'all' else [args.type]
    names = {'docx': 'TFL_Shell_Template', 'xlsx': 'TFL_TOC', 'sop': 'TFL_Shell_SOP'}
    targets = {k: root / f"{names[k]}_v{d['document_version']}.{'xlsx' if k=='xlsx' else 'docx'}" for k in kinds}
    manifest_path = root / f"delivery-contract_v{d['document_version']}.json"
    if any(p.exists() for p in [*targets.values(), manifest_path]):
        raise FileExistsError('Output already exists; choose a new directory or document_version')
    missing_text = set()
    with tempfile.TemporaryDirectory(prefix='tfl-stage-') as tmp:
        staged = []
        for kind in kinds:
            path = Path(tmp) / targets[kind].name
            generator = {'docx': docx_generate, 'xlsx': xlsx_generate, 'sop': sop_generate}[kind]
            generator(catalog, str(path), generate_figures=not args.no_figures,
                sponsor=d.get('sponsor'), protocol=d.get('protocol'), presentation_profile=d['presentation_profile'])
            customize(path, kind, catalog, settings, missing_text)
            staged.append({'kind': kind, 'path': str(path), 'file_name': path.name})
        if missing_text:
            result.update(status='needs_localization', localization_strings=sorted(missing_text))
            return result
        contract = expected_contract(catalog, settings)
        validation = validate_delivery(staged, contract)
        result['validation_results'] = validation
        if not validation['passed']:
            result['status'] = 'validation_failed'
            return result
        root.mkdir(parents=True, exist_ok=True)
        published = []
        try:
            for artifact in staged:
                target = targets[artifact['kind']]
                with target.open('xb') as out:
                    published.append(target)
                    out.write(Path(artifact['path']).read_bytes())
                artifact['path'] = str(target)
            with manifest_path.open('x', encoding='utf-8') as out:
                published.append(manifest_path)
                json.dump({'artifacts': staged, 'contract': contract}, out, ensure_ascii=False, indent=2)
        except Exception:
            for path in published:
                path.unlink()
            raise
    result.update(status='generated', task_mode='recommend_then_generate')
    result['generation_results'] = {'generated': True, 'artifacts': staged, 'artifact_count': len(staged), 'contract_path': str(manifest_path)}
    return result


def cli_main(full=False):
    import argparse
    parser = argparse.ArgumentParser(description='Recommend and generate configured TFL shells')
    parser.add_argument('--text', action='append')
    parser.add_argument('--input-file', action='append')
    parser.add_argument('--section', action='append', choices=['14.1','14.2','14.3','14.4','16.2'])
    parser.add_argument('--area', default='unknown')
    parser.add_argument('--phase', default='unknown')
    parser.add_argument('--type', default='all', choices=['docx','xlsx','sop','all'])
    parser.add_argument('--output-dir', default='./tfl-output')
    parser.add_argument('--sponsor')
    parser.add_argument('--protocol')
    parser.add_argument('--presentation-profile', default='csr_standard')
    parser.add_argument('--no-figures', action='store_true')
    parser.add_argument('--no-listings', action='store_true')
    parser.add_argument('--json', action='store_true')
    add_arguments(parser)
    args = parser.parse_args()
    try:
        result = execute(args, full=full)
    except (ValueError, OSError) as exc:
        result = {'status':'error', 'error': str(exc), 'generation_results':{'generated':False}}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] in ('recommended','generated') else 2
