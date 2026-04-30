# Dev-skill

Claude Code 技能工厂 — 可持续创建、开发和维护 Claude Code Skills 的项目。

## 快速开始

```bash
# 创建新 skill
python scripts/new_skill.py

# 将项目中的 skill 链接到 Claude Code（开发期间即时生效）
# Windows:
./scripts/install.ps1
# macOS/Linux:
./scripts/install.sh

# 校验所有 skill
python scripts/validate_all.py

# 打包分发
python scripts/package_all.py
```

## 目录结构

```
Dev-skill/
├── scripts/          # 项目工具链（脚手架、校验、打包、安装）
├── templates/        # 新 skill 脚手架模板
├── dist/             # 打包输出（.skill 文件）
├── <skill-name>/     # 每个 skill 一个顶层目录
│   ├── SKILL.md      # 必需 — skill 定义文件
│   ├── scripts/      # 可选 — 可执行脚本
│   ├── references/   # 可选 — 上下文文档
│   ├── assets/       # 可选 — 模板、图标等资源
│   └── evals/        # 可选 — 测试用例
└── ...docs
```

## 文档

- [SKILL_INDEX.md](SKILL_INDEX.md) — 全部 skill 清单
- [CONTRIBUTING.md](CONTRIBUTING.md) — 开发流程和规范
- [personal-assistant/](personal-assistant/) — 示例 skill（文档驱动的 R/Python 开发助手）
