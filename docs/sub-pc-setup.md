# 副机接入与同步指南

本指南使用私有 GitHub 仓库 `rinaikaku/my-knowledge-base`。由于当前网络到 `github.com` 的 HTTPS 路由不稳定，主机与副机统一使用 GitHub 官方支持的 SSH-over-443 连接。

## 一次性准备

1. 在副机安装 Git，并在 PowerShell 中确认：

   ```powershell
   git --version
   git config --global user.name "你的姓名"
   git config --global user.email "你的邮箱"
   ```

2. 使用有仓库访问权限的 GitHub 账号，并在该副机生成独立 SSH 密钥、将公钥添加到 GitHub。不要在命令行保存明文密码或复制主机私钥。

3. 在副机选择一个不被实时云盘同步的本地目录，然后克隆仓库：

   ```powershell
   git clone ssh://git@ssh.github.com:443/rinaikaku/my-knowledge-base.git
   cd my-knowledge-base
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

## 主机同步项目文件前的强制检查

主机从其他工作目录同步项目时，先在仓库根目录执行以下检查。以 IIJ Workspace 为例，当前已确认源目录是 `D:\IIJ-Workspace`，目标是 `projects/iij-workspace/`：

```powershell
$repo = "C:\Users\KAKU\Documents\Codex\2026-07-16\wo-de"
$source = "D:\IIJ-Workspace"
$target = "projects/iij-workspace"

Get-ChildItem "$source\03_Proposal" -File
git -C $repo status --short --untracked-files=all -- $target
git -C $repo ls-files -- "$target/03_Proposal"
git -C $repo check-ignore -v -- "$target/03_Proposal/AI_RAG_Customer_Proposal_Wording.md"
git -C $repo remote -v
```

验收标准：源目录中存在预期文件；`git ls-files` 能列出预期文件；`git check-ignore -v` 对预期文件没有输出；`origin` 的 fetch 与 push 地址均为 `ssh://git@ssh.github.com:443/rinaikaku/my-knowledge-base.git`。任何一项不符合时，不得推送，应先修正源目录或同步范围。

完成复制与提交后，再执行：

```powershell
git -C $repo diff --cached --check
git -C $repo push
git -C $repo ls-remote origin refs/heads/main
```

## 副机拉取后的验收

副机每次拉取项目更新后，除 `git pull --rebase` 外，还应检查提交号和关键文件：

```powershell
git pull --rebase
git log -1 --oneline
git ls-files -- projects/iij-workspace/03_Proposal
```

如预期文件缺失，请反馈上述命令输出以及 `git remote -v`；不要根据截图或文件夹名称重新猜测源目录，也不要使用强制推送覆盖远端。

## 出现冲突时

1. 不要使用 `git push --force`。
2. 运行 `git pull --rebase`，根据 Git 标记解决冲突文件。
3. 检查冲突解决后的内容，确认没有丢失另一台电脑的知识更新。
4. 运行 `git add <已解决文件>`，再运行 `git rebase --continue`。
5. 完成后执行 `git push`。

## 主机首次创建远端后的绑定命令

主机远端已绑定为：

```powershell
git remote -v
```

若重新绑定远端，使用：

```powershell
git remote set-url origin ssh://git@ssh.github.com:443/rinaikaku/my-knowledge-base.git
```

随后副机执行本指南中的 `git clone`。
