---
name: legacy-data-migration
description: >-
  Patterns and pitfalls for migrating/ETL-ing data between RDBMSs (SQL Server,
  MySQL, Oracle, ...): the source → intermediate file → target flow, ordinal
  (position-based) column mapping via templates, type-driven emit rules
  (NULL/quoting/defaults), dirty-data handling (length overflow, CR/LF breaking
  records, character escaping), transactions & rollback, import ordering,
  collation/charset reconciliation, and post-migration verification. Language-
  agnostic — applies whether the tool is written in VB.NET, C#, Python, or shell.
  Use when building or fixing a migration/ETL tool, writing data-transfer scripts,
  or debugging import failures. Triggers: "migrate data", "data migration", "ETL",
  "import/export data", "move DB", "column mapping", "dirty data", "collation",
  "charset".
metadata:
  type: reference
---

# Legacy data migration (ETL between RDBMSs)

Patterns and pitfalls for **migrating data between database systems** — independent of the
implementation language (VB.NET, C#, Python, scripts...). It focuses on the *process* and the
common failure modes, not on any one language's syntax.

> This is *general* guidance. Read the actual code/flow first and follow the conventions of
> the tool you are working on.

## Common flow architecture

**Source → intermediate file → target.** Many tools don't insert directly; instead they:

1. **Export**: SELECT from the source DB → write to an intermediate text file (one record per
   line, columns separated by a delimiter — often a comma).
2. **Transform**: map columns, coerce types, normalize values per a template/config.
3. **Import**: read the intermediate file → generate INSERTs → load the target DB inside a
   transaction.

Upside: clear separation, reviewable intermediate data, re-runnable per step. Downside: **a
line-based intermediate file is very sensitive to structure-breaking characters** (see
dirty-data below).

## Ordinal (position-based) column mapping — the biggest pitfall

Many tools use a **template file mapping source → target columns by POSITION, not by name**:

- The writer loops `for i = 0..colCount-1` writing each column; the importer `split(...)`s and
  pairs value *i* with template line *i*.
- → **The Nth column of the SELECT must match the Nth template line.** The import usually aborts
  if the exported column count ≠ the template line count.
- **Adding a column = edit both the SELECT and the template, and append at the END.** Such code
  often has hardcoded branches keyed on *column index*; inserting in the middle shifts every
  index after it.
- A single template line typically holds: target column name, type/attribute, formatting flags,
  default value, source column name.

### Type-driven emit rules

- **Numeric** types (`INT`/`TINYINT`/`DOUBLE`/...) → bare value (no quotes); empty → `NULL`.
- **Text** types → single-quoted `'...'`; empty → `''`.
- A **default value** in the template → used in place of an empty cell.
- **The template's encoding and line endings matter** (UTF-16LE/UTF-8, BOM or not, CRLF/LF).
  Preserve the original when editing, or the import will read it wrong.

## Dirty-data handling

Normalize values **before writing the intermediate file**:

- **Delimiter characters inside a field** (commas...) → replace with a safe character, or
  quote/escape per a real standard.
- **CR/LF embedded in a text field** → **breaks the record line** in a line-based file: one
  record splits across several physical lines → each fragment has the wrong column count. Strip/
  replace CR/LF within the field (usually safe and lossless for names/notes).
- **Target-DB escape characters** (e.g. `\` in MySQL) → escape or replace.
- **Length overflow**: a value longer than the target column's limit. Pull max length from
  metadata (`information_schema`) and check before importing.

### Report bad data, don't silently fix it

- Export offending records to a **separate file (CSV)** with the reason + an identifying column,
  then **roll back** — so the user fixes the **source** and re-runs. Don't quietly truncate or
  alter business data.
- Distinguish: technical "noise" (stray CR/LF) can be safely stripped on the export side;
  "content" errors (length overflow, business-invalid) must go back to the user to confirm.

## Transactions & rollback

- Load inside a **transaction**; any error → roll everything back (all-or-nothing) so the target
  DB is never left half-populated.
- **Dry-run mode**: always roll back (data/log inspection only), kept separate from the real
  commit mode.
- For large volumes you may commit in **batches/per table** to reduce memory — but note the
  recovery point is no longer global.

## Import ordering & masked failures

- Import in dependency order (parent tables before child tables due to foreign keys).
- **A failure at an early table aborts before later tables' bad data is ever seen** → "no error
  file" can mean "died earlier", **not** "clean data". Always read the log to learn which table
  failed and at which step.
- The log should clearly mark "starting import of table X" so you can trace the stop point.

## Collation / charset reconciliation (differences across RDBMSs)

- **SQL Server**: Unicode string literals need the `N'...'` prefix; without it, characters
  outside the collation's codepage become `?`. Some metadata functions (`OBJECT_ID`,
  `COL_LENGTH`) can silently return `NULL` when the collation doesn't match a non-ASCII
  identifier.
- **MySQL**: use a consistent charset/collation (usually `utf8mb4`) on the **connection,
  database, and columns**. Mismatched charset causes mojibake or an "Incorrect string value"
  error.
- Check the collation on **both ends before** migrating data with non-ASCII characters (names,
  addresses...).

## Performance

- A source table with **no index (heap)** or a large join → slow export. Consider a temporary
  index, or export by key/range.
- Avoid N+1 round-trips: read in batches, insert in batches (bulk/multi-row).

## Verify after changes

- After changing export/template logic: **re-run the tool so it regenerates the intermediate
  file, then import**, and **watch the log** — don't rely on "it compiled / no errors".
- Reconcile source vs target record counts, plus a few sample records with special characters.
- If the tool has multiple build configurations with copy-to-output assets (templates), build
  **every** configuration so a stale template doesn't cause a column-count mismatch.

See `references/checklist.md` for an add-a-column checklist and an import-failure debug table.
