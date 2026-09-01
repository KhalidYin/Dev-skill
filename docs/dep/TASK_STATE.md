---
status: in-progress
created: 2026-08-17 11:40
updated: 2026-09-01 10:20
---

# Current Tasks

## Task 1: Generate SAP 输出契约修复与重验

status: done

### Goal

完成 `generate-sap` 的机器可检查输出契约修复：六个目标槽全部通过 L1 四道 Gate；再以两个 oncology protocol 的 4 个主样本和 1 个重复样本验证证据可追溯性与临床质量。

### Progress

- [x] 用户授权启动 P0，并将计划移入 `plans/ongoing/`
- [x] 新增集中式 `output-contract.md` 并接入 `SKILL.md`
- [x] 更新 Evidence Ledger 模板，分离当前研究来源与外部 Reference
- [x] 新增只读本地校验器及合成测试
- [x] 对 P3 既有产物执行回归，不读取隐藏参考 SAP
- [x] 运行 Skill、项目、索引和安装校验并完成 P1 Gate
- [x] 用户确认启动 P2 的 6 次新版本隔离客观重验
- [x] 冻结修复版 Skill 标签和 6 个全新隔离输入包
- [x] 执行首槽及其唯一替代运行，并对替代产物执行包内校验器与冻结 `VAL-P2-v1` checker
- [x] 首个内容失败后原样保留产物与报告，并停止剩余 5 个矩阵槽
- [x] 在正式 Gate 外实现并验证“受控小块经标准输入写入 + 会话结束后校验”的新通道
- [x] 冻结 `remediation-02`、全新 R2 Run ID 和 6 个隔离运行包
- [x] 使用新控制器执行首槽替代运行；包内校验发生内容失败后按冻结规则停止
- [x] 在正式 Gate 外实现 helper 边界修复和单命令单块控制
- [x] 通过 YAML 跨块、本地长文档、旧失败回放和真实 CLI smoke
- [x] 冻结 `remediation-03`、全新 R3 Run ID 和 6 个空输出隔离包
- [x] 使用 v2 通道执行首槽写命令审计与包内校验；内容失败后停止其余 5 槽
- [x] 追溯 R3 事件日志，确认错误括号在进入 writer 前已存在，v2 writer 未改变 payload
- [x] 以测试先行实现逐记录 JSON 校验与确定性 Ledger YAML 组装脚本
- [x] 通过本地和真实 CLI 非临床序列化 smoke；真实 CLI 结果为一次安全拒绝后的 `pass_with_recovery`
- [x] 更新 Skill 契约、测试、安装、注册索引和项目文档；3/3 Skill、11/11 单测、官方 quick validator 和 diff 检查通过
- [x] 用户确认继续，建立并冻结 `remediation-04`、6 个全新 R4 Run ID 和双通道控制器
- [x] 执行 `ONC001-R4-C01`；发现 3,238 字符块违反冻结的 3,000 字符提示上限后立即停止并保留证据
- [x] 在正式 Gate 外以失败测试复现双上限缺口，并验证单一 3,000 字符 helper 硬上限
- [x] 用户确认继续，建立并冻结 `remediation-05`、6 个新 R5 Run ID 与 `WRITE-CHUNK-03`
- [x] 执行 `ONC001-R5-C01`；生成三件套后冻结 Markdown auditor 因 payload 提及 Ledger 文件名而误报，按规则停止并保留
- [x] 在正式 Gate 外以相反合成用例复现 target 检测缺陷，并验证只解析 `--target` 的最小候选修复
- [x] Goal 模式授权持续推进；补齐 5 项 target 形式测试并冻结 `remediation-06` 与 6 个新 R6 Run ID
- [x] 执行 `ONC001-R6-C01`；3,605 字符块被 helper 安全拒绝后中断并保留首块 Draft
- [x] Gate 外以 0/2 失败测试复现分块/拒绝停止提示缺口，最小候选 2/2 通过
- [x] 冻结 `remediation-07`、6 个新 R7 Run ID，并证明 controller 只有两条批准的提示增量
- [x] R7 C01/P01 通过并锁定；P02 因 Ledger auditor 将只读 builder 源码查看误判为调用而按 Gate 停止
- [x] Gate 外以 3/5 → 5/5 测试和 R7 三槽回放验证 invocation-aware 最小修复
- [x] 冻结 `remediation-08`、6 个新 R8 Run ID，确认只有 Ledger auditor 增量
- [x] R8 C01 通过四道 Gate 并锁定；P01 输出后遭宿主流中断，原样保留并停止 R8
- [x] 确认冻结 CLI 构建被宿主移除，当前 bundled CLI 同配置 smoke 通过
- [x] 冻结 `remediation-09`、6 个新 R9 Run ID，唯一变化为 CLI 版本/路径
- [x] R9 首槽因重复编码样板 ParserError 停止，部分 Draft 与失败 audit 原样保留
- [x] Gate 外复现错误，并验证删除冗余赋值后的 Markdown/Ledger UTF-8 逐字通道
- [x] 冻结 `remediation-10`、6 个新 R10 Run ID，唯一变化为两处固定命令模板简化
- [x] R10 首槽连续完成 16 条 writer 后随交互 turn 中断，部分 Draft 与 events 原样保留
- [x] Gate 外验证 detached launcher/monitor 可跨前台调用独立完成并记录 exit code
- [x] 冻结 `remediation-11`、6 个新 R11 Run ID，生成控制器和 Skill 与 R10 一致
- [x] R11 首槽由 detached monitor 完整记录生成前失败；冻结 D664 构建已被桌面更新清理，0 个输出且正式 Gate 未开始
- [x] Gate 外以当前 B993 构建完成同配置真实 CLI smoke，并冻结仅重钉路径的 `remediation-12` 与 6 个新 Run ID
- [x] `ONC001-R12-C01` 三件套完成并通过 Markdown audit、Ledger audit、package validator 和冻结 objective checker，已锁定
- [x] `ONC001-R12-P01` 三件套完成并通过四道 Gate（含 reference 与 target-leakage 检查），已锁定
- [x] `ONC001-R12-P02` 独立完成并通过四道 Gate，CASE-ONC-001 达到 3/3 locked
- [x] `ONC004-R12-C01` Markdown audit 通过但 Ledger audit 因一次 builder `--help` 实际调用失败；R12 原样停止且后两槽未运行
- [x] Gate 外完成 `LEDGER-PROMPT-SMOKE-01`：21 add + 1 finalize，unexpected/failed/external/network 均为 0
- [x] 冻结仅增加一条 builder 禁止探查指令的 `remediation-13`、6 个新 Run ID 和空输出隔离包
- [x] `ONC001-R13-C01` 在 7 次成功 writer 后因 `gpt-5.6-sol` capacity 返回 `turn.failed`；部分 Draft 原样保留，四道 Gate 未开始，R13 停止
- [x] Gate 外 `CLI-CAPACITY-SMOKE-01` 验证同一模型/配置恢复，完整 `turn.completed` 且退出码 0
- [x] 冻结与 R13 控制完全一致的 `remediation-14`、6 个新 Run ID 和空输出隔离包
- [x] `ONC001-R14-C01` 完成两个 Markdown artifacts 与 21 次 Ledger add 后，`item_87` 被执行层无退出码拒绝；Markdown audit pass、Ledger audit fail，R14 原样停止
- [x] Gate 外在本地和同一 CLI 命令工具中重放 `item_87` 的完全相同单条 add，均通过且 CLI 具有完整终止事件
- [x] 冻结无功能增量的 `remediation-15`、6 个新 Run ID 和空输出隔离包；输入、Skill 与全部运行控制和 R14 内容一致
- [x] `ONC001-R15-C01` 完成三件套并通过 Markdown audit、Ledger audit、package validator 和冻结 objective checker，0 warning，已锁定
- [x] `ONC001-R15-P01` 在零输出时因模型 capacity 失效；原现场保留，并按每槽一次额度冻结内容一致的替代 Run ID `ONC001-R15-P03`
- [x] P03 在 10 次辅助读取后再次因模型 capacity 于零输出终止；替代额度耗尽，R15 在 1/6 locked 处停止且余下槽未运行
- [x] Gate 外 `CLI-CAPACITY-SMOKE-03` 验证模型恢复，并确认 `pdftotext` 缺失但 `pypdf` 可用；不批准无证据的 PDF 控制变化
- [x] 冻结无功能增量的 `remediation-16`、6 个新 Run ID 与空输出包；输入/Skill/控制内容一致及全部语法检查通过
- [x] R16 C01 在零输出时因 capacity 失效；冻结内容一致的唯一替代 C02，并以 10/10 多轮 capacity soak 验证持续响应后启动
- [x] R16 C02 完成三件套并通过 30 writer、64 add + 1 finalize、包 validator 与冻结 checker，0 warning，已锁定为 1/6
- [x] R16 P01 完成三件套并通过 28 writer、60 add + 1 finalize、包 validator 与冻结 checker，9/9、0 warning，已锁定为 2/6
- [x] R16 P02 完成三件套并通过 30 writer、76 add + 1 finalize、包 validator 与冻结 checker，9/9、0 warning，已锁定为 3/6
- [x] R16 ONC004 C01 完成三件套并通过 29 writer、67 add + 1 finalize、包 validator 与冻结 checker，9/9、0 warning，已锁定为 4/6
- [x] R16 ONC004 P01 完成三件套并通过 22 writer、71 add + 1 finalize、包 validator 与冻结 checker，9/9、0 warning，已锁定为 5/6
- [x] R16 ONC004 P02 完成三件套并通过 28 writer、92 add + 1 finalize、包 validator 与冻结 checker，9/9、0 warning，L1 六槽达到 6/6
- [x] 依据用户指定的验证复盘，将验证拆成一次性 L0、六槽输出合同 L1 和 4+1 临床质量 L2；不再用基础设施联合成功率衡量 Skill
- [x] 冻结外层 `SAP-VALIDATION-GOVERNANCE-V2`；保留 R16 控制不变，基础设施失败改为 invalid-run 且仅局部替换
- [x] 完成 R16 六槽四道 L1 Gate，达到 6/6 locked
- [x] 固化 4+1 L2 样本、创建 5 个匿名评审包并恢复原 P2 盲评入口
- [x] 从六个锁定输出中按 4 个主样本 + 1 个重复样本创建匿名包并移交原 P2；专业临床质量评分归入 P2 P4

