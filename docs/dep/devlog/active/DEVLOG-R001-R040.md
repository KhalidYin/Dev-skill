# Dev Log — R001-R040

---

## 2026-08-12

### R001 [15:31] 新增 Clinical Statistical Design POC

#### Done

- 按项目脚手架创建 `clinical-statistical-design`，采用单一显式调用入口和包内渐进式披露。
- 将首个支持范围锁定为随机平行组确证性研究的连续重复测量主要终点；其他设计类型安全返回 `unsupported_scope`。
- 定义 `DecisionPackage` 输入输出契约、estimand 到敏感性分析的决策链、连续重复测量方法清单和来源策略。
- 配置 `allow_implicit_invocation: false`，避免因 “SAP” 关键词或 SAP ERP 语境误触发。
- 增加 8 个显式行为 eval 和 24 条未来 Workflow Router 语料，覆盖 `proposed`、`needs_input`、`unsupported_scope`、`not_applicable`、PII、来源伪造和 protocol 冲突。
- 更新注册表与索引，安装到 Codex、Claude、Agents 和 Workbuddy，生成 `.skill` 分发包。
- 运行项目全量校验、Codex 官方 quick validator、JSON/YAML/引用完整性检查和独立前向测试；最终独立审计无 P0/P1。
- 完成项目文档 Bootstrap，并同步本次已实现的架构、规格、测试和长期决策记录。

#### Issues / Blockers

- 工程校验通过，但尚未完成真实案例的资深统计师一致性测试或监管适用性验证，因此 registry 保持 `draft`。
- 项目校验器读取既有中文 skill 时触发 GBK 解码错误并回退 builtin validator；新 skill 同时通过 Codex 官方 validator，不影响本次交付。
- Codebuddy 的 skills 根目录不存在，安装脚本按设计跳过；其余四个目标均创建 Junction。

#### Next

1. 使用脱敏的真实或合成案例开展统计师盲评，验证决策一致性、可追溯性和安全退出。
2. 在未来 Workflow Layer 实现 Router 后，以 `evals/router-evals.json` 测量路由 precision/recall。
3. 通过 POC 后，再按独立用户意图扩展 SAP review、TTE、multiplicity/interim/sample-size 和 SAP authoring 等能力。

#### Files Changed / Commits

- `.skill-registry.json`（modified, uncommitted）
- `SKILL_INDEX.md`（modified, uncommitted）
- `USAGE.md`（added, uncommitted）
- `clinical-statistical-design/SKILL.md`（added, uncommitted）
- `clinical-statistical-design/agents/openai.yaml`（added, uncommitted）
- `clinical-statistical-design/evals/evals.json`（added, uncommitted）
- `clinical-statistical-design/evals/router-evals.json`（added, uncommitted）
- `clinical-statistical-design/references/contracts.md`（added, uncommitted）
- `clinical-statistical-design/references/decision-framework.md`（added, uncommitted）
- `clinical-statistical-design/references/continuous-repeated.md`（added, uncommitted）
- `clinical-statistical-design/references/source-policy.md`（added, uncommitted）
- `dist/clinical-statistical-design.skill`（generated, ignored, uncommitted）
- `docs/main/PROJECT_GUIDE.md`（added, uncommitted）
- `docs/main/PROJECT_SPEC.md`（added, uncommitted）
- `docs/main/CODE_STYLE.md`（added, uncommitted）
- `docs/main/TEST_GUIDE.md`（added, uncommitted）
- `docs/main/memory/MEMORY.md`（added, uncommitted）
- `docs/main/memory/project-clinical-statistical-design.md`（added, uncommitted）
- `docs/dep/DEVLOG.md`（added, uncommitted）
- `docs/dep/devlog/INDEX.md`（added, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（added, uncommitted）
- `docs/dep/PLAN.md`（added, uncommitted）
- `docs/deploy/DEPLOY_GUIDE.md`（added, uncommitted）
- `docs/dep/TASK_STATE.md`（temporary checkpoint, removed at completion）

---

## 2026-08-17

### R002 [11:31] [P1-generate-sap-skill] P1-P5: 重构 Generate SAP 初版

#### Done

- 将目标从统计 `DecisionPackage` 修正为单入口 `generate-sap` authoring Skill；不再承载半个 Agent Workflow。
- 使用项目脚手架创建并注册新包，配置显式调用策略，退役旧 `clinical-statistical-design` draft 的仓库内容和注册项。
- 固化 18 章通用 SAP review-draft 结构；输入不足、来源冲突和未决统计参数在对应章节使用稳定的 `TBD`、`Author Query` 或 `Conflict` 表达，不省略整体结构。
- 建立 `sourced / derived / proposed / tbd / conflict / not-applicable` 六种生成模式、内容项契约、来源优先级、跨章节检查和 Generation Evidence Ledger。
- 增加研究设计、Estimand/ICE、分析人群、连续重复主要终点、缺失/敏感性和安全分析的首版规则；未确认的研究特定参数不得补造。
- 增加同类研究广泛检索、分层筛选、深入阅读、差异总结和直接 Reference 规则；网络不可用或检索被禁止时显式降级。
- 增加 7 个行为 eval 和 5 个合成 fixture；完成部分输入、完整输入、先例材料和来源冲突的独立前向测试。
- 通过 Codex 官方 quick validator、项目全量校验、JSON/YAML/本地链接/章节结构/分发包完整性检查；更新索引，安装到 Codex、Claude、Agents 和 Workbuddy，并生成 `generate-sap.skill`。
- 同步项目规格、架构、测试、使用说明和长期记忆，完成 P1-P5 计划归档。

#### Issues / Blockers

- 项目全量校验器读取既有中文 Skill 时发生 GBK 解码错误并回退 builtin validator；`generate-sap` 已单独通过 Codex 官方 quick validator，当前交付不受影响，但工具链编码处理仍需修正。
- 安全策略阻止删除工作区外四个旧 `clinical-statistical-design` Junction 和被忽略的 `dist/clinical-statistical-design.skill`。旧 Junction 指向不含 `SKILL.md` 的空目录，当前不可调用；旧二进制不参与注册、索引或新包安装。
- Codebuddy 的 skills 根目录不存在，安装脚本跳过该宿主；其余四个目标安装成功。
- 本版本保持 `draft`；尚未经过真实项目材料和资深统计师的正式验收，不能视为批准或法规合规保证。

#### Next

1. 使用脱敏真实 Protocol、Sponsor 模板和已确认统计决定进行统计师审阅，重点验证章节充分性、问题传播和证据追溯。
2. 在获得明确文件系统删除授权或由用户手工处理后，清理四个失效旧 Junction 和旧分发包。
3. 若多案例显示固定结构或记录格式漂移，再最小化增加 JSON Schema 或结构校验脚本；首版不预建额外运行时。

#### Files Changed / Commits

- `generate-sap/`（added, uncommitted）
- `.skill-registry.json`（modified, uncommitted）
- `SKILL_INDEX.md`（modified, uncommitted）
- `USAGE.md`（added, uncommitted）
- `docs/main/PROJECT_SPEC.md`（added, uncommitted）
- `docs/main/PROJECT_GUIDE.md`（added, uncommitted）
- `docs/main/TEST_GUIDE.md`（added, uncommitted）
- `docs/main/memory/MEMORY.md`（added, uncommitted）
- `docs/main/memory/project-generate-sap.md`（added, uncommitted）
- `docs/dep/PLAN.md`（added, uncommitted）
- `docs/dep/plans/complete/P1-generate-sap-skill.md`（added, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（added, uncommitted）
- `docs/dep/devlog/INDEX.md`（added, uncommitted）
- `dist/generate-sap.skill`（generated, ignored, uncommitted）

---

### R003 [13:10] 移除 Codebuddy 安装目标并尝试清理旧 Skill

#### Done

- 从 Windows 与 Bash 安装脚本中移除 Codebuddy skill root，只保留 Claude、Codex、Agents 和 Workbuddy。
- 将 `install.sh` 从既有 CRLF 规范化为 LF，修复 Bash 在 `do\r` 处的语法错误，并更新两套脚本的宿主提示文本。
- 逐项验证四个旧 `clinical-statistical-design` 外部条目均为 Junction，且目标均精确指向本项目旧目录。
- 重新运行单 Skill Windows 安装，`generate-sap` 在四个目标均成功建立 Junction；项目校验 3/3 通过，Codex 官方 quick validator 通过。

#### Issues / Blockers

- 当前 Shell 工具安全策略拒绝所有删除命令，包括逐个非递归解除 Junction 和删除工作区内旧分发包；用户授权不改变该工具级限制，因此旧 Junction、旧空目录和旧 `.skill` 包仍存在。
- `.codebuddy\skills` 实际不存在；本轮删除的是安装脚本中的 Codebuddy 目标配置。

#### Next

1. 用户在本机 PowerShell 执行交付消息中的精确清理命令。
2. 后续复核旧路径全部不存在，再删除 `docs/dep/TASK_STATE.md`。

#### Files Changed / Commits

- `scripts/install.ps1`（modified, uncommitted）
- `scripts/install.sh`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（added, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

## 2026-08-27

### R004 [11:24] [P2-generate-sap-blind-validation] P1: 冻结盲测合同与客观检查

#### Done

- 将 P2 子计划从 backlog 移入 ongoing，完成 P1 Phase Gate，并保持 `generate-sap` Skill 本体冻结。
- 冻结 `VAL-P2-v1` 评测协议，明确两案例六次运行、角色隔离、评分权重、hard gates、差异类别、通过阈值和修改门控。
- 使用简单 Run ID、Review ID、输入/先例包标签和 `locked` 状态登记，不新增文件哈希字段。
- 扩展统计师评分表，增加 6 个总计 100 分的判分维度、逐级锚点、版本关系、盲法声明和专业判断字段。
- 建立 6 次计划运行登记和仅含公开元数据的版本关系表；`CASE-ONC-002/003` 保持 reserved-unseen。
- 实现客观检查脚本，覆盖 18 章结构、证据账本、Query/Reference 链接、generation mode 必填项、搜索/引用泄漏和越权声明；脚本明确不执行统计专业裁决。
- 新增 8 个合成测试；正向、缺章、目标搜索泄漏、正文合法目标标识、坏引用、权重、运行登记和元数据隔离测试全部通过。

