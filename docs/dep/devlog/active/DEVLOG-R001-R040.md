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