### Working Context

- **Files being edited**: `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`, `.validation-work/generate-sap/oncology-phase1-2/cli-capacity-soak-v1/`, `docs/dep/`
- **Last command run**: 构建并验证 `REV-101` 至 `REV-105` 五个匿名包；每包 6 个文件、Run ID/arm/repeat 标签扫描 0 命中、空白 scorecard 可解析
- **Key decisions**: R16 内部控制继续冻结；外层验证只统计产品质量，capacity/CLI/缺少辅助工具等基础设施异常标记 invalid-run、排除出 Skill 成功率并局部替换
- **Blocker**: None；P0 输出合同修复完成，原 P2 已恢复到 qualified statistician 盲评入口

### Phase Context

- **Sub-plan**: `docs/dep/plans/complete/P0-generate-sap-output-contract.md`
- **Phase**: P2-generate-sap-blind-validation P4 - ready-for-blinded-statistician
- **Input conditions**: P1 全部完成标准已通过；修复后的 Skill 已安装；旧产物、隐藏 SAP 和冻结 checker 未修改
- **Completion criteria**: 六个目标槽全部通过冻结 L1 四道 Gate并锁定；其中两个 protocol × protocol-only/precedent-assisted 共 4 个主样本，加 1 个预注册重复样本完成独立 L2 临床质量评审
- **Boundaries**: 不读取隐藏 SAP；不修改统计专业规则；不增加 Agent Workflow；不自动改写失败输出