#### Issues / Blockers

- 项目校验器仍会在读取既有中文 `personal-assistant` 和 `sub-brainstorm` 时触发 GBK 解码回退；builtin validator 完成校验，3/3 Skills 通过。该问题为既有工具链风险，不影响本地盲测 P1。
- 旧 `clinical-statistical-design` Junction 清理任务仍受 Shell 安全策略阻断，与本 Phase 无依赖关系。

#### Next

1. 启动 P2，审计并冻结 `PB-ONC001-v1` 和 `PB-ONC004-v1`。
2. 在首次生成前填写并锁定实际模型名称和推理配置。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/comparison/`（local ignored validation artifacts, uncommitted）
- `docs/dep/plans/ongoing/P2-generate-sap-blind-validation.md`（added/modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R005 [11:43] [P2-generate-sap-blind-validation] P2: 审计并冻结其他研究先例包

#### Done

- 核验 4 个非目标候选的 ClinicalTrials.gov 记录和 8 份 Protocol/SAP 原始 PDF，确认文档类型、版本/日期、直接来源及本地文件。
- 冻结 `PB-ONC001-v1`：入选 3 个实体瘤/免疫肿瘤先例，逐项记录相似点、重要差异、可支持内容和不得迁移的研究特定参数。
- 冻结 `PB-ONC004-v1`：只入选 2 个有限相关的血液肿瘤先例；明确没有足够接近的 AML 小分子联合先例，不以低相似实体瘤材料凑数。
- 对两个包内全部入选 Protocol/SAP 执行一次性全文 denylist 扫描，均未命中对应目标标识；bundle 元数据、直接来源和本地文件合同测试通过。
- 将内容有效性与搜索过程有效性分开登记：两个包可作为隔离生成输入，但原发现轮次曾返回目标记录，不能用于宣称自主盲搜能力通过。
- 新增 4 个先例包合同测试；盲测 comparison 测试共 12/12 通过，运行登记中的两个包更新为 `locked`。

#### Issues / Blockers

- 现有 discovery round 的根因是通用检索结果包含目标记录；过滤不会恢复该轮次的独立盲搜有效性。P3 可使用去标识审计通过的冻结包，但未来若验证搜索能力，必须由未接触目标信息的新搜索者重新执行。
- `PB-ONC004-v1` 的公共先例相似度有限，不能支持当前 AML 联合治疗的具体剂量、暴露、剂量强度或分析参数，只能支持结构与待确认问题。
- 旧 `clinical-statistical-design` Junction 清理任务仍受 Shell 安全策略阻断，与本 Phase 无依赖关系。

#### Next

1. 启动 P3 前填写并锁定实际模型名称和推理配置。
2. 在 6 个独立新会话中执行两案例的 Protocol-only 和 Protocol + 冻结先例包运行，全部关闭网络。
3. 对每份输出执行客观检查；失败不覆写原输出，使用新 Run ID 或标记为 invalid。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/precedent-bundles/`（local ignored validation artifacts, uncommitted）
- `.validation-work/generate-sap/oncology-phase1-2/search-log/2026-08-26.md`（local ignored validation artifact, modified）
- `.validation-work/generate-sap/oncology-phase1-2/comparison/run-register.yaml`（local ignored validation artifact, modified）
- `.validation-work/generate-sap/oncology-phase1-2/comparison/tests/test_precedent_bundles.py`（local ignored validation artifact, added）
- `docs/dep/plans/ongoing/P2-generate-sap-blind-validation.md`（modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R006 [14:02] [P2-generate-sap-blind-validation] P3: 隔离生成完成但客观 Gate 阻断

#### Done

- 锁定 `gpt-5.6-sol`、`high` 和应用内 Codex CLI 0.150.0-alpha.8，建立工作区内独立隔离运行包；每次运行只含冻结 Skill、目标 Protocol 和该 arm 允许的冻结先例包，并禁用生成会话的网络、插件、Apps、浏览器和 MCP。
- 完成两案例 6 个目标矩阵运行及客观检查；所有失败输出和报告均原样保留，未读取隐藏参考 SAP，未根据运行结果修改 Skill、prompt、bundle 或 checker。
- `ONC004-C01` 通过全部客观检查并标记为 `locked`；其余 5 个运行标记为 `invalid`，因此 P3 Gate 结果为 1/6 有效。
- 归纳重复的客观契约缺陷：当前 Protocol/bundle 误入外部 References、引用字段或枚举不符合 schema、固定章节标题漂移、内容单元引用未定义 source ID，以及未允许的 search status。
- 修正运行登记合同测试的计数语义：以“有输出、有客观报告、且无后续 replacement”的终态运行计数，不再把合法的 `invalid` 输出误判为未执行；comparison 测试 12/12 通过。
- 保留 `ONC001-C01/C02/C03` 的执行通道和早期替代尝试记录；全局 CLI 模型不兼容、系统临时目录只读等执行问题已通过应用内 CLI 与工作区隔离目录解决。
- 因有效输出不足，未创建 Review ID 映射和匿名评审包，未启动 P4 AI/统计师盲评；计划和任务状态更新为 `blocked`。

#### Issues / Blockers

- P3 合同要求 6 个有效匿名评审包，当前仅 1 个有效。缺陷已跨两个案例和两种 arm 重现，继续用完全相同的冻结配置重跑没有新增信息价值。
- 直接修改冻结 Skill 或生成 prompt 会破坏本轮预注册验证边界；继续推进需要用户确认将本轮记录为客观 Gate 失败，并另建最小修复计划或明确修订验证合同。
- 运行期间存在模型流连接重试、Windows `apply_patch` 多行参数限制和单命令长度限制；会话通过重试、分段写入或原生受控写入完成交付，这些执行问题不是最终 Gate 失败的主要根因。
- 旧 `clinical-statistical-design` Junction 清理任务仍受 Shell 安全策略阻断，与本 Phase 无依赖关系。

#### Next

1. 建议保持隐藏参考 SAP 未开启，正式记录当前 `generate-sap` 版本为 P3 客观 Gate 未通过。
2. 经用户确认后建立独立最小修复计划，只收紧 References schema/枚举、固定章节标题、source ID 和 search status 约束，不在本 P2 计划内直接改 Skill。
3. 修复后使用新的 Skill/Run 版本标签重跑客观 Gate；通过后才建立匿名包并进入 P4，保留案例 `CASE-ONC-002/003` 继续不消耗。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/run-workspaces/`（local ignored validation artifacts, added）
- `.validation-work/generate-sap/oncology-phase1-2/outputs/`（local ignored validation artifacts, added）
- `.validation-work/generate-sap/oncology-phase1-2/comparison/objective-checks/`（local ignored validation artifacts, added）
- `.validation-work/generate-sap/oncology-phase1-2/comparison/run-register.yaml`（local ignored validation artifact, modified）
- `.validation-work/generate-sap/oncology-phase1-2/comparison/run_generation.ps1`（local ignored validation artifact, added）
- `docs/dep/plans/ongoing/P2-generate-sap-blind-validation.md`（modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R007 [15:39] [P0-generate-sap-output-contract] P1: 固化输出契约与回归测试

#### Done

- 将 P0 修复计划移入 ongoing，保持原 P2 盲测失败证据、隐藏参考 SAP 和冻结 `VAL-P2-v1` checker 不变。
- 新增集中式 `output-contract.md`，固定 generic 模板 18 个标题，并明确当前 Protocol/修订/确认决定/Sponsor 约定进入 `source_versions/source_facts`，外部 `references` 只允许规范、同类研究和方法学来源。
- 更新 Ledger 模板，移除无效 `SEC-00`/假 Reference 示例，保留完整 18 节状态骨架和明确 `not-run` 搜索记录。
- 新增纯本地只读校验器，检查标题、字段、枚举、当前 Source 与外部 Reference 分离、Source/Reference/Query ID 闭合和搜索状态；校验器不联网、不生成、不改写，也不执行统计专业判断。
- 新增 7 个测试，覆盖当前研究标识边界、bundle 误作 Reference、标题漂移、未定义 Source/Reference、precedent/search 非法枚举和本地既有盲测回归。
- 回归结果与已冻结客观结论一致：`ONC004-C01` 通过；其余 5 个目标 invalid 输出及 `ONC001-C03` 失败，且错误类别覆盖原 objective report。
- 更新行为 eval 期望、Skill 注册日期和索引；安装到 Claude、Codex、Agents 和 Workbuddy。项目 3/3 Skill 校验、官方 quick validator、7/7 测试及 `git diff --check` 通过，`SKILL.md` 为 72 行。

#### Issues / Blockers

- P1 无功能性失败。Windows 当前权限不能创建 SymbolicLink，安装脚本按设计回退 Junction 并成功安装。
- 项目校验既有 GBK 解码问题仍使 `personal-assistant` 和 `sub-brainstorm` 回退 builtin validator；`generate-sap` 已单独通过官方 quick validator，不影响本 Phase。
- P2 需要 6 次新的模型运行；为避免跨 Phase 自动消耗运行并保持失败即停规则，本轮停在 P2 启动前等待用户确认。

#### Next

1. 用户确认后，为修复版 Skill 建立简单版本标签和 `remediation-01` 隔离运行目录。
2. 依照 P2 矩阵逐槽运行；每份输出先经过包内校验器，再经过冻结 `VAL-P2-v1` checker，任一内容失败即停止且不现场修改。
3. 仅在 6/6 通过后恢复原 P2 的匿名包装和 P4 专业盲评；隐藏参考 SAP 在此之前继续封存。

#### Files Changed / Commits

- `generate-sap/SKILL.md`（modified, uncommitted）
- `generate-sap/references/output-contract.md`（added, uncommitted）
- `generate-sap/references/precedent-research.md`（modified, uncommitted）
- `generate-sap/assets/generation-record-template.yaml`（modified, uncommitted）
- `generate-sap/scripts/validate_output_contract.py`（added, uncommitted）
- `generate-sap/evals/evals.json`（modified, uncommitted）
- `tests/test_generate_sap_output_contract.py`（added, uncommitted）
- `.skill-registry.json`（modified, uncommitted）
- `SKILL_INDEX.md`（generated, modified, uncommitted）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（added/modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R008 [16:49] [P0-generate-sap-output-contract] P2: 首个内容失败后停止客观重验

#### Done

- 建立本地忽略的 `remediation-01`，冻结 `GSAP-OC1-20260827`、`VAL-P2-v1`、统一模型配置、6 个全新 Run ID、允许输入和隔离控制文件；生成会话未接触隐藏 SAP、旧输出、manifest 或 denylist。
- `ONC001-R1-C01` 在产生输出前遇到 Windows 写入通道失败，依合同使用该槽位唯一替代 ID `ONC001-R1-C02`；原运行记录和空输出目录保留。
- 替代运行完成 Protocol 事实提取并生成三件套；Evidence Ledger、Open Questions/References 和禁止搜索状态成功落盘，目标泄漏、越权声明、Ledger schema、References 与 search-summary 客观检查通过。
- 主稿长文本写入只成功保存第 1–6 节；冻结包内校验器与 `VAL-P2-v1` checker 均报告缺少第 7–18 节及 16 个未在主稿呈现的 Query ID，结果为 2 failed checks、0 warnings。
- 在生成会话尝试补写前终止运行并复核文件长度、标题和修改时间；失败主稿保持第 1–6 节原状，objective report 已保存，剩余 5 个矩阵槽标记 `not-run-phase-stopped`。
- 更新 P0 计划、任务状态和计划面板；未修改 Skill、prompt、validator、checker、失败输出或隐藏参考 SAP，未创建匿名包或启动 P4。

#### Issues / Blockers

- 根因位于 Windows 隔离 CLI 的长文档落盘通道：普通文件变更被拒绝，单次大 `apply_patch` 超过命令长度；短 `Set-Content` 成功，但承载第 7–18 节的长 `Add-Content` 命令返回失败，主稿因此截断。
- 生成会话的自然行为是在首次非零校验后修稿，这与冻结 Gate 的“内容失败即停止并保留”冲突；当前由外层控制者及时终止，后续需把强制停止写入控制器，而不能依赖模型自觉停止。
- P2 要求 6/6 通过，当前首槽已发生内容失败，本轮必须保持 stopped；该结果不能区分 Skill 输出合同质量与写入执行通道质量。

#### Next

1. 在正式 Gate 之外创建最小写入 smoke test，只验证固定长文本分块写入、文件完整性和首次校验失败后的强制终止，不读取任何临床验证材料。
2. smoke test 通过后冻结新的控制器/运行标签；如继续 P2，使用新的 remediation 标签和全新 Run ID，不复用或覆写本轮证据。
3. 仍保持隐藏参考 SAP 和 `CASE-ONC-002/003` 封存；新的 6/6 客观 Gate 通过前不恢复匿名包装或 P4。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-01/`（local ignored validation artifacts, added/modified）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R009 [17:39] [P0-generate-sap-output-contract] P2: 修复长文档写入与校验控制通道

