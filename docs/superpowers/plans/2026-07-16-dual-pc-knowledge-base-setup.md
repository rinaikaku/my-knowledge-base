# 双 PC 知识库初始化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立可由主机与副机通过私有 Git 仓库同步的版本化知识库基础结构。

**Architecture:** 仓库内的 Markdown 知识条目、元数据和项目规则由 Git 管理；每台电脑保留独立工作副本。README 说明知识库入口，AGENTS 固化 Codex 规则，副机指南定义首次克隆和日常同步流程。

**Tech Stack:** Git、Markdown、PowerShell。

---

## 文件结构

- 创建：`.gitignore` — 排除凭据、缓存、临时文件与本地工具目录。
- 创建：`README.md` — 项目用途、目录说明与主机日常流程。
- 创建：`AGENTS.md` — Codex 在本项目记录与更新知识时的规则。
- 创建：`knowledge/README.md` — 知识条目格式、命名与元数据规范。
- 创建：`docs/sub-pc-setup.md` — 副机首次接入和每日操作步骤。

### Task 1: 建立安全的项目边界

**Files:**
- Create: `.gitignore`
- Create: `AGENTS.md`

- [ ] **Step 1: 写入忽略规则**

```gitignore
# Secrets and local configuration
.env
.env.*
!.env.example
*.pem
*.key

# Codex and tool-local state
.codex/local/
.codex/cache/

# OS and editor files
.DS_Store
Thumbs.db
*.tmp
~$*

# Python and Node local environments
.venv/
venv/
node_modules/
```

- [ ] **Step 2: 验证忽略规则不跟踪 `.env`**

Run: `git check-ignore -v .env`

Expected: 输出 `.gitignore` 中匹配 `.env` 的规则。

- [ ] **Step 3: 写入 Codex 项目规则**

```markdown
# 项目工作规则

- 知识库正文、结构化元数据和索引规则必须保存在仓库内的版本化文件中。
- 新建知识记录时保留来源日期、具体时间、来源位置和原始文件链接；不凭空补充事实。
- 将事实、推断与待确认事项明确区分。
- 提交前不得写入密钥、账号令牌、客户敏感正文或 Codex 本地缓存。
- 更新知识后，先检查 `git diff`，再进行小粒度提交并推送。
- 发现另一台电脑已有新提交时，先拉取并处理冲突，禁止使用强制推送覆盖历史。
```

- [ ] **Step 4: 验证工作规则已存在**

Run: `rg -n "来源日期|事实、推断|强制推送" AGENTS.md`

Expected: 输出三条规则的行号。

### Task 2: 建立知识库入口和条目规范

**Files:**
- Create: `README.md`
- Create: `knowledge/README.md`

- [ ] **Step 1: 写入项目入口说明**

```markdown
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
# 更新知识文件
git status
git add knowledge docs README.md AGENTS.md
git commit -m "docs: 更新知识库"
git push
```

远端仓库创建并绑定前，`git push` 不可用；本地提交仍会保留完整历史。
```

- [ ] **Step 2: 写入知识条目规范**

```markdown
# 知识条目规范

## 存放方式

每条知识使用一个 Markdown 文件，按主题建立子目录，例如 `knowledge/projects/`、`knowledge/customers/`、`knowledge/decisions/`。

## 必填元数据

```yaml
title: 条目标题
date: 2026-07-16
time: "14:30"
source: 原始材料名称或链接
status: fact
```

`status` 只能使用 `fact`、`inference` 或 `pending-confirmation`。没有明确时间时，省略 `time`，不要虚构。
```

- [ ] **Step 3: 验证知识规范包含三种状态**

Run: `rg -n "fact|inference|pending-confirmation" knowledge/README.md`

Expected: 输出状态定义所在行。

### Task 3: 编写副机接入与同步指南

**Files:**
- Create: `docs/sub-pc-setup.md`

- [ ] **Step 1: 写入副机指南**

指南必须覆盖：Git 安装与身份检查、私有仓库克隆、首次打开 Codex 的目录选择、开始工作前拉取、变更后提交推送、冲突处理、禁止同步的内容，以及主机创建远端后如何添加 `origin`。

- [ ] **Step 2: 验证指南包含核心命令**

Run: `rg -n "git clone|git pull --rebase|git push|git remote add origin" docs/sub-pc-setup.md`

Expected: 四个命令均有匹配项。

### Task 4: 提交并验证本机基础结构

**Files:**
- Modify: `.gitignore`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `knowledge/README.md`
- Modify: `docs/sub-pc-setup.md`

- [ ] **Step 1: 检查预期文件和 Git 状态**

Run: `git status --short; Get-ChildItem -Force; Get-ChildItem knowledge; Get-ChildItem docs`

Expected: 五个文件均存在，且 Git 显示它们为待提交内容。

- [ ] **Step 2: 提交基础结构**

Run: `git add .gitignore README.md AGENTS.md knowledge/README.md docs/sub-pc-setup.md; git commit -m "chore: initialize shared knowledge base"`

Expected: Git 输出一个包含五个文件的提交。

- [ ] **Step 3: 完整验证**

Run: `git status --short --branch; git log --oneline -2; git check-ignore -v .env; rg -n "git clone|git pull --rebase|git push|git remote add origin" docs/sub-pc-setup.md`

Expected: 工作区无待提交修改；最近两条提交包含设计说明与基础结构；`.env` 被忽略；副机指南包含四个核心命令。