### Resume From

由合格统计师在不访问 mapping 的前提下完成五份 scorecard；全部锁定后再单独授权 hidden reference SAP 比较与解盲归因。

## Task 2: Generate SAP 真实方案盲测 P4

status: in-progress

### Goal

在 4+1 匿名样本上完成两案例版本对齐、AI 事实预审和 1 名合格统计师最终盲评。

### Progress

- [x] 核对 P2 Gate 和 P3 输入、产出、完成标准与边界
- [x] 从本机配置锁定 `gpt-5.6-sol`、`high`，并锁定支持该模型的应用内 Codex CLI 0.150.0-alpha.8
- [x] 建立 6 个最小隔离运行包，确保只含允许输入且输出目录为空
- [x] 保留不合格执行通道产生的 `ONC001-C01/C02` invalid 记录，建立替代 Run ID `ONC001-C03`
- [x] 原样保留 `ONC001-C03` 及失败检查报告；不修改冻结 Skill/prompt/checker，建立替代 Run ID `ONC001-C04`
- [x] 在 6 个独立 ephemeral 会话中显式调用冻结 `generate-sap`，关闭网络
- [x] 对 6 份输出执行客观检查并更新运行状态；1 份通过并锁定，5 份 invalid 且原样保留
- [x] 依据 post-remediation 4+1 治理创建 Review ID 映射和五个匿名评审包
- [x] P4-A：完成两案例版本关系说明和 5 份不含评分的 AI 事实预审
- [ ] P4-B：由 1 名合格统计师完成并锁定 5 份盲态 scorecard
- [x] 执行 P3 Phase Gate 并更新运行登记和计划；Gate 结果为 blocked
- [x] 用户确认后建立独立的最小客观契约修复计划 `P0-generate-sap-output-contract.md`
- [x] 用户授权启动 P0，计划已移入 ongoing；P1 输出契约修复正在执行

