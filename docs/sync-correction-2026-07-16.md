# IIJ Workspace 同步纠错复盘（2026-07-16）

## 结论

此前 `projects/iij-workspace/03_Proposal/` 漏同步 4 个提案文件，不是副机拉取失败，也不是 `.gitignore` 排除了这些文件。

根因是主机在未验证源目录的情况下，将 `D:\Codex\sandbox\K-os\IIJ-Workspace` 误作为 IIJ Workspace 的源目录复制到仓库；该目录的 `03_Proposal/` 当时仅含 `Proposal_Template.md`。正确的当前源目录是 `D:\IIJ-Workspace`，其中还包含以下文件：

- `AI_RAG_Customer_Proposal_Wording.md`
- `Kowa_Security_Evaluation_Proposal.md`
- `NTT_ID_SMX_Service_Recovery_Strategy.md`
- `Nikon中国统一服务器基础设施_提案概要.md`

因此，远端提交 `2f9ce05` 中仅有模板文件是源目录选择错误的直接结果。随后以正确目录重建同步内容，并推送为提交 `46b6b9d`。

## 失效点

1. **来源确认缺失：** 仅按历史路径和截图推断，没有先列出正确源目录的文件清单。
2. **提交前验证不足：** 没有对关键目录执行 `git ls-files`，因而未能在推送前发现 4 个文件未被跟踪。
3. **完成条件错误：** 将“`git push` 成功”误当作“预期内容已同步”；推送只能证明已提交内容到达远端，不能证明来源完整。
4. **跨机验收缺失：** 副机在首次拉取后没有按关键文件清单验证远端内容，导致差异直到人工比对后才暴露。

## 纠错机制

后续同步必须完成四阶段闭环；任一阶段不一致时停止推送并保留命令输出。

| 阶段 | 必须确认的事实 | 最小证据 |
| --- | --- | --- |
| 源目录 | 路径、文件数和关键文件均来自当前实际项目目录 | `Get-ChildItem`、`rg --files` |
| 暂存区 | 目标文件已被 Git 跟踪，且未被忽略 | `git status --short --untracked-files=all`、`git ls-files`、`git check-ignore -v` |
| 远端 | 本地提交已抵达正确仓库的正确分支 | `git remote -v`、`git push`、`git ls-remote origin refs/heads/main` |
| 副机 | 拉取后的提交号和关键文件与主机一致 | `git pull --rebase`、`git log -1 --oneline`、`git ls-files` |

## IIJ Workspace 的当前映射

| 项目 | 已确认源目录（主机） | 版本化目标目录 |
| --- | --- | --- |
| IIJ Workspace | `D:\IIJ-Workspace` | `projects/iij-workspace/` |

此映射在源目录迁移时必须先更新本文件和同步命令，再进行复制或提交。

## 同步边界

- 可同步：Markdown、项目配置、脚本、索引、必要的非 Office 参考资产。
- 不同步：`.env`、密钥、令牌、账号会话、Codex 缓存、本地数据库、依赖目录、构建产物、`outputs/`、`work/`，以及生成的 Office 文档（`*.pptx`、`*.docx`、`*.xlsx`）及其检查输出。
- 客户资料在推送前仍需检查是否包含凭据、令牌或不应进入远端的敏感正文；发现疑似敏感内容时先停在暂存前处理，不以“需要双机同步”为由绕过检查。
