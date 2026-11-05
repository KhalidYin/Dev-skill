# Table Layout 契约

## 1. Shell-First 规则

Tables 与 listings 只保留 layout structure，不包含最终统计结果或伪造 subject-level records。

第一列保留结构性行标签。非结构性单元格使用 placeholder。

## 2. 受控组别表头

受控 table headers 使用：

- `Group 1`
- `Group 2`

可选的更多组别通过独立 `...` 扩展列表达。

扩展列必须保持独立，不得与以下列合并：

- `Overall`
- `Total`
- `HR`
- other analytic columns

## 3. Placeholder 样式

允许的 placeholder 示例包括：

- `XX`
- `xx`
- `xx (xx.x)`
- `x.xxx`
- `(xx.x, xx.x)`
- `xx.x (xx.x, xx.x)`

placeholder 样式必须匹配目标展示模式。

## 4. 三线表规则

生成的 DOCX tables 使用 Product 三线表约定：

- top border
- header separator
- bottom border
- left-aligned table headers and body cells
- auto-fit to page width

## 5. Listing 规则

Listings 保留变量列、排序说明与关键展示字段，不得包含伪造 subject-level rows。