### Working Context

- **Files being edited**: `.validation-work/generate-sap/oncology-phase1-2/comparison/`, `.validation-work/generate-sap/oncology-phase1-2/l2-review/`, `docs/dep/`
- **Last command run**: 验证五个匿名包各含 8 个文件、Protocol/参考 SAP 对应正确、预审各含 6 个主题且无 AI 评分字段、盲化标签 0 命中、scorecard 仍为空白
- **Key decisions**: P4-A 已完成；ONC001 将后发 DOR 规格与参考实现细节分开，ONC004 将停止 expansion/abbreviated CSR 归为 Protocol 后运营决定，不自动判生成错误；下一步只做 P4-B 单统计师盲评
- **Blocker**: P4-B 需要 1 名合格统计师完成并签署 5 份 scorecard；AI 不替代该专业结论

### Phase Context

- **Sub-plan**: `docs/dep/plans/ongoing/P2-generate-sap-blind-validation.md`
- **Phase**: P4 - 版本对齐、AI 预审和统计师盲评
- **Input conditions**: P3 Gate 已通过；L1 6/6 locked；P4-A Gate 已通过；五个包已加入对应 reference SAP 和仅含事实定位的 AI 预审
- **Completion criteria**: 两份版本关系说明、5 份事实预审和 5 份合格统计师 scorecard 全部完成并锁定
- **Boundaries**: AI 不评分；不读取 Review ID 映射；不修改原输出、Skill、阈值或评分锚点；不读取保留案例

### Resume From

由 1 名合格统计师在不访问 `control/review-id-mapping.yaml` 的前提下，逐包确认或修正 `ai-prereview.yaml`，完成并签署 `scorecard.yaml`；五份全部锁定后才进入 P5 解盲。

## Task 3: 清理已退役 Skill 残留

status: blocked

### Goal

移除 Codebuddy 安装目标并清理已退役的 `clinical-statistical-design` 残留。

### Progress

- [x] 核对安装脚本中的 Codebuddy 路径
- [x] 验证四个旧 Junction 均指向本项目旧目录
- [x] 修改 Windows 和 Bash 安装脚本
- [ ] 删除旧 Junction、空目录和旧分发包（工具安全策略阻断）
- [x] 执行安装与项目校验
- [x] 更新开发日志；删除完成后再移除本检查点

### Working Context

- **Files being edited**: `scripts/install.ps1`, `scripts/install.sh`, `docs/dep/devlog/`
- **Last command run**: 安装脚本、项目校验和 Codex quick validator 均通过；脚本中已无 Codebuddy 引用
- **Key decisions**: 用户已明确授权删除旧 Skill；外部只删除目标精确指向本项目旧目录的 Junction
- **Blocker**: Shell 安全策略拒绝所有删除命令，即使目标已验证且用户已授权；需用户在本机终端执行精确清理命令

### Resume From

用户完成精确清理命令后，复核六个旧路径均不存在并删除本检查点。
