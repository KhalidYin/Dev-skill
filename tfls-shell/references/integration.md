# Dev-skill 整合与运行

## 来源

- 上游：[KhalidYin/TFL-shell](https://github.com/KhalidYin/TFL-shell)。
- 来源目录：`Skill/tfls-shell/`。
- 固定提交：`8d85a4174a40b0b0847875e6411bdf1c278383fa`，Product 版本 `2.1.0`。
- 整合日期：2026-11-05。
- `Skill/tfl-governed-shell-workflow/` 在上游标为历史命名版本，本项目不重复安装该入口。
- 本地修改：兼容已安装 Product；交付 v2 增加输入关卡、独立版本、语言/格式/表头适配、标题去重和配置驱动验证。Product 和原始 catalog 基线沿用上述提交，定制交付契约独立维护。

## Product 依赖

本 Skill 携带规则和参考资产；正式生成依赖上游 Python Product，不随 Skill 复制 Product 源码。
需要 Python 3.10+ 和 Product 的依赖（详见上游 `pyproject.toml`）。
`package_assets/minimal_runtime_requirements.txt` 只是 Office 层最小清单，不是完整 Product 依赖。

本提交的普通 wheel 未包含推荐器使用的 `data/domain_registry.json`，因此使用固定提交的源码可编辑安装，保留该资源：

```powershell
$tflBackend = Join-Path $HOME '.codex/dependencies/tflshell-8d85a417'
git clone https://github.com/KhalidYin/TFL-shell.git $tflBackend
git -C $tflBackend checkout 8d85a4174a40b0b0847875e6411bdf1c278383fa
python -m pip install --user --editable $tflBackend
python -c "from pathlib import Path; import tflshell; assert (Path(tflshell.__file__).parent / 'data/domain_registry.json').is_file(); print(tflshell.__version__)"
```

若目标目录已存在，先核对它的远端与提交，避免覆盖其他版本。虚拟环境中安装时省略 `--user`。
Product 必须安装在执行 Skill 脚本的同一 Python 环境。维护时固定版本与包内契约一起升级。

## 调用

以下命令从 Dev-skill 根目录运行；在其他项目中使用 Skill 目录的绝对路径。

按材料先推荐，补齐研究信息和偏好后按配置生成，完整示例见 [输入和交付契约](request-contract.md)：

```powershell
python -X utf8 tfls-shell/scripts/recommend_then_generate.py --config request.json --mode recommend --no-figures --json
```

`--mode recommend` 不写业务文件；缺少关键研究资料时返回 `needs_information`。通用模板须显式使用 `--generic-template`。
`--input-file` 接受 UTF-8 文本材料；PDF、DOCX 等先提取文本。示例 JSON 用于说明请求结构，不是此 CLI 的输入协议。
需要图形时去掉 `--no-figures`；图形是模拟 shell，不是真实研究分析。

完整 catalog 直接生成与独立检查：

```powershell
python -X utf8 tfls-shell/scripts/generate_project_aligned_outputs.py --generic-template --document-version 1.0 --type all --no-figures --output-dir ./tfl-full --json
python -X utf8 tfls-shell/scripts/validate_outputs.py --contract ./tfl-full/delivery-contract_v1.0.json --json
```

定制交付必须带 `--contract` 验证本次子集与配置。无该参数是原始 Product 基线检查，不适用于标题去重后的新交付。状态及验证结果均需检查；参考资产齐备不代表生成通过。已有同名文件会拒绝覆盖。

## 维护与验证

```powershell
python -X utf8 -m unittest discover -s tests -p test_tfls_shell.py -v
python -X utf8 scripts/validate_all.py
python -X utf8 scripts/generate_index.py
.\scripts\install.ps1 -SkillName tfls-shell
```

`evals/evals.json` 定义行为用例，尚需 agent 实际执行并由统计师复核；机械回归通过不代表临床适用性已确认。
`PACKAGE_GUIDE.md` 中原仓库安装命令及 `scripts/validate_skill_baseline.py` 属于上游维护工具，在本项目使用上述工具链。
保持 `docs/`、`package_assets/`、`runtime/`、`examples/` 的相对路径，包内脚本依赖这些路径。
