# 副机接入与同步指南

本指南假定主机已创建一个私有 GitHub 仓库，并已将本机项目推送到该仓库。

## 一次性准备

1. 在副机安装 Git，并在 PowerShell 中确认：

   ```powershell
   git --version
   git config --global user.name "你的姓名"
   git config --global user.email "你的邮箱"
   ```

2. 使用有仓库访问权限的 GitHub 账号登录；建议使用 SSH 密钥或 Git Credential Manager，避免在命令行保存明文密码。

3. 在副机选择一个不被实时云盘同步的本地目录，然后克隆仓库：

   ```powershell
   git clone <你的私有仓库地址>
   cd <仓库目录名>
   ```

4. 在 Codex 中打开该克隆目录。Codex 的会话和缓存仍各自保留在本机；项目规则与知识文件来自此仓库。

## 每次开始工作前

```powershell
git status
git pull --rebase
```

如果 `git status` 显示未提交修改，先提交、暂存或处理它们；不要在有本地修改时盲目拉取。

## 完成一次知识更新后

```powershell
git status
git add knowledge docs README.md AGENTS.md
git commit -m "docs: 更新知识库"
git push
```

只提交知识、规则和非敏感项目文件。不要提交 `.env`、密钥、令牌、账号会话、Codex 缓存或本地数据库。

## 出现冲突时

1. 不要使用 `git push --force`。
2. 运行 `git pull --rebase`，根据 Git 标记解决冲突文件。
3. 检查冲突解决后的内容，确认没有丢失另一台电脑的知识更新。
4. 运行 `git add <已解决文件>`，再运行 `git rebase --continue`。
5. 完成后执行 `git push`。

## 主机首次创建远端后的绑定命令

在 GitHub 创建空的私有仓库后，于主机项目目录执行：

```powershell
git remote add origin <你的私有仓库地址>
git branch -M main
git push -u origin main
```

随后副机才执行本指南中的 `git clone`。
