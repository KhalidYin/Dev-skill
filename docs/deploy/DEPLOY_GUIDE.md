# 部署指南

本项目不部署业务服务。Skill 通过安装脚本链接或复制到本机 agent 的 skills 目录。

## 前置条件

- 目标 agent 的 skills 目录已存在。
- Windows 使用 PowerShell；macOS/Linux 使用 shell。

## 安装

```powershell
.\scripts\install.ps1 -SkillName <skill-name>
```

## 验证

运行 `python scripts/validate_all.py`，并在目标 agent 中确认 skill 可发现且触发边界符合 eval 用例。

## 回滚

删除目标 skills 目录中对应的链接或副本；源 skill 仍保留在本仓库。

