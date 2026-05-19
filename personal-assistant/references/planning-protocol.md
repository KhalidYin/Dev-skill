# Planning Protocol

多轮交互式规划流程。当用户触发规划请求时，不走一次性生成，而是分轮与用户确认，确保每个 Phase 的粒度足够细、边界足够清晰。

## 触发条件

以下任一情况进入规划模式：

- 用户明确说"帮我规划一下"、"先想清楚再做"、"plan this out"、"设计一下方案"
- 任务预估超过 3 个 DEVLOG 轮次
- 涉及多个模块或功能，需要排序列
- 架构决策需要记录理由

## 规划模式总览

规划本身是一个独立的多轮交互过程，不直接修改代码。规划完成后，PLAN.md 作为执行阶段的合同文件。

```
规划模式（多轮交互）
  ├── 第 1 轮：目标与范围确认
  ├── 第 2 轮：Phase 拆解（概要）
  ├── 第 3 轮：逐 Phase 细化（可按 Phase 数量拆为多轮）
  └── 第 4 轮：最终确认，写入 PLAN.md
```

## 第 1 轮：目标与范围确认

### AI 动作

1. 阅读相关的主文档（`PROJECT_GUIDE.md`、`PROJECT_SPEC.md`）和项目记忆
2. 检查附近代码，理解当前实现状态
3. 输出以下内容，向用户确认：

```markdown
## 目标
[一句话 — 要构建什么，为什么]

## 范围
- **包含**：[明确要做的事]
- **不包含**：[明确不做的事，防止范围蔓延]

## 约束
- [技术约束、时间约束、依赖约束]

## 关键决策点
- [需要用户在前置回答的问题，如：用 Redis 还是内存缓存？]
```

### 用户确认

用户对目标、范围、约束进行确认或调整。如果用户提出修改，AI 更新后再次确认。直到用户说"可以"、"确认"、"开始拆解"等，才进入下一轮。

### 规则

- **不要跳过**：即使用户的问题看起来很直接，也要先确认目标和范围
- **不要猜测**：关键决策点必须由用户回答，AI 不能代为决定
- **排除项是必须的**：范围中必须写"不包含"，防止 AI 在后续执行中自行扩展

## 第 2 轮：Phase 拆解（概要）

### AI 动作

1. 基于确认的目标和范围，将工作拆解为 2-6 个 Phase
2. 输出 Phase 总览表，每个 Phase 只有目标一句话：

```markdown
## Phase 拆解

| Phase | 目标 | 预估轮次 | 依赖 |
|-------|------|---------|------|
| P1 | 数据模型与迁移 | R001-R002 | - |
| P2 | API 端点实现 | R003-R005 | P1 |
| P3 | 中间件与路由保护 | R006-R007 | P2 |
| P4 | 前端页面与交互 | R008-R010 | P3 |

### Phase 依赖图（文字版）
P1 → P2 → P3 → P4
```

### 拆解原则

- **每个 Phase 应该在 1-3 个 DEVLOG 轮次内完成**。如果一个 Phase 预估超过 3 轮，继续拆。
- **每个 Phase 有明确的"完成"定义**——不是"做了一半"，而是"可以独立验证"
- **Phase 之间有清晰的边界**——不会出现"这个文件在 P2 和 P3 都要改，到底归谁"
- **依赖链尽量线性**——减少并行 Phase（并行 Phase 增加 AI 上下文切换成本）

### 用户确认

用户可以调整 Phase 顺序、合并或拆分 Phase。直到确认后，进入下一轮。

## 第 3 轮：逐 Phase 细化

这是规划的核心环节。每个 Phase 必须细化到"换一个 AI session 也能无歧义执行"的程度。

### AI 动作

按 Phase 顺序逐个细化。对于 2-3 个 Phase 的小计划，可以一轮全部细化；对于 4+ 个 Phase 的大计划，每轮细化 1-2 个。

每个 Phase 的细化模板：

```markdown
## P1: [Phase 名称]

### 输入条件
- [开始本 Phase 前必须为真的条件]
- [如："数据库已运行且 Alembic 已配置"]
- [如："P0 的 User 模型已合并到 main"]

### 产出
- [具体的、可验证的交付物]
- [如："User 模型文件 src/models/user.py"]
- [如："Alembic 迁移脚本，支持 upgrade/downgrade"]

### 完成标准
- [ ] [可客观验证的标准]
- [ ] [如："User.create() 和 User.get_by_email() 通过单元测试"]
- [ ] [如："迁移脚本 upgrade + downgrade 均无错误"]
- [ ] [如："密码使用 bcrypt 哈希，测试验证非明文存储"]

### 边界（本 Phase 明确不做）
- [排除项 — 防止 AI 在执行中越界]
- [如："不做 JWT token 生成逻辑（那是 P2 的）"]
- [如："不做 API 端点（那是 P2 的）"]
- [如："不做前端页面（那是 P4 的）"]

### 涉及文件
- `src/models/user.py` — 新建
- `migrations/versions/xxxx_add_user.py` — 新建
- `tests/test_user_model.py` — 新建

### 关键决策
- [如果本 Phase 有技术选择需要用户拍板，列在这里]
- [如："密码哈希用 bcrypt 还是 argon2？（推荐 bcrypt — 生态更成熟）"]
```

### UI 类 Phase 的细化要求

UI 类 Phase 需要额外的细节层次，确保视觉效果和交互行为没有歧义：

