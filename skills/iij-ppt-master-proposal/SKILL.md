---
name: iij-ppt-master-proposal
description: Create IIJ-style Japanese business proposal decks from user-provided proposal materials using the installed ppt-master pipeline. Use when the user asks to make, plan, or revise a PPT/PPTX for IIJ, IIJ Global Solutions China, customer proposals, IT operation proposals, M365 migration proposals, PC support proposals, or says to combine "IIJ style", "ppt-master", and provided source documents.
---

# IIJ PPT Master Proposal

Build customer-facing Japanese proposal decks with the installed `ppt-master` skill, using IIJ red-white corporate visual DNA and user-provided source materials.

## Required Skill Chain

1. Use this skill for IIJ proposal-specific defaults and guardrails.
2. Also use `$ppt-master` for the actual pipeline. Read its `SKILL.md` before executing the deck workflow.
3. If the user supplies a native PPTX company introduction deck, use it as visual reference/source context unless it is an explicit `ppt-master` template directory. Do not treat an arbitrary PPTX as a `ppt-master` template path.

## Core Defaults

- Language: Japanese business style unless the user explicitly requests otherwise.
- Audience: customer-facing enterprise proposal or internal customer decision support.
- Canvas: `ppt169`, 16:9, 1280 x 720.
- Style objective: `B) General Consulting + IIJ corporate business proposal`.
- Visual style: IIJ red-white, not blue-primary.
- Main palette:
  - Background: `#FFFFFF`
  - Primary IIJ red: `#D9003F`
  - Black: `#111111`
  - Deep red: `#7A001F`
  - Secondary background: `#F4F5F7`
  - Body text: `#1F2328`
  - Secondary text: `#5C6670`
  - Border: `#D8DDE3`
  - Caution: `#A86A00`
- Typography: PPT-safe Gothic stack. Prefer `Microsoft YaHei, Arial, sans-serif` in SVG and `spec_lock.md`; avoid quoted font-family values that can cause checker drift.
- Icons: `tabler-outline`, stroke width `2`, one icon library per deck.
- Image usage: no AI or web images by default. Use user/company PPTX assets only when necessary and explicitly planned.

## Proposal Content Rules

- Treat user source files as authority. Do not invent facts, quantities, dates, schedule estimates, service scope, or customer constraints.
- If supplier quotation files are used, extract service scope and assumptions only. Do not expose supplier price, unit price, subtotal, total price, or quote validity in customer-facing slides unless the user explicitly asks.
- Preserve customer-facing wording. Do not expose internal notes, tool workflow, or "supplier gave me" framing in visible slide content.
- For IT operation/M365/PC support proposals, prefer this narrative:
  1. Current contracted operation scope
  2. Gap or additional consideration area
  3. Proposed support or migration scope
  4. Operational flow or migration prerequisites
  5. Schedule and next confirmation items

## ppt-master Workflow Overlay

Follow `ppt-master` exactly:

1. Convert/import source materials.
2. Initialize a `ppt-master` project.
3. Use free design unless the user provides an explicit `ppt-master` template directory containing `design_spec.md`.
4. Present Eight Confirmations and stop for explicit confirmation.
5. After confirmation, write `design_spec.md` and `spec_lock.md`.
6. Generate SVG pages sequentially, rereading `spec_lock.md` before every page.
7. Run `svg_quality_checker.py` and fix all errors. Prefer fixing warnings when straightforward.
8. Generate speaker notes, run post-processing, and export PPTX.

Recommended Eight Confirmations for an IIJ proposal:

1. Canvas: `ppt169`
2. Page count: match content volume; often 8-12 pages
3. Audience: customer IT/management stakeholders
4. Style: `B) General Consulting + IIJ corporate business proposal`
5. Color: IIJ red-white corporate palette above
6. Icon: `tabler-outline`, stroke width `2`
7. Typography: `Microsoft YaHei, Arial, sans-serif`; formula policy `text-only` unless technical formulas exist
8. Images: no external/AI images by default

## Encoding Safety

This workflow often contains Japanese and Chinese filenames/content. On Windows:

- Do not write Japanese SVG/PPT content through PowerShell strings, here-strings, `Set-Content`, or inline command text if avoidable.
- Prefer creating or editing UTF-8 files with `apply_patch`.
- For generated helper scripts containing Japanese text, save the script as UTF-8 first, then run it.
- When using Python, set/read/write `encoding="utf-8"` explicitly.
- For commands that print Japanese, set `PYTHONIOENCODING=utf-8`.
- Before exporting PPTX, inspect one SVG with UTF-8 read and confirm real Japanese text is present, not `???`.
- After exporting PPTX, inspect `ppt/slides/slide1.xml` inside the PPTX and confirm `<a:t>` contains Japanese text, not `???`.

## Quality Gates

Before final delivery:

- `svg_quality_checker.py` must report 0 errors. Target 0 warnings.
- Confirm `spec_lock drift: none`.
- Confirm visible slide copy contains no forbidden price information unless explicitly requested.
- Confirm the final PPTX exists under `exports/`; copy it to the workspace `outputs/` folder for easy access.

## Reference

For a compact example based on a completed Senju/IIJ operation support and M365 migration deck, read `references/senju-example.md` when working on a similar proposal.
