# 贡献指南

## 开发流程

### 1. 创建新 Skill

```bash
python scripts/new_skill.py
```

交互式提示：
- **Skill name** — kebab-case 格式，例如 `my-awesome-skill`
- **Description** — 一行描述，说明 skill 的功能和触发场景

脚本会自动：
- 从 `templates/` 生成目录结构和 `SKILL.md`
- 创建 `evals/evals.json` 骨架
- 注册到 `.skill-registry.json`（状态设为 `draft`）

### 2. 编写 Skill 内容

编辑生成的文件：

- **`<skill-name>/SKILL.md`** — 核心 skill 定义。frontmatter 已经填好，需要完善 body 内容
- **`<skill-name>/scripts/`** — 可选，放可执行脚本
- **`<skill-name>/references/`** — 可选，放详细参考文档
- **`<skill-name>/assets/`** — 可选，放模板、图标等静态资源

### 3. 安装链接（使 Skill 在开发期间可用）

Claude Code 从 `~/.claude/skills/` 加载 skill。安装脚本将项目中的 skill 目录链接到那里：

**Windows:**
```powershell
./scripts/install.ps1          # 链接所有 skill
./scripts/install.ps1 -SkillName my-skill  # 只链接一个
```

链接策略：SymbolicLink → Junction → Copy（自动回退）

**macOS/Linux:**
```bash
./scripts/install.sh           # 链接所有 skill
./scripts/install.sh my-skill  # 只链接一个
```

### 4. 测试 Skill

- 在另一个项目中启动 Claude Code
- 确认 skill 出现在可用的 skill 列表中
- 用相关任务触发该 skill，验证行为正确

### 5. 添加测试用例 (Evals)

编辑 `<skill-name>/evals/evals.json`：

```json
{
  "skill_name": "my-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "应该触发此 skill 的用户 prompt",
      "expected_output": "期望的输出描述",
      "files": ["evals/files/test_input.txt"],
      "expectations": [
        "skill 应该被触发",
        "输出应该包含 X"
      ]
    }
  ]
}
```

### 6. 校验和更新

```bash
# 校验所有 skill
python scripts/validate_all.py

# 更新 skill 索引
python scripts/generate_index.py

# 更新 registry 状态（手动编辑 .skill-registry.json）
# draft -> stable 当 skill 经过充分测试后
```

### 7. 打包分发

```bash
# 打包所有 skill
python scripts/package_all.py

# 打包单个 skill
python scripts/package_all.py --skill my-skill
```

`.skill` 文件输出到 `dist/` 目录。

## Skill 规范要点

| 约束 | 规则 |
|------|------|
| `name` | kebab-case，最多 64 字符 |
| `description` | 最多 1024 字符，不能含 `<>` |
| 文件编码 | UTF-8 |
| SKILL.md 行数 | 推荐 ≤ 500 行 |
| frontmatter | YAML，以 `---` 开始和结束 |

## Registry 状态说明

| 状态 | 含义 |
|------|------|
| `draft` | 开发中，尚未完成 |
| `stable` | 已完成并通过测试 |
| `deprecated` | 仍可用，但不推荐使用 |
| `archived` | 已归档，不再安装 |