#### Done

- 保持 `remediation-01`、失败输出、Skill、包内 validator 和冻结 `VAL-P2-v1` checker 不变，在正式 Gate 外建立本地忽略的 `write-channel-smoke/`。
- 新增受限写入 helper：只允许三件套文件名，正文只从标准输入接收，单块最多 3,500 字符，区分首次创建与后续追加，并拒绝覆盖、超限、NUL、路径逃逸和 2,000,000 字符以上文件。
- 新增候选控制器：生成提示要求每块不超过 3,000 字符并禁止 `Set-Content`、`Add-Content`、`Out-File`、`apply_patch` 和其他临时写法；包内校验移到 Codex 生成会话完全退出之后执行。
- 本地非临床 smoke 将 102,200 字符按 2,400 字符块完整重组，超限块和路径逃逸均被拒绝。
- 首次真实 CLI smoke 因把读取 helper 识别为编码任务而加载全局 `personal-assistant`，违反隔离约束；该 attempt 被终止、标记 invalid 并单独保留，未接触临床材料。
- 第二次真实 CLI smoke 改为纯执行协议、明确禁止全局 Skill 并禁用 Skill 搜索：成功写出 24,417 字符和 18 个标题；写入器调用存在，被禁写命令为 0，外部路径读取为 0，最大命令长度为 1,520 字符。
- Python 与 PowerShell 语法检查、项目 3/3 Skill 校验、官方 `generate-sap` quick validator、7/7 单元测试、索引生成和 `git diff --check` 均通过。

#### Issues / Blockers

- 第一轮 agent smoke 的根因不是写入 helper，而是提示包含“读取脚本”等开发语义，触发了全局开发 Skill；通过把任务改为固定数据传输协议并只授权 run-local Skill 解决。该失败不能计为通道通过证据。
- `remediation-01` 仍按冻结合同保持 stopped；当前只解除技术通道阻断，尚未冻结新的 remediation 标签或启动任何临床生成。
- CLI 仍会报告 Skill 描述预算告警，即使禁用 Skill 搜索；第二次 smoke 没有实际加载全局 Skill 或读取外部路径。新的临床提示必须继续显式禁止全局 Skill，并仅授权运行包内 `generate-sap`。

#### Next

1. 用已通过 smoke 的 helper 和候选控制器建立新的 remediation 标签及全新 Run ID，复制到每个隔离运行包的 `control/`。
2. 冻结新控制器后再逐槽重启 P2；每次先等待生成会话退出，再执行包内 validator 和冻结 checker，任何内容失败仍立即停止。
3. 保持 `remediation-01`、隐藏参考 SAP 和 `CASE-ONC-002/003` 封存；新的 6/6 Gate 通过前不创建匿名包或启动 P4。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/write-channel-smoke/`（local ignored validation artifacts, added）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R010 [11:03] [P0-generate-sap-output-contract] P2: 第二次客观重验因 YAML 分块边界失败而停止

#### Done

- 冻结 `remediation-02`、6 个全新 R2 运行包、通过 smoke 的 STDIN helper/控制器、`GSAP-OC1-20260827` 和未修改的 `VAL-P2-v1` checker；所有初始输出目录为空且输入只来自上一轮冻结 Protocol/precedent/Skill。
- `ONC001-R2-C01` 在模型调用前因 Codex 应用更新移除旧 build 路径而失败；确认新可执行文件仍为 CLI 0.150.0-alpha.8 后，仅重钉路径并启动该槽唯一替代 `ONC001-R2-C02`。
- 替代运行只读取 run-local Protocol、Skill 与 control，未读取隐藏 SAP、旧输出、全局 Skill 或网络资源；完成 27,591 字节 Draft、46,093 字节 Ledger 和 9,580 字节 Open Questions/References。
- helper 正确拒绝了一个超过 3,500 字符的首次 Ledger 块，生成会话随后以更小块重试；所有内容写入结束后会话退出，外层控制器才执行包内校验。
- 包内校验器因 Ledger 第 25 行相邻 YAML sequence entry 拼接而失败；未修改的冻结 checker 因同一 YAML 解析错误返回 configuration error，未生成 objective report。
- 保存运行登记和独立 execution audit；`ONC001-R2-C02` 标记 `invalid-content-failure`，剩余 5 槽标记 `not-run-phase-stopped`，原始三件套与事件日志保持不变。

#### Issues / Blockers

- 直接根因是 controller 要求每次调用 `--strip-pipeline-newline`：PowerShell 管道附加换行被删除后，helper 又没有为 append 自动插入边界换行，导致独立合法块在文件中粘连为无效 YAML。
- 模型虽遵守单 payload 上限，却把多个 helper 调用放进同一 PowerShell command；最大命令长度 29,444 字符。上一轮非临床 smoke 只验证了纯文本完整性，没有覆盖 YAML 跨块语义或单命令单次调用。
- 根据冻结合同，内容存在后的任何包校验失败都必须停止；当前不能修补失败文件、继续剩余矩阵或再次替代同一槽。

#### Next

1. 在正式 Gate 外最小修改 helper：由 helper 自身保证 append 前恰好一个记录分隔换行，避免把边界责任交给模型或 PowerShell 管道。
2. 新增 YAML 跨块解析 smoke，并在真实 CLI smoke 中强制、审计每条 shell command 只包含一次 helper 调用及受控最大命令长度。
3. smoke 通过后再由用户决定是否建立新的 remediation 标签；隐藏 SAP、失败输出和 `CASE-ONC-002/003` 继续封存。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-02/`（local ignored validation artifacts, added/modified）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R011 [11:18] [P0-generate-sap-output-contract] P2: v2 写入边界与单命令审计 smoke 通过

#### Done

- 保持 `remediation-02` 及其失败证据完全冻结，在本地忽略的 `write-channel-smoke-v2/` 创建候选 `CTRL-STDIN-02` / `WRITE-CHUNK-02`。
- 最小修改 helper：append 时仅在现有文件末尾和新 payload 开头都没有换行时插入一个 `\n`，块内部内容保持不变。
- 更新候选控制提示，固定 PowerShell/Python UTF-8 环境和完整 helper 参数；明确每条 shell command 只能包含一个 `$chunk` 和一次 writer 调用，禁止循环或批处理多个块。
- 新增会话后命令审计：强制单命令单 writer、6,000 字符上限、writer 成功，并拒绝被禁写法、外部/全局 Skill 路径和网络命令。
- 本地 smoke 通过 102,199 字符长文档精确重组、四段 YAML 跨块解析、超限拒绝和路径逃逸拒绝。
- 回放 `ONC001-R2-C02` 旧事件得到预期失败，识别 9 条聚合 writer、8 条超长命令和失败 writer。
- 首次真实 CLI smoke 因提示接口不完整标记 invalid 并保留；补齐精确模板后的 `agent-attempt-02` 成功生成 60 项 UTF-8 YAML，6 条 writer 命令最大 1,114 字符，全部审计项通过。

#### Issues / Blockers

- 技术通道候选已经通过，但当前尚无新的 remediation 标签或临床 Run ID；不能把非临床 smoke 等同于 6/6 SAP 客观 Gate。
- Codex CLI 仍输出 Skill description budget 和 PowerShell snapshot 告警，但 agent smoke 未加载全局 Skill，也未产生外部路径或网络命令。
- `remediation-02` 继续保持 stopped，不可用 v2 helper 修补或续跑其剩余矩阵。

#### Next

