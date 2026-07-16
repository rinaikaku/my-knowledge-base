#!/usr/bin/env python3
"""Monthly fapiao PDF rename and variance report helper."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover
    raise SystemExit("PyMuPDF is required: pip install PyMuPDF") from exc


@dataclass
class Invoice:
    path: Path
    invoice_no: str
    ds: str
    total: float
    period_text: str
    period_token: str
    customer: str

    @property
    def key(self) -> tuple[str, float]:
        return (self.ds, round(self.total, 2))


def read_text(path: Path) -> str:
    with fitz.open(path) as doc:
        return "\n".join(page.get_text() for page in doc)


def period_to_token(period_text: str) -> str:
    parts = re.findall(r"20\d{2}/\d{2}/\d{2}", period_text)
    if len(parts) != 2:
        return ""
    return "-".join(part.replace("/", "") for part in parts)


def extract(path: Path) -> Invoice:
    text = read_text(path)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    invoice = re.search(r"(263\d{17})", text)
    ds = re.search(r"\b(DS\d{10})\b", text)
    total = re.search(r"¥\s*([0-9]+(?:\.[0-9]{2})?)", text)
    period = re.search(r"(20\d{2}/\d{2}/\d{2})\s*~\s*(20\d{2}/\d{2}/\d{2})", text)

    missing = [
        name
        for name, match in [
            ("invoice number", invoice),
            ("DS number", ds),
            ("total", total),
            ("period", period),
        ]
        if not match
    ]
    if missing:
        raise ValueError(f"{path.name}: missing {', '.join(missing)}")

    period_text = period.group(0)
    customer = ""
    if period_text in lines:
        index = lines.index(period_text)
        if index + 1 < len(lines):
            customer = lines[index + 1]

    return Invoice(
        path=path,
        invoice_no=invoice.group(1),
        ds=ds.group(1),
        total=float(total.group(1)),
        period_text=period_text,
        period_token=period_to_token(period_text),
        customer=customer,
    )


def load_invoices(folder: Path) -> list[Invoice]:
    pdfs = sorted(folder.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"No PDF files found: {folder}")
    return [extract(path) for path in pdfs]


def target_name(previous: Invoice, current: Invoice) -> str:
    tail = previous.path.name.split("_", 1)[1] if "_" in previous.path.name else previous.path.name
    if previous.period_token and current.period_token:
        tail = tail.replace(previous.period_token, current.period_token)
    else:
        tail = re.sub(r"20\d{6}-20\d{6}", current.period_token, tail)
    return f"{current.invoice_no}_{tail}"


def aggregate(rows: list[Invoice]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        totals[row.ds] += row.total
    return dict(totals)


def first_customer(rows: list[Invoice]) -> dict[str, str]:
    customers: dict[str, str] = {}
    for row in rows:
        customers.setdefault(row.ds, row.customer)
    return customers


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def money(value: float) -> str:
    return f"{value:,.0f}" if value == round(value) else f"{value:,.2f}"


def build_reports(
    prev: list[Invoice],
    current: list[Invoice],
    output_dir: Path,
    rename_rows: list[list[object]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    prev_totals = aggregate(prev)
    current_totals = aggregate(current)
    customers = first_customer(prev + current)

    diff_rows: list[list[object]] = []
    for ds in sorted(set(prev_totals) | set(current_totals)):
        old = prev_totals.get(ds, 0.0)
        new = current_totals.get(ds, 0.0)
        diff = new - old
        if old and new:
            status = "持平" if diff == 0 else "金额变动"
        elif old:
            status = "当月未出现"
        else:
            status = "当月新增"
        diff_rows.append([ds, customers.get(ds, ""), old, new, diff, status])

    write_csv(
        output_dir / "rename_log.csv",
        ["status", "ds", "total", "old_name", "new_name"],
        rename_rows,
    )
    write_csv(
        output_dir / "monthly_diff.csv",
        ["ds", "project", "amount_prev", "amount_current", "diff", "status"],
        diff_rows,
    )

    missing = [row for row in diff_rows if row[5] == "当月未出现"]
    new_only = [row for row in diff_rows if row[5] == "当月新增"]
    readme = [
        "# 发票整理月结报告",
        "",
        f"- 上月 PDF 数：{len(prev)}",
        f"- 当月 PDF 数：{len(current)}",
        f"- 上月合计：{money(sum(row.total for row in prev))}",
        f"- 当月合计：{money(sum(row.total for row in current))}",
        f"- 差异：{money(sum(row.total for row in current) - sum(row.total for row in prev))}",
        "",
        "## 上月有、当月未出现",
        "",
        "| DS 编号 | 项目 | 上月金额 |",
        "|---|---|---:|",
    ]
    readme += [f"| {ds} | {project} | {money(old)} |" for ds, project, old, *_ in missing]
    readme += [
        "",
        "## 当月新增",
        "",
        "| DS 编号 | 项目 | 当月金额 |",
        "|---|---|---:|",
    ]
    readme += [f"| {ds} | {project} | {money(new)} |" for ds, project, _, new, *_ in new_only]
    (output_dir / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prev-dir", required=True, type=Path)
    parser.add_argument("--current-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="Actually rename matched current PDFs.")
    args = parser.parse_args()

    prev = load_invoices(args.prev_dir)
    current = load_invoices(args.current_dir)
    prev_by_key = {row.key: row for row in prev}

    rename_rows: list[list[object]] = []
    for row in current:
        previous = prev_by_key.get(row.key)
        if not previous:
            rename_rows.append(["kept", row.ds, row.total, row.path.name, ""])
            continue
        new_name = target_name(previous, row)
        rename_rows.append(["renamed" if args.apply else "preview", row.ds, row.total, row.path.name, new_name])
        if args.apply and row.path.name != new_name:
            target = row.path.with_name(new_name)
            if target.exists():
                raise FileExistsError(f"Target exists: {target}")
            row.path.rename(target)

    build_reports(prev, current, args.output_dir, rename_rows)
    print(f"previous_count={len(prev)} current_count={len(current)}")
    print(f"previous_total={sum(row.total for row in prev):.2f}")
    print(f"current_total={sum(row.total for row in current):.2f}")
    print(f"reports={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
