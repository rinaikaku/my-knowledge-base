# 我的知识库

这是一个以 Git 管理、可在主机与副机之间同步的知识库。

## 目录

- `knowledge/`：知识正文、元数据与索引规范。
- `docs/`：项目设计、操作指南与决策记录。
- `outputs/`：面向用户的交付物；仅提交需要版本化保存的文件。
- `work/`：本地过程文件；默认不作为稳定知识源。

## 主机日常流程

```powershell
git pull --rebase
# 更新 knowledge/ 或 docs/ 中的文件
git status
git add knowledge docs README.md AGENTS.md
git commit -m "docs: 更新知识库"
git push
```

本项目的远端仓库是 `rinaikaku/my-knowledge-base`，并使用 SSH-over-443 连接，以适配当前网络环境。首次推送前，需要将本机 SSH 公钥添加到 GitHub。

## 安全边界

知识、规则和非敏感项目配置可以进入 Git。密钥、令牌、账号会话和 Codex 缓存不可提交；请在两台电脑各自通过受控密码管理器或企业密钥管理系统获取。