1. 用户确认后，以 `CTRL-STDIN-02` / `WRITE-CHUNK-02` 建立新的 remediation 标签、全新 Run ID 和空输出隔离包。
2. 冻结 controller/helper/auditor 后逐槽运行；每次生成会话退出后先过写命令审计，再过包内 validator 和冻结 checker。
3. 任一内容或通道审计失败仍立即停止；隐藏 SAP 与 `CASE-ONC-002/003` 继续封存。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/write-channel-smoke-v2/`（local ignored validation artifacts, added）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R012 [11:54] [P0-generate-sap-output-contract] P2: 第三次客观重验因 Ledger YAML 语法失败停止

#### Done

- 建立并冻结本地忽略的 `remediation-03`、6 个全新 R3 运行包、同一 Skill/checker/validator，以及通过 v2 smoke 的 `CTRL-STDIN-02` / `WRITE-CHUNK-02`；输入与 Skill 树复核一致，所有初始输出为空。
- 执行首槽 `ONC001-R3-C01` Protocol-only 生成，完成 18 节 Draft、结构化 Ledger 和 Open Questions/References；未使用网络、外部路径、全局 Skill、隐藏 SAP 或旧输出。
- 会话后写命令审计通过：40 条 writer 命令，最大 3,509 字符；聚合、超长、失败、被禁写、外部路径和网络命令均为 0。
- 包内 validator 在 Ledger 第 417 行发现 YAML flow sequence 以 `}` 而非 `]` 结束，返回非零；按冻结顺序未运行 objective checker。
- 将首槽标记 `invalid-content-failure`，记录三件套大小并原样保留；其余 5 槽标记 `not-run-phase-stopped`。未修补单字符错误，未修改 Skill、prompt、helper、auditor、validator 或 checker。

#### Issues / Blockers

- 直接根因是模型手写 38 KB Ledger 时产生单字符 YAML 配对错误，不是分块边界、命令长度或 Windows 写入失败；v2 写入与审计技术通道已在真实临床运行中通过。
- YAML 任一语法错误会使整个证据账本不可读，说明仅依赖模型逐块手写大型结构化 artifact 仍是当前 Gate 的主要可靠性风险。
- 根据预注册规则，已有输出后的内容失败必须停止；R3 不能修补后继续，也不能启动剩余矩阵或匿名包装。

#### Next

1. 在正式 Gate 外评估最小结构化序列化方案：优先让模型输出受限记录块并由固定 helper 解析后序列化，或至少改为 YAML block style 并对每个记录块做即时纯语法拒绝；不得自动修复语义内容。
2. 先用合成、多记录和真实 CLI 非临床 smoke 证明语法方案，再由用户决定是否建立新的 remediation 与全新 Run ID。
3. 保持 R3 失败三件套、隐藏 SAP、`CASE-ONC-002/003` 和剩余矩阵封存；6/6 Gate 前不创建匿名包或启动 P4。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-03/`（local ignored validation artifacts, added/modified）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`（modified, uncommitted）
- `docs/dep/TASK_STATE.md`（modified, uncommitted）
- `docs/dep/devlog/active/DEVLOG-R001-R040.md`（modified, uncommitted）
- `docs/dep/devlog/INDEX.md`（modified, uncommitted）

---

### R013 [12:38] [P0-generate-sap-output-contract] P2: 确定性 Ledger 序列化 smoke 完成

#### Done

- 从 R3 原始事件日志确认错误括号在 writer 接收前已存在，排除 v2 helper 改写 payload；R3 失败输出和正式 Gate 状态保持不变。
- 测试先行新增 4 个 Ledger builder 单元测试；先确认脚本不存在时失败，再实现逐记录 JSON 校验、私有 JSONL 暂存、固定顶层顺序 YAML 组装和成功后暂存清理。
- builder 限制单条记录 3,500 字符、固定输出根与文件名、单例和稳定 ID 唯一性，拒绝错误 JSON、NUL、超限、重复和最终文件覆盖；不补字段、不修改语义、不判断统计方法。
- 更新 `generate-sap` 的核心步骤、输出合同、Ledger 模板和行为 eval，使脚本作为按需披露资源使用，不把它扩展成 Agent Workflow 或 Validation Engine。
- 本地 smoke 通过 18 个章节状态、60 个内容项、25 个问题、25 个一致性项的确定性组装，并证明错误 JSON 不污染暂存。
- 真实 CLI 非临床 smoke 生成 60 条目标记录和一次 finalize；最终 YAML 可解析、ID 顺序正确、暂存已清除，最大命令 566 字符，未使用网络、外部路径或被禁写法。首次问题记录字段名错误被安全拒绝并以相同语义重试，因此结论为 `pass_with_recovery`。
- 重新生成索引并安装 `generate-sap`；Windows 无管理员权限时安装器按设计回退 Junction。项目 3/3 Skill、官方 quick validator、11/11 单元测试、Python 编译、JSON 解析和 `git diff --check` 全部通过。

#### Issues / Blockers

- smoke 包装器最初把 CLI 的非 JSON 告警行当作 JSON 解析；审计器改为统计并忽略这些行，保留全部结构化命令事件。该问题只影响外层审计读取，不影响生成的 Ledger。
- `question_id`/`query_id` 暴露出提示字段名不足；未来控制提示已明确 `query_id`。builder 继续严格拒绝未知稳定 ID，不猜测用户意图。
- 当前只解除 Ledger 语法序列化风险，尚未证明临床内容合同或 6/6 客观 Gate 通过；新 remediation 仍未建立。

#### Next

1. 完成 Skill 安装、索引、项目/官方校验和全量单测，确认工作树仅包含预期变更。
2. 用户决定继续时，再冻结包含 builder 的新 Skill 标签、全新 remediation 和 Run ID；不得复用或修补 R3。
3. 新 Gate 仍按生成会话退出后依次执行写入审计、包内 validator 和冻结 checker，任一失败立即停止。

#### Files Changed / Commits

- `generate-sap/scripts/build_evidence_ledger.py`（added, uncommitted）
- `tests/test_generate_sap_ledger_builder.py`（added, uncommitted）
- `generate-sap/SKILL.md`（modified, uncommitted）
- `generate-sap/references/output-contract.md`（added/modified, uncommitted）
- `generate-sap/assets/generation-record-template.yaml`（modified, uncommitted）
- `generate-sap/evals/evals.json`（modified, uncommitted）
- `.validation-work/generate-sap/oncology-phase1-2/ledger-serialization-smoke/`（local ignored validation artifacts, added）
- `.skill-registry.json`、`SKILL_INDEX.md`、`docs/`（modified, uncommitted）

---

### R014 [13:02] [P0-generate-sap-output-contract] P2: R4 双上限控制失败与 v3 修复

#### Done

- 按用户确认建立并冻结 `REMEDIATION-04`、`GSAP-OC2-20260828`、`CTRL-LEDGER-01`、6 个全新 R4 Run ID、Markdown/Ledger 双通道和未修改的 `VAL-P2-v1` checker；全部使用简单标识符。
- 逐文件、逐字节确认 R4 输入与 R3 冻结输入一致，R4 Skill 与当前已验证包一致；控制脚本语法、writer Ledger 目标拒绝和 6 个空输出目录检查通过。
- 启动 `ONC001-R4-C01`。生成会话只读取 run-local Skill 与 Protocol；本地 `fitz` 成功读取 154 页文本，未使用网络、外部路径、全局 Skill或临时解析文件。
- Draft 首块 2,989 字符成功；第二块 3,238 字符超过 register/提示的 3,000 字符模型上限，但低于 helper 的 3,500 字符上限而被接受。控制者立即终止，保留 6,244 字节部分 Draft、events 和独立 violation report；其余 5 槽停止。
- 会话后证据显示 30 条完成命令、2 条成功 writer、最大命令 3,580 字符、0 Ledger builder、0 外部路径和 0 网络命令。冻结 auditor 返回 pass，确认它没有执行 payload 上限。
- 在正式 Gate 外建立 `write-channel-smoke-v3`。失败测试先证明旧 helper 接受 3,001 字符；候选 `WRITE-CHUNK-03` 只把硬上限改为 3,000，随后 3,000 接受、3,001 在创建文件前拒绝，2/2 测试与 Python 编译通过。

#### Issues / Blockers

- 直接根因是同一控制声明了 3,000 字符模型上限、3,500 字符 helper 上限和 6,000 字符命令审计上限，但只有后两者可执行；提示限制被违反时仍能写入并通过 frozen auditor。
- R4 已有输出，不能把候选 helper 回填、续跑或改写后计入同一 Gate；R4 状态为 `stopped-execution-control-failure`，package validator 和 objective checker 均未运行。
- v3 只证明边界执行正确，尚未建立新 remediation 或临床 Run ID；6/6 客观 Gate 继续未完成。

#### Next

1. 用户确认后以 `WRITE-CHUNK-03`、原 Ledger builder、全新 remediation 与 Run ID 建立空输出隔离包；R4 保持只读。
2. 新控制器只注册 helper 的 3,000 字符硬上限；提示可建议较短目标块，但不得定义第二个未执行合格阈值。
3. 仍按双通道审计、包内 validator、冻结 checker 顺序执行，任一失败立即停止。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-04/`（local ignored validation artifacts, added/modified）
- `.validation-work/generate-sap/oncology-phase1-2/write-channel-smoke-v3/`（local ignored validation artifacts, added）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`、`docs/dep/TASK_STATE.md`、`docs/dep/devlog/`（modified, uncommitted）

---

### R017 [16:52] [P0-generate-sap-output-contract] P2: R7 两槽通过与 Ledger auditor 误报修复

#### Done

- R7 `ONC001-R7-C01`、`ONC001-R7-P01` 均通过 Markdown/Ledger 双审计、包内 validator 和冻结 `VAL-P2-v1` checker，0 failed、0 warnings，并锁定三件套。
- `ONC001-R7-P02` 完成三件套后，冻结 Ledger auditor 把 `Get-Content .../build_evidence_ledger.py` 只读源码查看误判为非法 builder 调用 `item_66`；按冻结顺序停止，未运行 validator/checker 或 ONC004 三槽。
- Gate 外建立 `ledger-auditor-smoke-v1`；五类调用检测由冻结实现 3/5 提升为候选 5/5，候选对 R7 C01/P01/P02 events 只读回放均为 pass。
- 建立并冻结 `REMEDIATION-08`、六个全新 R8 Run ID 与 `LEDGER-AUDIT-02`。输入/Skill/非 auditor 控制逐文件逐字节一致，输入数 1/8/8/1/6/6、Skill 每槽 27、输出均为空。

#### Issues / Blockers

- 根因是 auditor 用文件名子串代表执行调用；只读源码命令包含同一文件名，产生误报。builder、生成内容和统计规则本身未失败。
- R7 正式结论保持失败；不得用候选回放补跑其 validator/checker，也不得复用 R7 输出进入 R8。

#### Next

1. 从 `ONC001-R8-C01` 开始执行六槽完整冻结顺序。
2. 每槽通过即锁定；任一正式失败立即保留并进入下一 Goal 根因循环。
3. 达到 6/6 后创建匿名评审包并恢复原 P2 入口。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-07/`（local ignored validation artifacts, modified status）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-08/`（local ignored validation artifacts, added）
- `.validation-work/generate-sap/oncology-phase1-2/ledger-auditor-smoke-v1/`（local ignored validation artifacts, added）
- `docs/dep/`（modified, uncommitted）

### R018 [10:25] [P0-generate-sap-output-contract] P2: R8 宿主中断与 R9 重新冻结

#### Done

- `ONC001-R8-C01` 依次通过 Markdown/Ledger 双审计、包内 validator 和冻结 `VAL-P2-v1` checker，0 failed、0 warnings，并锁定三件套。
- 恢复 `ONC001-R8-P01` 时确认其已完成 12 次 Draft writer、保留 17,597 bytes 部分 Draft，但无终止事件、Ledger、Open Questions/References 或任何后置 Gate 报告；末尾事件是 response stream disconnect。
- 进一步确认冻结的 CLI 0.150.0-alpha.8 构建已从宿主移除，而当前 bundled CLI 为 0.150.0-alpha.12.2。R8 P01 标记 `invalid-execution-interruption`，部分输出/events 原样保留，其余 R8 槽停止。
- 当前 bundled CLI 以冻结模型、推理配置、隔离参数和禁用项完成无工具 smoke 并返回 `BUILD_READY`。
- 建立并冻结 `REMEDIATION-09`、六个全新 R9 Run ID、`CTRL-CLI-05` 和 `CODEX-BUILD-D664`。六槽输入/Skill 与 R8 对应槽一致，非 CLI 控制一致，controller 仅可执行路径不同，语法通过且输出均为空。

#### Issues / Blockers

- 根因归类为宿主执行环境在输出后中断并替换冻结构建；没有证据表明 Skill、writer、Ledger builder、auditor、包内合同或 objective checker 失败。
- 因 P01 已产生输出，冻结策略不允许续写、同 Run ID 重启或使用“输出前替代”额度。R8 的正式结论保持 stopped。
- 当前无 blocker；CLI 版本变化已作为 R9 唯一批准变量明确登记，不能把 R8 C01 的通过结果带入 R9。

#### Next

1. 从 `ONC001-R9-C01` 开始顺序执行六槽完整冻结 Gate。
2. 每槽通过即锁定；任一正式失败立即保留并进入下一 Goal 根因循环。
3. 达到 6/6 后创建匿名评审包、恢复原 P2 入口并完成项目级校验。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-08/`（local ignored validation artifacts, status/evidence updated）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-09/`（local ignored validation artifacts, added/frozen）
- `.validation-work/generate-sap/oncology-phase1-2/cli-build-smoke-v2/`（local ignored validation artifacts, added）
- `docs/dep/`（modified, uncommitted）

---

### R015 [13:48] [P0-generate-sap-output-contract] P2: R5 Markdown target 审计误报与候选修复

#### Done

- 按冻结配置启动 `ONC001-R5-C01`。生成会话只使用 run-local Skill 和 Protocol；`pdftotext` 不可用后改用既有本地 `pypdf` 读取，没有安装依赖、写解析临时文件、访问网络、隐藏 SAP、旧输出或全局 Skill。
- 生成完整三件套：Draft 28,870 bytes、Ledger 32,823 bytes、Open Questions/References 8,008 bytes。16 条 Markdown writer 均成功，最大 payload 2,886 字符；63 条 Ledger add 与唯一 finalize 均成功，暂存文件已清除。
- 冻结 Markdown auditor 在 `item_48` 返回 `Ledger sent through Markdown writer`，控制器按顺序立即停止；Ledger auditor、包内 validator、冻结 objective checker 和剩余 5 槽均未运行，R5 原始输出与报告保持不变。
- 只读取证确认 `item_48` 的实际 `--target` 是 `sap-review-draft.md`；触发原因是 Draft 附录文字提到独立产物名 `generation-evidence-ledger.yaml`，而 auditor 对整条命令做文件名子串搜索。
- 在正式 Gate 外新增 `write-channel-audit-smoke-v4`。冻结 auditor 对 payload-only mention 与 actual Ledger target 两例为 1/2；最小候选改为解析 writer 调用后的 `--target`，两例 2/2 通过，并对 R5 events 只读回放为 pass。
- 更新 R5 register：首槽标为 `invalid-execution-control-failure`，其余 5 槽标为 `not-run-phase-stopped`；后验候选回放明确标记 `pass-not-gate-result`。

#### Issues / Blockers

- 直接根因是审计器混淆 payload 内容与目标参数：`LEDGER_TARGET in command` 无法区分“正文引用文件名”和“实际写入该文件”。这是 audit-control 缺陷，不是 writer 越权或生成内容失败。
- R5 已产生输出且冻结 auditor 返回非零，因此即使后验确认误报，也不能替换 auditor、补跑 validator/checker 或继续矩阵；正式 Phase 结果仍是 stopped。
- 本轮尚未证明三件套内容符合 package validator 或 `VAL-P2-v1`，也未建立新的 remediation；候选回放只能证明 target 检测根因与最小修复。

#### Next

1. 用户确认后，以 target-aware auditor、原 `WRITE-CHUNK-03`、Ledger builder、全新 remediation/Run ID 和空输出重新冻结；R5 保持只读。
2. 新冻结前保留两项相反合成测试，并增加 actual allowed target 的引号形式边界检查；不改变正文、统计规则、validator 或 objective checker。
3. 新首槽仍按 Markdown audit → Ledger audit → package validator → frozen checker 顺序执行；任一失败立即停止。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-05/`（local ignored validation artifacts, added/modified）
- `.validation-work/generate-sap/oncology-phase1-2/write-channel-audit-smoke-v4/`（local ignored validation artifacts, added）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`、`docs/dep/TASK_STATE.md`、`docs/dep/devlog/`（modified, uncommitted）

---

### R016 [14:20] [P0-generate-sap-output-contract] P2: R6 Markdown helper 拒绝与分块控制候选

#### Done

- 扩展 Markdown target 审计 smoke 至无引号、单双引号和 `--target=` 共 5 例；冻结 R5 auditor 为 3/5，target-aware 候选为 5/5，并再次通过 R5 events 只读回放。
- 建立并冻结 `REMEDIATION-06`、6 个全新 R6 Run ID、`CTRL-LEDGER-03` 与 `WRITE-AUDIT-02`。R6 只修改 auditor；输入、Skill、controller、writer、Ledger builder/auditor、validator、checker 和 denylist 与 R5 对应项逐字节一致，6 个输出为空。
- 启动 `ONC001-R6-C01`。生成者只读取 run-local Skill/Protocol；`pdftotext` 不可用后使用既有 `pypdf 6.4.1`，未安装依赖、写临时解析文件、访问网络、隐藏 SAP、旧输出或全局 Skill。
- 首个 Draft 块 2,941 字符成功；第二块合并 Section 5/6，实际 payload 3,605 字符，被 3,000 字符 helper 在追加前拒绝。输出保持 2,943 bytes，Ledger/OQ 未开始。
- 生成者因提示只对 Ledger add 明确“拒绝即停止”而启动拆块重试；控制者立即中断。重试 `item_29` 只有 started、无 completed，输出未变化。后验 auditor 正确报告 `item_27` failed，外部路径/网络命令为 0。
- Gate 外新增 v5 静态控制测试；R6 controller 对“每块最多一个顶层章节”和“Markdown 拒绝即停止”两项为 0/2，候选只添加这两条后为 2/2，PowerShell 语法通过。

#### Issues / Blockers

- 直接根因不是 helper，而是分块提示允许一个块跨多个顶层章节，且 Markdown 与 Ledger 的拒绝停止语义不一致。helper 正确保护了文件，但该槽已产生输出并包含失败 writer，必须停止。
- R6 不能用候选提示续跑或重试；剩余 5 槽、Ledger audit、package validator 和 objective checker 均未运行。
- 当前技术通道仍依赖模型遵守分块形态；下一 remediation 会保留机器硬限，并用单顶层章节规则降低首次提交超限风险，不把提示建议注册成第二个数值 Gate。

#### Next

1. 以 v5 候选 controller、R6 target-aware auditor、原 writer/Ledger builder 和全新 Run ID 冻结下一 remediation。
2. 逐字节确认除 controller 提示两行外无差异，运行 target 5/5、writer 边界 2/2、语法和空输出检查。
3. 首槽按完整冻结顺序执行；通过后自动锁定并继续下一槽，正式失败则原样停止并继续 Goal 根因流程。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-06/`（local ignored validation artifacts, added/modified）
- `.validation-work/generate-sap/oncology-phase1-2/write-channel-smoke-v5/`（local ignored validation artifacts, added）
- `docs/dep/plans/ongoing/P0-generate-sap-output-contract.md`（modified, uncommitted）
- `docs/dep/PLAN.md`、`docs/dep/TASK_STATE.md`、`docs/dep/devlog/`（modified, uncommitted）

