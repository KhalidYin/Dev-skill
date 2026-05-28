# Review protocol

When the user issues an audit/review/inspection command, follow a two-tier approach: **Quick Review** first, then offer **Full Report**.

The review process cross-checks four sources:
- **Dev log** (`docs/dep/DEVLOG-RXXX-RXXX.md`) — what was claimed as done
- **Git history** (`git log --oneline --since=<date>`) — what was actually committed
- **Main docs** (`docs/main/`) — what the architecture/spec says should exist
- **Actual code** — what is really there

## Scope determination

Review scope is determined by the user's request. If unspecified, default to: **all entries since the last review**.

| User says | Scope |
|-----------|-------|
| "review the codebase" | All rounds since last review (or last 10 rounds if no prior review) |
| "review last week" | DEVLOG rounds from the past 7 days (identify via date headers) |
| "review the auth module" | Rounds that touch auth-related files, regardless of date |
| "review R020 to R035" | Rounds R020–R035, may cross batch boundaries |
| "review everything" | All DEVLOG rounds across all batches |

When scope crosses batch boundaries, read both the active batch and the relevant sealed batch — only the round sections within scope.

## Quick Review (default)

Always start here. Read dev log rounds within scope. Run `git log --oneline --since=<scope start date>` to cross-check claims against actual commits. Output 3-5 bullet points directly in the response — no file is written.

Format:

```
## Quick Review

- [finding 1: what was checked, what was found — reference dev log round RXXX if relevant]
- [finding 2: issue or gap identified vs dev log claims]
- [finding 3: risk or concern — dev log items still open, blockers, etc.]
- **Plan sync status**: N 个阻断/P0 issues 未同步到 PLAN.md（最长积压 X 轮）/ 已同步；Quick Review 只报告状态，不写文件
- [summary verdict: OK / needs attention / blocking]

需要我生成完整的审查报告到 `docs/dep/REVIEWS.md` 吗？
```

Quick Review covers:
- Critical issues (bugs, security, data loss)
- Dev log claims not backed by git commits
- Missing pieces vs dev log claims and main docs
- Dev log items still marked as open/blocked
- Obvious deviations from conventions
- A one-line verdict

## Full Report (on demand)

Only generate when the user confirms (after Quick Review prompt) or explicitly asks for "完整报告", "生成报告", "full report".

### Format

`REVIEWS.md` is a **single rolling file**, append-only. Each review is a numbered section. Naming follows actual review sequence (第 1 次 review = Review 1).

Only include sections that have content — skip empty sections entirely, do not generate empty tables.

```markdown
# Review Reports

---

## Review 1 [2026-05-04]

### Scope
<!-- What was reviewed: files, features, modules, round range -->

### Dev Logs Reviewed

| Round | Claim | Verified |
|-------|-------|----------|
| R007 | [what dev log says was done] | ✅ / ⚠️ / ❌ — [evidence] |

### Findings

#### Issues
<!-- Only include if issues found -->

| # | Severity | File/Area | Description | Status |
|---|----------|-----------|-------------|--------|
| 1 | high/medium/low | path:line | ... | open/fixed/deferred |

#### Unimplemented / Incomplete
<!-- Only include if unimplemented items found -->

| # | Reference | Description | Next step |
|---|-----------|-------------|-----------|
| 1 | R008 / spec ref | ... | ... |

#### Deviations
<!-- Only include if deviations found -->

| # | Expected | Actual | Impact |
|---|----------|--------|--------|
| 1 | ... | ... | ... |

### Next Actions
<!-- Always include — concrete, prioritized -->

1. ...

### Status: in-progress / resolved / deferred

---

## Review 2 [2026-05-05]
- ...
```

### Rules

- **Append-only** — never delete or edit past reviews
- **Only include sections with content** — no empty tables or placeholder sections
- **Review header** — `## Review N [YYYY-MM-DD]`, N is the sequential review count (1, 2, 3, ...)
- **Dev Log reference** — use global round numbers (R007), not date-based references
- **Status tracking** — `in-progress` (issues open), `resolved` (all closed), `deferred` (some deferred)
- **Status is historical** — do not modify past reviews' status. If previously open issues are now resolved, note the resolution in the new review's findings
- Link to related prior reviews by review number reference

### Plan Sync (mandatory, after Full Report)

Review 报告写入 `REVIEWS.md` 后，必须立即执行以下检查，确保 Review 发现不会与 `PLAN.md` 断裂：

1. **阻断/P0 同步**：将本轮 Review 中 `Status=open` 的阻断 issue 写入对应位置：
   - 属于现有子计划 → 写入该子计划 `docs/dep/plans/P<phase>-<name>.md` 的 execution findings 表。
   - 不属于任何子计划 → 创建独立 `docs/dep/plans/P0-<desc>.md`，PLAN.md 只保留子计划指针。
2. **非阻断技术债务同步**：将本轮 Review 中非阻断的技术债务写入或创建 `docs/dep/plans/P0-tech-debt.md`。该文件是单一技术债务 track，内部用 Phase 或条目区分来源和处理批次。
3. **老化检测**：读取 `P0-tech-debt.md` 和所有 open 的 `P0-*.md`。如果 open issues 积压超过 3 个 DEVLOG 轮次未被标记为 resolved → 在本轮 Review Findings 中标记为 `aging`。
4. **状态刷新**：
   - 已 resolved 的 issues → 从 PLAN.md 技术债务 track 移除，记入"最近完成"
   - 仍 open 的 issues → 保留在 PLAN.md，更新积压天数

### Cross-sub-plan finding classification

当 Review 发现不属于任何现有子计划时，按以下规则归属：

| 发现类型 | 归属 |
|----------|------|
| 阻断型 bug / 安全 / 数据完整性问题 | 创建独立 `docs/dep/plans/P0-<desc>.md`，PLAN.md 最高优先级 |
| 非阻断技术债务（Bug、性能、维护性） | 创建或更新 `docs/dep/plans/P0-tech-debt.md`，PLAN.md 只保留一行指针 |
| 新功能需求 | 按 `references/planning-protocol.md` 的“执行中插入新计划”流程创建新子计划 |
| 架构改进 | 归入最相关的现有子计划，或创建新子计划 |

所有 Review 生成的子计划都遵循 `templates/sub-plan.md.template`。`P0-tech-debt.md` 的 frontmatter 使用 `phase_index: 0`，`priority` 低于独立阻断型 `P0-<desc>.md`。PLAN.md 仪表盘只保留指针，不内联详细任务表。

### Layered reading for REVIEWS.md

To minimize token consumption when reading past reviews:

| Reviews to read | How |
|----------------|-----|
| Last 3 reviews | Full read — complete sections |
| Older reviews | Status line only — read just the `### Status:` line |
| User requests specific review | Full read of that review section |

## When NOT to generate

- Simple code change or bug fix (not a review)
- One-line answer about code behavior
- Purely writing new code (no review implied)
