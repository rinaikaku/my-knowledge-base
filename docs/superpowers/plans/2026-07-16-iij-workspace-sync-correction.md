# IIJ Workspace 同步纠错机制 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 IIJ Workspace 的源目录、同步范围、提交前验证和副机验收固化为可重复执行的规则，避免错误目录或截图判断导致漏同步。

**Architecture:** 以 `D:\IIJ-Workspace` 为当前 IIJ Workspace 的唯一已确认源目录；仓库副本固定为 `projects/iij-workspace/`。每次同步在复制前、提交前、推送后和副机拉取后分别验证文件清单、远端与提交号。规则同时保留敏感信息、缓存和 Office 输出的排除边界。

**Tech Stack:** Git、PowerShell、Markdown。

---

### Task 1: 记录根因与证据

**Files:**
- Create: `docs/sync-correction-2026-07-16.md`

- [x] **Step 1: 记录可复核事实**

写明旧源目录 `D:\Codex\sandbox\K-os\IIJ-Workspace` 的 `03_Proposal` 仅含模板，而正确目录 `D:\IIJ-Workspace` 含 5 个提案文件；远端提交 `2f9ce05` 因此只含模板。

- [x] **Step 2: 区分根因与非根因**

将根因限定为“未验证源目录即复制，并以截图推断同步结果”；说明 `.gitignore` 和副机拉取不是此次缺失原因。

### Task 2: 固化主机同步原则

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`

- [x] **Step 1: 增加来源清单原则**

要求每个同步项目在提交前记录“源目录—仓库目标目录”映射；未验证映射不得执行复制或宣称同步完成。

- [x] **Step 2: 增加四阶段验收**

要求依次验证源文件、暂存清单、远端提交和副机拉取结果，并以 `git ls-files`、`git ls-tree`、`git status --short --branch` 等命令作为证据。

### Task 3: 更新副机协作流程

**Files:**
- Modify: `docs/sub-pc-setup.md`

- [x] **Step 1: 增加主机提交前检查命令**

给出参数化 PowerShell 示例，要求确认仓库目录、远端地址、目标文件跟踪状态及忽略规则。

- [x] **Step 2: 增加副机验收命令**

要求副机在 `git pull --rebase` 后，以 `git log -1` 和 `git ls-files` 验证预期文件存在；不一致时反馈命令输出，而不是重新猜测原因。

### Task 4: 验收并提交

**Files:**
- Verify: `AGENTS.md`
- Verify: `README.md`
- Verify: `docs/sub-pc-setup.md`
- Verify: `docs/sync-correction-2026-07-16.md`

- [x] **Step 1: 检查文档差异与 Markdown 文件清单**

运行：

```powershell
git diff --check
git diff --name-only
```

预期：仅包含上述同步原则和复盘文档；不包含凭据、缓存或 Office 输出。

- [ ] **Step 2: 提交并推送**

```powershell
git add AGENTS.md README.md docs/sub-pc-setup.md docs/sync-correction-2026-07-16.md docs/superpowers/plans/2026-07-16-iij-workspace-sync-correction.md
git commit -m "docs: add sync correction principles"
git push
```