---

### R019 [10:40] [P0-generate-sap-output-contract] P2: R9 writer 语法失败与 R10 模板简化

#### Done

- `ONC001-R9-C01` 前 7 条 Markdown writer 成功；`item_63` 将 `$OutputEncoding` 表达式多写一个 `]`，PowerShell 在 helper 启动前返回 ParserError。生成会话按冻结规则停止且未重试。
- Markdown audit 返回 fail；7,533 bytes 部分 Draft、events 和 audit 原样保留，Ledger、Open Questions/References、后续 Gate 与其余 R9 槽均未运行。
- Gate 外 `writer-boilerplate-smoke-v1` 复现同一 ParserError。删除两行重复编码赋值后，Markdown writer 与 Ledger builder 在 PowerShell 7 + `python -X utf8` 下均完成多语言逐字 round-trip。
- 建立并冻结 `REMEDIATION-10`、六个全新 R10 Run ID 与 `CTRL-BOILERPLATE-06`。controller 只简化两个固定命令模板；输入/Skill/非 controller 控制一致，精确 diff、语法和空输出检查通过。

#### Issues / Blockers

- 根因是模型逐命令转录冗余 shell 样板时发生单字符语法错误；失败发生在 helper 前，不是 helper、artifact schema 或 SAP 内容问题。
- R9 已产生输出并触发正式 Markdown audit failure，不能修正原命令、续写或补跑后续 Gate。
- 当前无 blocker；R10 的批准变化仅减少已由环境保证且经过双通道验证的重复编码初始化。

