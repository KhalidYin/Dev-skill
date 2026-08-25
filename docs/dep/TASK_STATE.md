---
status: blocked
created: 2026-08-17 11:40
updated: 2026-08-17 13:10
---

# Current Task

## Goal

移除 Codebuddy 安装目标并清理已退役的 `clinical-statistical-design` 残留。

## Progress

- [x] 核对安装脚本中的 Codebuddy 路径
- [x] 验证四个旧 Junction 均指向本项目旧目录
- [x] 修改 Windows 和 Bash 安装脚本
- [ ] 删除旧 Junction、空目录和旧分发包（工具安全策略阻断）
- [x] 执行安装与项目校验
- [x] 更新开发日志；删除完成后再移除本检查点

## Working Context

- **Files being edited**: `scripts/install.ps1`, `scripts/install.sh`, `docs/dep/devlog/`
- **Last command run**: 安装脚本、项目校验和 Codex quick validator 均通过；脚本中已无 Codebuddy 引用
- **Key decisions**: 用户已明确授权删除旧 Skill；外部只删除目标精确指向本项目旧目录的 Junction
- **Blocker**: Shell 安全策略拒绝所有删除命令，即使目标已验证且用户已授权；需用户在本机终端执行精确清理命令

## Resume From

用户完成精确清理命令后，复核六个旧路径均不存在并删除本检查点。