```markdown
### 涉及页面/组件
- 页面：`src/pages/Login.tsx` — 新建
- 组件：`src/components/LoginForm.tsx` — 新建
- 组件：`src/components/ErrorMessage.tsx` — 复用已有

### 组件树
App
└── LoginPage
    ├── LoginForm
    │   ├── EmailInput (受控)
    │   ├── PasswordInput (受控)
    │   ├── SubmitButton
    │   └── ErrorMessage (条件渲染)
    └── AuthRedirectLink

### 状态矩阵
| 状态 | 触发条件 | UI 表现 |
|------|---------|---------|
| 初始 | 页面加载，未输入 | 表单为空，按钮可点击 |
| 提交中 | 点击登录按钮 | 按钮显示"登录中..."，禁用 |
| 错误 | API 返回 401 | ErrorMessage 显示"邮箱或密码错误" |
| 成功 | API 返回 200 + token | 跳转到 /dashboard |
| 网络错误 | API 无响应 | ErrorMessage 显示"网络错误，请重试" |

### 交互流
1. 用户输入邮箱和密码
2. 点击"登录"按钮（或按 Enter）
3. 前端校验：邮箱格式、密码非空
4. 调用 POST /api/auth/login
5. 成功 → 存储 token → 跳转 /dashboard
6. 失败 → 显示错误信息，保留表单内容

### 不做
- 不做"记住我"功能（后续迭代）
- 不做社交登录（后续迭代）
- 不做密码可见性切换（后续迭代）
```

### 用户确认

对每个 Phase 的细化内容进行确认。用户可能需要调整完成标准、边界或关键决策。确认一个 Phase 后，继续下一个。

## 第 4 轮：最终确认，写入 PLAN.md

### AI 动作

1. 汇总所有确认的 Phase，写入 `docs/dep/PLAN.md`
2. 使用 `status: planning`，等待用户最终确认
3. 输出完整 PLAN.md 内容供用户最终审阅

### 用户确认

用户说"开始"、"确认执行"、"go" 等后：
1. AI 将 PLAN.md 的 `status` 更新为 `in-progress`
2. 创建 TASK_STATE.md，Goal 引用 P1
3. 进入 Development 模式的 Full Development 流程

### 用户说"需要调整"

如果用户对最终 PLAN.md 有修改意见，回到对应的细化轮次进行调整，直到确认。

## 计划完成后的处理

### 已完成计划的生命周期

```
规划完成 → status: done（保留 PLAN.md 文件，但标记为完成）
新规划触发 → 直接覆盖 PLAN.md（旧内容已同步到主文档和 DEVLOG）
```

### 覆盖前检查

覆盖 PLAN.md 前，AI 必须确认：
1. 旧计划的产出已反映在 `PROJECT_SPEC.md` 或 `PROJECT_GUIDE.md` 中
2. 旧计划的执行记录已完整写入 DEVLOG
3. 旧计划中的关键决策已保存到项目记忆（`docs/main/memory/`）

如果以上任一项缺失，AI 必须先补齐再覆盖。

### 为什么不归档

- PLAN.md 是**执行工具**，不是**历史记录**
- 计划的核心内容在执行过程中已同步到主文档（蓝图）和 DEVLOG（日记）
- 保留旧 PLAN.md 会造成混淆——AI 可能读到过期的计划内容
- 覆盖而非归档，保持 `docs/dep/` 中只有一个"当前计划"

## 执行阶段的 Phase-Gate

规划完成后进入执行阶段，每完成一个 Phase 必须经过 Gate 验证才能进入下一个。

### TASK_STATE.md 与 Phase 的关联

```markdown
## Goal
P2 — 实现注册/登录 API（PLAN.md Phase 2）

## Progress
- [x] POST /api/auth/register 端点
- [ ] POST /api/auth/login 端点
- [ ] 请求校验（邮箱格式、密码长度）
- [ ] 集成测试

## Phase Context
- **Phase 完成标准**：[引用 PLAN.md 中 P2 的完成标准]
- **Phase 边界**：[引用 PLAN.md 中 P2 的边界]
- **上一 Phase 状态**：P1 done — 数据模型已就绪
```

### DEVLOG 中的 Phase 标注

每轮 DEVLOG 标题标注所属 Phase：

```markdown
### R005 [14:30] — P2: 实现 POST /api/auth/register
```

### Gate 验证流程

当一个 Phase 的所有 TASK_STATE 项都完成时：

1. 逐条检查 PLAN.md 中该 Phase 的完成标准
2. 检查是否有越界改动（做了边界中排除的内容）
3. 全部通过 → 在 PLAN.md 中勾选完成标准，更新 Phase 总览状态
4. 有未通过的 → 补齐缺口，不进入下一 Phase
5. 发现越界改动 → 标记并询问用户："这个改动超出了 P2 的边界，是否扩展到 P2 范围，还是拆分到后续 Phase？"

## 快速规划（轻量模式）

对于 1-2 个 Phase 的小任务，可以使用快速规划模式：

1. AI 直接提出目标 + Phase 拆解（含完成标准和边界）
2. 一轮确认即可
3. 写入 PLAN.md，即刻开始执行

触发条件：用户说"快速规划一下"、"简单列个计划"，或 AI 判断任务只需要 1-2 个 DEVLOG 轮次。

快速规划不能跳过 Phase 的完成标准和边界——这两项是防止漂移的最小必要信息。