#### Next

1. 从 `ONC001-R10-C01` 开始顺序执行六槽完整冻结 Gate。
2. 每槽通过即锁定；任一正式失败立即保留并进入下一 Goal 根因循环。
3. 达到 6/6 后创建匿名评审包、恢复原 P2 入口并完成项目级校验。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-09/`（local ignored validation artifacts, status/evidence updated）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-10/`（local ignored validation artifacts, added/frozen）
- `.validation-work/generate-sap/oncology-phase1-2/writer-boilerplate-smoke-v1/`（local ignored validation artifacts, added）
- `docs/dep/`（modified, uncommitted）

---

### R020 [11:14] [P0-generate-sap-output-contract] P2: R10 前台中断与 R11 detached launcher

#### Done

- `ONC001-R10-C01` 连续完成 16 条 Markdown writer、进入 Section 12 并保留 25,726 bytes Draft，证明 R10 命令模板越过 R9 失败点。
- 交互 turn 中断后进程句柄消失；events 无终止事件、无 failed writer，Ledger/OQ 和后置 Gate 均未开始。R10 标记 `invalid-execution-interruption`，部分输出/events 原样保留，其余槽停止。
- Gate 外 `background-launcher-smoke-v1` 证明隐藏后台子进程在前台调用结束后继续运行；两层 launcher/monitor 候选进一步独立等待 dummy controller 并写出 `controller_exit_code: 0`。
- 建立并冻结 `REMEDIATION-11`、六个全新 R11 Run ID、`DETACHED-LAUNCH-01` 和 `DETACHED-MONITOR-01`。输入/Skill/生成控制器与 R10 一致，新增启动层语法、后台生存、终止记录和空输出检查通过。

#### Issues / Blockers

- 根因是长控制器进程绑定当前交互 turn；界面中断会在内容已写入后终止它。这与 SAP Skill、writer、builder 和四道 Gate 无关。
- R10 已有部分输出，不能续写或同 ID 重启；R10 正式结论保持 stopped。
- 当前无 blocker；R11 后台层只负责进程生命周期和终止证据，正式 Gate 仍由未修改控制器执行。

#### Next

1. 通过 detached launcher 启动 `ONC001-R11-C01`，轮询其 `background-exit.yaml` 而非持有前台进程。
2. 每槽通过即锁定并后台启动下一槽；任一正式失败立即保留并进入下一 Goal 根因循环。
3. 达到 6/6 后创建匿名评审包、恢复原 P2 入口并完成项目级校验。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-10/`（local ignored validation artifacts, status/evidence updated）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-11/`（local ignored validation artifacts, added/frozen）
- `.validation-work/generate-sap/oncology-phase1-2/background-launcher-smoke-v1/`（local ignored validation artifacts, added）
- `docs/dep/`（modified, uncommitted）

---

### R021 [11:21] [P0-generate-sap-output-contract] P2: R11 运行时失效与 R12 重钉

#### Done

- detached monitor 正常启动 `ONC001-R11-C01` 并写出终止证据；控制器在生成前因冻结 `CODEX-BUILD-D664` 路径不存在而退出。输出文件数为 0，正式四道 Gate 未开始，R11 原样停止。
- Gate 外 `CLI-BUILD-SMOKE-03` 使用当前 `CODEX-BUILD-B993`、CLI `0.151.0-alpha.7.2` 和正式模型/隔离/禁网参数完成真实 roundtrip，退出码 0、终止事件完整。
- 建立并冻结 `REMEDIATION-12` 与六个新 Run ID。输入/Skill 与 R11 一致，生成控制器除可执行路径外一致，输出为空，PowerShell 语法通过。

#### Issues / Blockers

- 根因是桌面更新清理了 build-specific 可执行目录，不是 Skill、生成内容、写入器或四道 Gate 失败。
- R11 同 Run ID 不重启；其 launch、exit、stderr 和失败报告继续保留。
- 当前无 blocker；R12 的唯一批准变化是运行时路径重钉。

#### Next

1. 通过 detached launcher 启动 `ONC001-R12-C01`。
2. 每槽以后台终止证据和四道冻结 Gate 判定，通过即锁定并顺序启动下一槽。
3. 达到 6/6 后创建匿名评审包、恢复原 P2 入口并完成项目级校验。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-11/`（local ignored validation artifacts, status/evidence updated）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-12/`（local ignored validation artifacts, added/frozen）
- `.validation-work/generate-sap/oncology-phase1-2/cli-build-smoke-v3/`（local ignored validation artifacts, added）
- `docs/dep/`（modified, uncommitted）

---

### R022 [11:59] [P0-generate-sap-output-contract] P2: R12 首槽四 Gate 通过

#### Done

- `ONC001-R12-C01` detached 运行完整结束，控制器退出码 0、monitor 无故障，三件套齐全且 Ledger staging 已清除。
- Markdown audit 31 次 writer 全通过；Ledger audit 68 add + 1 finalize 全通过；包 validator PASS；冻结 `VAL-P2-v1` 9/9 pass、0 warning。
- 创建锁定记录并启动 `ONC001-R12-P01`；R12 矩阵当前 1/6 locked。

#### Issues / Blockers

- 无新的正式 Gate 失败；首槽证明 detached 生命周期、受控 Markdown writer 和确定性 Ledger builder 可端到端完成。
- 当前无 blocker；第二槽在相同冻结控制下后台运行。

#### Next

1. 等待并判定 `ONC001-R12-P01` 四道 Gate。
2. 通过则锁定并顺序启动 P02 和 CASE-ONC-004 三槽；失败则原样停止并进入新 remediation。
3. 达到 6/6 后创建匿名评审包并恢复原 P2 入口。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-12/`（local ignored validation artifacts, outputs/status/lock added）
- `docs/dep/`（modified, uncommitted）

---

### R025 [14:12] [P0-generate-sap-output-contract] P2: R12 Ledger 命令失败与 R13 冻结

#### Done

- `ONC004-R12-C01` 完成三件套并通过 Markdown audit；Ledger audit 检出 `item_29` 实际执行 `build_evidence_ledger.py --help`，按冻结 Gate 返回 fail。validator/checker 与余下两槽未运行，R12 全部现场原样保留。
- Gate 外建立 `LEDGER-PROMPT-SMOKE-01`。首次简化提示因遗漏正式隔离条款而在 Ledger 写入前中止；补齐既有全局 Skill/外部路径禁令后，真实 agent 完成 21 add + 1 finalize，Ledger auditor pass，unexpected/failed/external/network 均为 0。
- 建立并冻结 `REMEDIATION-13` 与六个新 Run ID；唯一批准增量是明确 builder 禁止 `--help`、裸调用和 inspection/testing。六槽输入与 R12 对应槽一致，计数 1/8/8/1/6/6，Skill 均为 27 个文件，输出均为空。
- 控制器逐行验证只新增一条 Ledger 指令；其余 auditor、writer、builder、validator、checker、denylist、launcher/monitor 与运行时保持不变，运行控制同步、PowerShell/YAML 语法和 B993 可用性检查通过。

#### Issues / Blockers

- R12 根因是提示没有显式封闭 builder 的可执行命令集合；auditor 行为正确，不修改 auditor 或生成产物。
- 无当前 blocker；R13 需从 0/6 重新执行，R12 三个通过槽不计入新矩阵。

#### Next

1. detached 启动并判定 `ONC001-R13-C01` 四道 Gate。
2. 每槽通过后锁定并顺序启动余下五槽；失败则原样停止并建立新 remediation。
3. 6/6 后创建匿名评审包、恢复原 P2 入口并执行项目级校验。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-12/`（local ignored validation artifacts, failure/status preserved）
- `.validation-work/generate-sap/oncology-phase1-2/ledger-builder-help-smoke-v1/`（local ignored Gate-external evidence, added）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-13/`（local ignored frozen validation package, added）
- `docs/dep/`（modified, uncommitted）

---

### R024 [13:14] [P0-generate-sap-output-contract] P2: CASE-ONC-001 三槽通过

#### Done

- `ONC001-R12-P02` 独立完成三件套；Markdown audit、Ledger audit、package validator 和冻结 `VAL-P2-v1` 全通过，0 warning。
- CASE-ONC-001 的 C01/P01/P02 三槽全部锁定；两次 precedent 运行均包含 3 条 reference 且 target-leakage 检查通过。
- 启动 `ONC004-R12-C01`；R12 矩阵达到 3/6 locked。

#### Issues / Blockers

- P02 曾发生一次可恢复的 sampling stream retry，CLI 在同一会话中恢复并最终完整通过；无输出命令失败。
- 当前无 blocker，第四槽后台运行中。

#### Next

1. 判定 `ONC004-R12-C01` 四道 Gate。
2. 顺序执行并锁定 `ONC004-R12-P01/P02`。
3. 达到 6/6 后创建匿名评审包、恢复原 P2 入口并做项目级校验。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-12/`（local ignored validation artifacts, outputs/status/lock added）
- `docs/dep/`（modified, uncommitted）

---

### R023 [12:38] [P0-generate-sap-output-contract] P2: R12 precedent 首次运行通过

#### Done

- `ONC001-R12-P01` 完成三件套并通过 Markdown audit、Ledger audit、package validator 和冻结 `VAL-P2-v1`。
- Ledger 含 29 content units、16 open questions、3 precedent references、10 consistency findings 和 1 search summary；target-leakage 检查通过，0 warning。
- 该槽已锁定并启动独立复现槽 `ONC001-R12-P02`；矩阵进度 2/6 locked。

