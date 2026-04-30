# Document structure

This is the authoritative reference for all document paths and naming conventions used by this skill.

## Directory tree

```
<project-root>/
├── USAGE.md                        # 使用指南 — 快速开始、前置条件、常用命令（根目录）
│
└── docs/
    ├── main/                       # 项目蓝图 — 描述"是什么"
    │   ├── PROJECT_GUIDE.md        # 架构、模块职责、数据流、共享依赖
    │   ├── PROJECT_SPEC.md         # 技术范围、设计决策、功能边界
    │   ├── CODE_STYLE.md           # 命名、格式、风格约定
    │   ├── TEST_GUIDE.md           # 测试布局、回归覆盖、测试入口
    │   └── memory/                 # 跨平台项目记忆（见 context-memory.md）
    │       ├── MEMORY.md           # 记忆索引（始终先读这个）
    │       └── <type>-<topic>.md   # 记忆条目
    │
    ├── dep/                        # 项目日记 — 记录"做了什么"
    │   ├── dev-<YYYYMMDD>.md       # 开发日志（每日一个文件，内分多轮）
    │   └── review-<YYYYMMDD>-<NN>.md # 审查报告（按需生成，对照 dev 日志）
    │
    └── deploy/                     # 部署指引 — 说明"如何部署"
        └── DEPLOY_GUIDE.md          # 部署指南：环境、前置条件、步骤、配置、回滚
```

## File reference

### USAGE.md — 使用指南（项目根目录）

| File | Writes | When | Format |
|------|--------|------|--------|
| `USAGE.md` | Bootstrap / Development | Bootstrap auto-generates; dev mode updates as project evolves | Quick start, prerequisites, common commands, FAQ |

### docs/main/ — 项目蓝图

| File | Writes | When | Format |
|------|--------|------|--------|
| `PROJECT_GUIDE.md` | Bootstrap / Development | Bootstrap auto-generates; dev mode updates when architecture changes | Free-form, project-specific |
| `PROJECT_SPEC.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; dev mode fills in over time | Free-form, project-specific |
| `CODE_STYLE.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; dev mode fills in as conventions emerge | Free-form, project-specific |
| `TEST_GUIDE.md` | Bootstrap / Development | Bootstrap generates TBD placeholder; dev mode updates when test layout changes | Free-form, project-specific |
| `memory/MEMORY.md` | Bootstrap / Context update | Bootstrap creates empty; updated when a memory file is added/removed | Index — one link per line |
| `memory/<type>-<topic>.md` | Development / Consultation | When decisions, preferences, or project facts emerge | Frontmatter + markdown body (see context-memory.md) |

### docs/dep/ — 项目日记

| File | Writes | When | Format |
|------|--------|------|--------|
| `dev-<YYYYMMDD>.md` | Development (mandatory) | After each completed round of work; one file per day, multiple rounds within | 4 sections per round: Done, Issues/Blockers, Next, Files Changed (see dev-log-protocol.md) |
| `review-<YYYYMMDD>-<NN>.md` | Review (on demand) | Only after user confirms they want a full report (after Quick Review) | Frontmatter + Scope + Dev Logs Reviewed table + Findings + Next Actions (see review-protocol.md) |

### docs/deploy/ — 部署指引

| File | Writes | When | Format |
|------|--------|------|--------|
| `DEPLOY_GUIDE.md` | Deployment / Development | Bootstrap generates TBD placeholder; filled in when user asks to deploy or when deployment-relevant code changes | Environments, prerequisites, step-by-step, config, rollback procedure |

## Naming rules

| Pattern | Rule |
|---------|------|
| `USAGE.md` | Root level. Auto-generated at bootstrap, updated as project evolves. |
| `dev-<YYYYMMDD>.md` | Date of the development work. One file per day. Rounds within use `## Round N [HH:MM]`. |
| `review-<YYYYMMDD>-<NN>.md` | Date of the review. `NN` = sequential round `01`, `02`, ... per day. |
| `DEPLOY_GUIDE.md` | Persistent deployment guide. Bootstrap generates TBD placeholder; filled in over time. |
| `memory/<type>-<topic>.md` | `type` = `user` / `project` / `feedback` / `reference`. `topic` = short kebab-case identifier. |
