# 代码风格约定

## 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| Skill 目录和 name | kebab-case，最多 64 字符 | `personal-assistant` |
| Python 文件、函数和变量 | snake_case | `generate_index.py` |
| Markdown 资源文件 | 小写 kebab-case | `decision-contract.md` |
| JSON 字段 | 延续所在文件的既有 snake_case | `last_modified` |

## 格式

- Python：4 空格缩进，保持清晰的标准库优先导入顺序。
- JSON：2 空格缩进，UTF-8 编码，文件末尾保留换行。
- Markdown：使用清晰标题层级；项目文档使用中文。
- YAML frontmatter：以 `---` 开始和结束，仅使用校验器允许的字段。

## 注释规则

- 解释非显然的设计原因，不重复代码本身。
- Python 公共工具函数使用简洁 docstring。

## 导入顺序

Python 按标准库、第三方库、本地模块分组。

## 错误处理

- CLI 校验失败时输出具体原因并返回非零退出码。
- 文件不存在等可预期情况应给出可操作提示，不静默吞掉错误。

## 特殊约定

- 新 skill 使用 `scripts/new_skill.py` 创建。
- 优先做最小修改，不引入与 skill 运行无关的辅助文档。

