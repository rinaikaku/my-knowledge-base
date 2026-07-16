# 我的知识库

这是一个以 Git 管理、可在主机与副机之间同步的知识库。

## 目录

- `knowledge/`：知识正文、元数据与索引规范。
- `docs/`：项目设计、操作指南与决策记录。
- `outputs/`：面向用户生成的交付物；默认不进入跨电脑 Git 同步。
- `work/`：本地过程文件；默认不作为稳定知识源。

## 主机日常流程

```powershell
git pull --rebase
# 先确认实际源目录与仓库目标目录的映射；IIJ Workspace 当前为：
# D:\IIJ-Workspace -> projects/iij-workspace/
git status
git add knowledge docs projects/iij-workspace README.md AGENTS.md
git commit -m "docs: 更新知识库"
git push
```

## 项目同步验收

对于从主机其他目录复制进来的项目，不能只因 `git push` 成功就认定同步完成。必须依次确认：

1. 源目录存在预期关键文件；
2. 仓库副本已跟踪这些文件，且文件未被忽略；
3. `origin` 指向 `rinaikaku/my-knowledge-base`，推送后远端 `main` 已更新；
4. 副机 `git pull --rebase` 后能列出同一批关键文件。

具体根因、命令与边界见 [IIJ Workspace 同步纠错复盘](docs/sync-correction-2026-07-16.md)。

本项目的远端仓库是 `rinaikaku/my-knowledge-base`，并使用 SSH-over-443 连接，以适配当前网络环境。首次推送前，需要将本机 SSH 公钥添加到 GitHub。

## 安全边界

知识、规则和非敏感项目配置可以进入 Git。密钥、令牌、账号会话和 Codex 缓存不可提交；请在两台电脑各自通过受控密码管理器或企业密钥管理系统获取。
