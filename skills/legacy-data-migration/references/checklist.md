# Data migration — checklist & debug

## Adding a column to the export flow (ordinal template)

Edit **in sync, appending at the END** — wrong order shifts the entire mapping:

- [ ] Add the new column as the **last** column of the source SELECT.
- [ ] Add the **last line** to the mapping template, in the correct format
      (target name, type, flags, default, source name).
- [ ] Correct **emit type**: numeric → bare, empty → `NULL`; text → quoted, empty → `''`;
      has a default → use the default.
- [ ] Preserve the template's original **encoding + line endings**.
- [ ] Confirm the target column's **length / type** can hold the source data.
- [ ] Build **every configuration** that uses the template (if it's a copy-to-output asset).
- [ ] Re-run the tool → regenerate the intermediate file → import → read the log to confirm.

## Debugging import failures

| Symptom | Common cause |
| --- | --- |
| Aborts on "column count mismatch" / shifted columns | CR/LF embedded in a text field breaking the record line; or SELECT ↔ template got out of sync |
| Characters become `?` (SQL Server) | Missing `N'...'` prefix on a Unicode literal / wrong collation |
| Mojibake / "Incorrect string value" (MySQL) | Connection/column charset isn't consistently utf8mb4 |
| Length overflow | Value longer than the target column limit — cross-check `information_schema` |
| "No error file" but the import fails | Died at an earlier table → never reached the table with dirty data; read the log for the failing table |
| Import runs but the target DB is empty | Running in dry-run mode (always rolls back) |
| Stale Release template causes column shift | Release configuration wasn't rebuilt after editing the template |

## Log-reading procedure

1. Find the last "starting import of table X" marker → the table being processed when it failed.
2. Find the exception line right after it → the error class (column count / length / charset /
   foreign key).
3. If an error CSV was exported → open it for the record + identifying column + reason.
4. Fix the **source** (for content errors) or the export logic (for technical ones like CR/LF)
   → re-run.

## Normalizing a field before writing the intermediate file (pseudocode)

```
safe = raw
safe = safe.replace(delimiter, safeChar)     # delimiter inside the field
safe = safe.replace(CR, "").replace(LF, "")  # avoid breaking the record line
safe = safe.replace(dbEscapeChar, safeAlt)   # e.g. '\' in MySQL
# check length before emitting:
if len(safe) > targetColumnMaxLen: -> report an error (do NOT auto-truncate)
```

## Principles

- **Report errors, don't silently fix** business data.
- **All-or-nothing** inside a transaction; keep dry-run distinct from real commit.
- **Ordinal binding**: append at the end, never insert in the middle.
- **Verify by running for real + reading the log**, not just by compiling.