#### Issues / Blockers

- 无新失败；冻结 precedent bundle 的来源与限制可被完整序列化且未触发目标泄漏。
- 当前无 blocker，第三槽后台运行中。

#### Next

1. 判定并锁定 `ONC001-R12-P02`。
2. 顺序执行 CASE-ONC-004 的 C01/P01/P02 三槽。
3. 达到 6/6 后创建匿名评审包并恢复原 P2 入口。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-12/`（local ignored validation artifacts, outputs/status/lock added）
- `docs/dep/`（modified, uncommitted）

---

### R026 [14:15] [P0-generate-sap-output-contract] P2: R13 启动检查点

#### Done

- 确认 R13 六槽冻结包、控制同步、文档状态与 `R025` 登记完成，固定 B993 在启动前仍可用。
- 记录既有 active batch 的物理轮次顺序含早前的 R024/R023 倒置；本轮不改写历史条目，仅从物理文件末尾继续追加。

#### Issues / Blockers

- 无 blocker；下一动作是 detached 启动 R13 首槽。

#### Next

1. 启动并判定 `ONC001-R13-C01`。
2. 按冻结矩阵自主推进至 6/6 或首个失败。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-13/`（local ignored frozen validation package, ready）
- `docs/dep/`（modified, uncommitted）

---

### R027 [14:33] [P0-generate-sap-output-contract] P2: R13 capacity 失败与 R14 冻结

#### Done

- `ONC001-R13-C01` 在 7 次成功 writer、8,373 bytes 部分 Draft 后收到后端 model capacity 错误并 `turn.failed`；monitor 正常记录退出码 1，Ledger 与四道 Gate 均未开始。
- R13 同 Run ID 与余下五槽停止，输出/events 原样保留。Gate 外同一 B993、`gpt-5.6-sol/high`、ephemeral/禁网 smoke 随后返回 `CAPACITY_READY`、`turn.completed`、退出码 0。
- 建立并冻结 `REMEDIATION-14` 与六个新 Run ID，无功能性增量。R13 控制逐文件一致；六槽输入/Skill 一致、计数 1/8/8/1/6/6 与 27，输出为空，控制同步、PowerShell/YAML 与 B993 检查通过。

#### Issues / Blockers

- R13 根因是瞬时模型容量，不修改 Skill、提示、统计规则、writer、builder、auditor、validator 或 checker。
- 无当前 blocker；R14 从 0/6 重新执行。

#### Next

1. detached 启动并判定 `ONC001-R14-C01`。
2. 通过后锁定并顺序推进余下五槽；失败则保留现场并继续根因循环。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-13/`（local ignored validation artifacts, failure preserved）
- `.validation-work/generate-sap/oncology-phase1-2/cli-capacity-smoke-v1/`（local ignored Gate-external evidence, added）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-14/`（local ignored frozen validation package, added）
- `docs/dep/`（modified, uncommitted）

---

### R028 [15:26] [P0-generate-sap-output-contract] P2: R14 执行层失败与 R15 冻结

#### Done

- `ONC001-R14-C01` 完成两件 Markdown artifact、28 次 writer 和 21 次 Ledger add；第 22 次 `item_87` 在命令层以 failed/null exit/no output 停止，Markdown audit pass、Ledger audit fail，后续 Gate 与其余五槽未运行。
- R14 失败输出、staging、events 和报告原样保留，同 Run ID 未重试。Gate 外相同 `SAP-13-002` add 在本地直接重放与同一 B993 CLI 命令工具重放均通过；有效 CLI attempt 返回 `STAGED content_unit`、退出码 0 和完整 `turn.completed`。
- 将 R14 归类为瞬时命令执行层失败；建立并冻结无功能增量的 `REMEDIATION-15` 与六个新 Run ID。输入/Skill/控制和 R14 内容一致，计数、空输出、PowerShell/YAML、控制同步与 B993 可用性验证均通过。

#### Issues / Blockers

- 重放 attempt-01 因 here-string 终止符缩进而无效，attempt-02 在命令执行前遭模型 capacity；两者均不用于判定 builder 或 payload。
- 当前无 blocker；R15 从 0/6 开始正式执行。

#### Next

1. detached 启动并判定 `ONC001-R15-C01` 的四道冻结 Gate。
2. 通过后锁定并顺序推进余下五槽；失败则原样保留并进入新的 Gate 外根因循环。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-14/`（local ignored validation artifacts, failure preserved）
- `.validation-work/generate-sap/oncology-phase1-2/ledger-command-rejection-smoke-v1/`（local ignored Gate-external evidence, added）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-15/`（local ignored frozen validation package, added）
- `docs/dep/`（modified, uncommitted）

---

### R029 [16:04] [P0-generate-sap-output-contract] P2: R15 首槽四道 Gate 通过

#### Done

- `ONC001-R15-C01` detached 完整结束，monitor 记录退出码 0、无 monitor failure；三件输出齐全且暂存 Ledger 已清除。
- Markdown audit 以 27 次 writer 通过；Ledger audit 以 63 add + 1 finalize 通过，无 unexpected/failed/external/network 命令。
- 包内 validator 和冻结 `VAL-P2-v1` checker 均通过，9/9 checks、0 warning；创建锁文件并将 R15 进度登记为 1/6 locked。

#### Issues / Blockers

- 无新失败；该槽已越过 R14 第 22 次 add 历史失败点，支持瞬时 host-execution 分类。
- 当前无 blocker，下一槽为 `ONC001-R15-P01`。

#### Next

1. detached 启动并判定 `ONC001-R15-P01`。
2. 通过后锁定并继续 R15 余下四槽；任一失败则原样保留并停止 remediation。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-15/`（local ignored validation artifacts, first lock added）
- `docs/dep/`（modified, uncommitted）

---

### R030 [16:10] [P0-generate-sap-output-contract] P2: P01 输出前 capacity 与替代冻结

#### Done

- `ONC001-R15-P01` 在 writer/builder 和任何 artifact 产生前收到模型 capacity，具有明确 `turn.failed`；detached monitor 记录退出码 1、无 monitor failure，输出目录为 0 文件。
- 按预注册的每槽最多一次输出前替代规则，将 P01 标记为 invalid-execution-failure 并保留全部事件，不计入 6/6。
- 建立 `ONC001-R15-P03` 替代 Run ID；8 个输入、27 个 Skill 文件、10 个 control 与 P01 内容一致，输出为空，PowerShell/YAML 与 B993 检查通过，无功能增量。

#### Issues / Blockers

- 根因是生成开始前的瞬时模型 capacity，不是 Skill、输出合同或冻结 Gate 失败。
- 当前无 blocker；P03 已消耗该槽唯一替代额度，再次失败将停止 R15。

#### Next

1. detached 启动并判定 `ONC001-R15-P03`。
2. 通过后锁定该目标槽并继续 P02；失败则原样保留并停止 remediation。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-15/`（local ignored replacement package and evidence, added）
- `docs/dep/`（modified, uncommitted）

---

### R031 [16:20] [P0-generate-sap-output-contract] P2: P03 capacity 与 R15 停止

#### Done

- Gate 外 `CLI-CAPACITY-SMOKE-02` 先返回 `CAPACITY_READY`、完整 `turn.completed` 和退出码 0；随后启动唯一替代 `ONC001-R15-P03`。
- P03 完成 10 次 run-local 辅助读取后，在零输出状态再次因模型 capacity `turn.failed`；monitor 记录退出码 1、无 monitor failure。
- P03 的 `item_27` 因本机无 `pdftotext` 退出 1，但它不是冻结 writer/builder，且正式终止原因为后续模型 capacity。P03 与 P01 现场均保留，R15 在 1/6 locked 处停止，其余槽未运行。

#### Issues / Blockers

- P01→P03 已用尽该槽唯一的输出前替代额度；R15 不得继续 P02 或再启动 P03。
- 当前无用户 blocker；需在 Gate 外复核 capacity 恢复，并客观判断是否需要约束 PDF 读取工具后再冻结下一 remediation。

#### Next

1. Gate 外运行同模型 capacity 恢复 smoke，并验证 pypdf/pdftotext 环境事实。
2. 只批准有失败证据支持的最小增量，或以无功能增量冻结下一 remediation；从 0/6 新 Run ID 重启。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-15/`（local ignored failure evidence and stopped status, added）
- `.validation-work/generate-sap/oncology-phase1-2/cli-capacity-smoke-v2/`（local ignored Gate-external evidence, added）
- `docs/dep/`（modified, uncommitted）

---

### R032 [16:25] [P0-generate-sap-output-contract] P2: capacity 复核与 R16 冻结

#### Done

- P03 终止后，Gate 外 `CLI-CAPACITY-SMOKE-03` 以相同 B993、模型、推理和隔离配置返回 `CAPACITY_READY`、完整终止态和退出码 0。
- 环境复核为 `pdftotext` unavailable、`pypdf` available；结合 R15 C01 在同控制下完成，未把 P03 的辅助读取失败误归因为终止根因，也未修改 PDF 或 Skill 规则。
- 建立并冻结无功能增量的 `REMEDIATION-16` 与六个新 Run ID。输入 1/8/8/1/6/6、每槽 Skill 27/control 10/output 0；内容一致、root/run control 同步、PowerShell/YAML 与 B993 检查通过。

#### Issues / Blockers

- 短 capacity smoke 只能证明启动时模型可用，不能保证长会话期间无容量变化；这继续作为 host-execution 风险记录，而不是放宽模型配置。
- 当前无 blocker；R16 从 0/6 独立重启，R15 的通过结果不带入。

#### Next

1. detached 启动并判定 `ONC001-R16-C01`。
2. 通过后锁定并顺序推进余下五槽；失败则保留现场并继续根因循环。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/cli-capacity-smoke-v3/`（local ignored Gate-external evidence, added）
- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored frozen validation package, added）
- `docs/dep/`（modified, uncommitted）

---

### R033 [16:35] [P0-generate-sap-output-contract] P2: C01 capacity 与多轮 soak 后启动 C02

#### Done

