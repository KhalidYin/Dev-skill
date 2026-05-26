# Dev-skill 项目约定

## 这是什么项目

Dev-skill 是一个 skill 工厂 — 在这里创建和维护 Codex Skills。

## 项目结构

- 每个包含 `SKILL.md` 的顶层目录是一个 skill
- `scripts/` — 项目级工具链（安装、校验、打包、脚手架）
- `templates/` — 新 skill 的脚手架模板
- `.skill-registry.json` — 机器可读的 skill 元数据（状态、分类、tag）

## 当用户要求添加或编辑 skill 时

1. 对于新 skill，使用 `scripts/new_skill.py` 脚手架
2. 编辑 skill 的 `SKILL.md` 和相关资源文件
3. 运行 `scripts/install.ps1`（Windows）或 `scripts/install.sh`（macOS/Linux）将 skill 链接到 `~/.Codex/skills/`
4. 提交前运行 `python scripts/validate_all.py` 校验
5. 同步更新 `.skill-registry.json` 中的状态
6. 运行 `python scripts/generate_index.py` 更新 `SKILL_INDEX.md`

## Skill 规范

- `SKILL.md` 必须包含 YAML frontmatter，以 `---` 开头和结尾
- `name` — kebab-case，最多 64 字符
- `description` — 描述何时触发和使用该 skill，最多 1024 字符，不能含 `<>`
- Skill 主体使用三级渐进式披露：
  1. 元数据（name + description）— 始终在上下文
  2. SKILL.md body — skill 被触发时加载
  3. 打包资源（scripts/、references/、assets/）— 按需加载
- 保持 SKILL.md 在 500 行以内
- 禁止在前言 (frontmatter) 中遗漏必需的 `name` 和 `description` 字段

## 校验参考

校验规则参考 `~/.Codex/skills/skill-creator/scripts/quick_validate.py`。
关键约束：
- name: kebab-case，最多 64 字符，不能以 `-` 开头/结尾或包含 `--`
- description: 最多 1024 字符，不能含 `<>`

## 工具权限

所有 `scripts/` 下的 Python 脚本和 `.ps1`/`.sh` 脚本均可运行。
