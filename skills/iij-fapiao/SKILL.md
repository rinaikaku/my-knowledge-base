---
name: iij-fapiao
description: Use when the user needs IIJ invoice/fapiao monthly整理, renaming current-month invoice PDF files from the previous month's naming format, comparing monthly totals, reporting missing/new DS projects, or preparing Office-readable CSV/XLSX summaries.
---

# IIJ 发票

## Overview

Use the previous month's PDF folder as the naming reference for the current month. Match invoices by PDF content, not by timestamp filename, then rename only matched current-month PDFs and report monthly differences.

## Workflow

1. Inspect both folders and confirm they contain PDF invoices.
2. Extract each PDF's invoice number, `DS` number, billing period, customer/project text, and tax-included total.
3. Match current-month PDFs to previous-month PDFs by `DS` number + total amount.
4. Rename only matched current-month files using the previous-month filename tail, replacing the compact period token with the current period.
5. Do not rename current-month PDFs that do not exist in the previous month.
6. Report previous-month projects missing from the current month.
7. Produce a subproject folder with:
   - `README.md`
   - `rename_log.csv`
   - `monthly_diff.csv`
   - Prefer `.xlsx` too when Office readability matters.

## Script

Use `scripts/fapiao_monthly.py` for deterministic extraction, matching, rename preview/apply, and report generation.

Preview only:

```powershell
python scripts/fapiao_monthly.py --prev-dir "D:\...\2606\06PDF" --current-dir "D:\...\2607\07PDF" --output-dir "D:\IIJ-Workspace\三社月结统计"
```

Apply renames:

```powershell
python scripts/fapiao_monthly.py --prev-dir "D:\...\2606\06PDF" --current-dir "D:\...\2607\07PDF" --output-dir "D:\IIJ-Workspace\三社月结统计" --apply
```

If the PDF folders are outside the writable workspace, request filesystem approval before `--apply`.

## Matching Rules

- Primary key: `DS` number + tax-included total.
- Preserve the old filename style after the first underscore, including spaces, underscores, Japanese/Chinese text, and existing punctuation.
- Replace compact date patterns like `20260601-20260631` with the current period token inferred from the current PDF period, such as `20260701-20260731`.
- Keep unmatched current-month files unchanged and list them as new/current-only.
- List previous-month matched keys missing from current as disappeared/missing.

## Office Compatibility

- Save CSV as `utf-8-sig` so Excel/Office opens Chinese and Japanese text without mojibake.
- When the user says CSV opens garbled, create `.xlsx` from the CSV outputs and cite the workbook path.

## Common Mistakes

| Mistake | Correct action |
|---|---|
| Matching by customer name only | Use `DS` + total; one customer can have multiple invoices. |
| Renaming every current-month PDF | Rename only files whose key exists in the previous month. |
| Treating timestamp files as unusable | Extract PDF text; the needed data is in the invoice body. |
| Saving plain UTF-8 CSV for Office | Use UTF-8 BOM (`utf-8-sig`) or generate `.xlsx`. |
| Claiming totals without rerun | Re-extract PDFs after rename and verify counts/totals. |

