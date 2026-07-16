import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const baseDir = "D:/IIJ-Workspace/三社月结统计";

function parseCsv(text) {
  return text
    .replace(/^\uFEFF/, "")
    .trim()
    .split(/\r?\n/)
    .map((line) => line.split(",").map((value) => {
      const numeric = Number(value);
      return value !== "" && Number.isFinite(numeric) ? numeric : value;
    }));
}

async function readCsv(name) {
  const text = await fs.readFile(path.join(baseDir, name), "utf8");
  return parseCsv(text);
}

const renameRows = await readCsv("rename_log.csv");
const diffRows = await readCsv("monthly_diff.csv");

const workbook = Workbook.create();

function addSheet(name, rows, widths) {
  const sheet = workbook.worksheets.add(name);
  const rowCount = rows.length;
  const colCount = rows[0].length;
  const range = sheet.getRangeByIndexes(0, 0, rowCount, colCount);
  range.values = rows;

  sheet.getRangeByIndexes(0, 0, 1, colCount).format = {
    fill: "#1F4E79",
    font: { bold: true, color: "#FFFFFF" },
  };
  range.format.borders = { preset: "all", style: "thin", color: "#D9E2F3" };
  sheet.freezePanes.freezeRows(1);

  rows[0].forEach((_, idx) => {
    const column = sheet.getRangeByIndexes(0, idx, rowCount, 1);
    column.format.columnWidth = widths[idx] ?? 16;
    if (idx >= 2 && rows[0][idx].toString().match(/amount|total|diff|金额|差异/i)) {
      column.format.numberFormat = "#,##0";
    }
  });

  sheet.getRangeByIndexes(1, 0, Math.max(rowCount - 1, 1), colCount).format.wrapText = true;
  return sheet;
}

addSheet("改名记录", renameRows, [12, 16, 12, 72, 72]);
addSheet("月间差异", diffRows, [16, 24, 14, 14, 14, 18]);

for (const sheet of workbook.worksheets.items) {
  sheet.showGridLines = false;
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(baseDir, "三社月结统计.xlsx"));

for (const csvName of ["rename_log.csv", "monthly_diff.csv"]) {
  const text = await fs.readFile(path.join(baseDir, csvName), "utf8");
  await fs.writeFile(path.join(baseDir, csvName), `\uFEFF${text.replace(/^\uFEFF/, "")}`, "utf8");
}

const preview = await workbook.render({
  sheetName: "月间差异",
  autoCrop: "all",
  scale: 1,
  format: "png",
});
await fs.writeFile(
  path.join(baseDir, "月间差异_preview.png"),
  new Uint8Array(await preview.arrayBuffer()),
);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
console.log(errors.ndjson);