- `ONC001-R16-C01` 在一次 run-local 枚举后于零输出状态因模型 capacity `turn.failed`；monitor 记录退出码 1、无 monitor failure，现场原样保留。
- 冻结唯一替代 `ONC001-R16-C02`；1 input、27 Skill、10 control 与 C01 内容一致，0 output，PowerShell/YAML 通过。
- Gate 外 `CLI-CAPACITY-SOAK-01` 连续完成 10/10 个独立命令边界；一次 stream disconnect 由同一会话恢复，最终 `CAPACITY_SOAK_READY`、`turn.completed`、exit 0。随后 detached 启动 C02。

#### Issues / Blockers

- R16 control 槽替代额度已耗尽；C02 若终止，R16 必须停止。
- 当前无 blocker；C02 后台运行中。

#### Next

1. 判定 `ONC001-R16-C02` 的终止态与四道 Gate。
2. 通过后锁定并继续 P01；失败则保留现场并进入下一 remediation 根因循环。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored replacement package and evidence, added）
- `.validation-work/generate-sap/oncology-phase1-2/cli-capacity-soak-v1/`（local ignored Gate-external evidence, added）
- `docs/dep/`（modified, uncommitted）

---

### R034 [17:22] [P0-generate-sap-output-contract] P2: R16 替代 C02 四道 Gate 通过

#### Done

- `ONC001-R16-C02` detached 完整结束，monitor 记录退出码 0、无 monitor failure；三件输出齐全且 staging 已清除。
- Markdown audit 以 30 writer 通过；Ledger audit 以 64 add + 1 finalize 通过，无 unexpected/failed/external/network 命令。
- 包内 validator 与冻结 `VAL-P2-v1` checker 均通过，9/9、0 warning；C02 作为 control 目标槽有效替代已锁定，R16 达到 1/6。

#### Issues / Blockers

- 无新失败；长会话完整完成进一步支持 capacity 为瞬时宿主问题。
- 当前无 blocker，下一槽为 `ONC001-R16-P01`。

#### Next

1. detached 启动并判定 `ONC001-R16-P01`。
2. 通过后锁定并继续 P02；失败则按冻结规则处理。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored outputs/status/lock added）
- `docs/dep/`（modified, uncommitted）

---

### R035 [17:38] [P0-generate-sap-output-contract] P2: 验证治理收敛为 L0/L1/L2

#### Done

- 完整复核用户指定的《规划SAP验证体系》结论，并与 R12-R16 证据对照：capacity、CLI 构建清理、缺少 `pdftotext`、auditor 误报和命令执行拒绝均不能直接证明 `generate-sap` 临床质量失败。
- 冻结外层 `SAP-VALIDATION-GOVERNANCE-V2`：L0 技术健康只验证并冻结一次；L1 对每个有效产物执行三件套和冻结合同检查；L2 评估临床统计质量、追溯性和稳定性。
- 正式样本从每案例三槽收敛为两个案例 × protocol-only/precedent-assisted 四个主样本，并预注册 `ONC001` precedent 的一次重复，总计 5 个有效样本。
- 将基础设施异常定义为 `invalid-run`，排除出 Skill 质量分母并只替换受影响样本；产品内容、证据、统计逻辑或合同失败才进入 Skill 缺陷分析。R16 冻结控制与当前 P01 均未修改或中断。

#### Issues / Blockers

- 旧 R16 run register 仍准确记录其原始冻结执行政策；新的治理文件只调整跨运行归因和样本汇总，不能被用于改写既有运行证据。
- 当前无 blocker；P01 已开始写入 SAP Draft，继续等待自然终止。

#### Next

1. 判定 `ONC001-R16-P01`，通过后作为第二个主样本锁定；基础设施异常只局部替换。
2. 收集 ONC004 protocol-only、ONC004 precedent 和 ONC001 precedent repeat，随后执行匿名 L2 质量评审与跨 case 比较。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/validation-governance-v2.yaml`（local ignored governance evidence, added）
- `docs/dep/`（modified, uncommitted）

---

### R036 [17:44] [P0-generate-sap-output-contract] P2: 分离六槽 L1 与 4+1 L2 口径

#### Done

- 对照持续 Goal 的明确完成条件复核 R035：临床质量样本可收敛为 4+1，但输出契约修复里程碑仍要求原六个目标槽完成 Markdown audit、Ledger audit、package validator 和冻结 `VAL-P2-v1`。
- 更新外层治理为两条证据链：L1 保留 R16 六槽并要求 6/6 locked；L2 从六个锁定输出中选取四个主样本和一个 `ONC001` precedent repeat。
- 基础设施异常仍只作为 invalid-run 局部替换，不重置已锁定槽；该归因规则不减少六个目标槽，也不改变任何冻结运行控制。
- 权威检查确认 P01 monitor PID 16876 存活且响应，Draft 已持续写入；未中断或修改当前运行。

#### Issues / Blockers

- P01 Draft 事件显示源文本中存在字符显示异常，当前运行不得现场修改；待运行终止后由冻结 Gate 和后续 L2 质量评审客观判定影响。
- 当前无 blocker。

#### Next

1. 等待 P01 自然终止并执行四道 L1 Gate。
2. 通过则锁定并继续 P02；基础设施异常只替换本槽，产品失败进入 Skill 缺陷分析。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/validation-governance-v2.yaml`（local ignored governance evidence, modified）
- `docs/dep/`（modified, uncommitted）

---

### R037 [18:14] [P0-generate-sap-output-contract] P2: P01 四道 Gate 通过并启动 P02

#### Done

- `ONC001-R16-P01` detached 完整结束；`background-exit.yaml` 记录 controller exit 0、monitor failure none，三件输出齐全且 staging 已清除。
- Markdown audit 以 28 writer pass；Ledger audit 以 60 add + 1 finalize pass，记录构成为 18 section status、18 content unit、9 open question、3 reference、10 consistency finding、1 document、1 search summary。
- 包内 validator 返回 PASS；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，`valid_for_blinded_statistical_review: true`。创建 P01 锁并将 R16 更新为 2/6 locked。
- 验证 P02 为 0 output、8 input、27 Skill、10 control 且无既有 launch/exit 证据后 detached 启动；monitor PID 9336，进程已确认存活并响应。

#### Issues / Blockers

- controller 事件日志的 PowerShell 聚合输出存在终端显示转码，但实际 Markdown 已按 UTF-8 解码验证且无替换字符或 mojibake 字符；不是产物失败。
- 当前无 blocker。

#### Next

1. 判定 `ONC001-R16-P02` 终止态及四道 Gate。
2. 通过后锁定并启动 `ONC004-R16-C01`；基础设施异常只局部替换。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored P01 evidence/lock and P02 launch evidence, modified）
- `docs/dep/`（modified, uncommitted）

---

### R038 [19:08] [P0-generate-sap-output-contract] P2: P02 四道 Gate 通过并锁定

#### Done

- `ONC001-R16-P02` detached 完整结束；`background-exit.yaml` 记录 controller exit 0、monitor failure none，三件输出齐全且 Ledger staging 已清除。
- Markdown audit 以 30 writer pass；Ledger audit 以 76 add + 1 finalize pass，记录构成为 18 section status、25 content unit、18 open question、3 reference、10 consistency finding、1 document、1 search summary。
- 包内 validator 返回 PASS；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，`valid_for_blinded_statistical_review: true`。创建 P02 锁并将 R16 更新为 3/6 locked。
- 整个运行中出现一次同会话可恢复的 response stream disconnect；CLI 自动恢复且未产生 writer/builder 失败，不计作基础设施 invalid-run。

#### Issues / Blockers

- 当前无 blocker；CASE-ONC-001 三个目标槽已全部锁定。

#### Next

1. 在空输出和冻结输入/Skill/control 验证后 detached 启动 `ONC004-R16-C01`。
2. 判定其终态与四道 L1 Gate；通过后继续 ONC004 P01/P02。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored P02 evidence/lock and register, modified）
- `docs/dep/`（modified, uncommitted）

---

### R039 [19:12] [P0-generate-sap-output-contract] P2: 启动 ONC004 protocol-only 槽

#### Done

- 对 `ONC004-R16-C01` 执行冻结 preflight：0 output、无既有 launch/exit/events，1 input、27 Skill、10 control，全部符合 run register。
- 使用冻结 detached launcher 启动该槽；`background-launch.yaml` 记录 monitor PID 16344，进程已确认存活并响应。
- 将根 run register 与计划状态更新为 C01 running；CASE-ONC-001 三个锁保持不变，矩阵仍为 3/6 locked。

#### Issues / Blockers

- 当前无 blocker；C01 尚未产生终态，不能提前执行 Gate 或锁定。

#### Next

1. 观察 C01 的产物单调增长与终态，不读取隐藏参考 SAP。
2. 终态后按固定顺序读取 Markdown audit、Ledger audit、package validator 与 `VAL-P2-v1`。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored C01 launch evidence and register, modified）
- `docs/dep/`（modified, uncommitted）

---

### R040 [20:03] [P0-generate-sap-output-contract] P2: ONC004 C01 通过并启动 P01

#### Done

- `ONC004-R16-C01` detached 完整结束；controller exit 0、monitor failure none，三件输出齐全且 staging 已清除。
- Markdown audit 以 29 writer pass；Ledger audit 以 67 add + 1 finalize pass，记录构成为 18 section status、24 content unit、13 open question、10 consistency finding、1 document、1 search summary。
- 包内 validator 返回 PASS；冻结 `VAL-P2-v1` 为 9/9 pass、0 failed checks、0 warnings，`valid_for_blinded_statistical_review: true`。创建 C01 锁并将 R16 更新为 4/6 locked。
- 对 `ONC004-R16-P01` 执行冻结 preflight：0 output、无既有 launch/exit/events，6 input、27 Skill、10 control；随后 detached 启动，monitor PID 2992 已确认存活并响应。

#### Issues / Blockers

- 当前无 blocker；P01 尚未产生终态，不能提前执行 Gate 或锁定。

#### Next

1. 判定 `ONC004-R16-P01` 终态及四道 L1 Gate。
2. 通过后锁定并启动最后一个 L1 槽 `ONC004-R16-P02`。

#### Files Changed / Commits

- `.validation-work/generate-sap/oncology-phase1-2/remediation-16/`（local ignored C01 evidence/lock and P01 launch evidence, modified）
- `docs/dep/`（modified, uncommitted）
