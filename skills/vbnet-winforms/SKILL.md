---
name: vbnet-winforms
description: >-
  Conventions and patterns for reading, modifying, and extending legacy VB.NET
  WinForms apps on the .NET Framework (WinExe, x86/AnyCPU): file structure,
  Option Strict, #Region, XML docs, non-ASCII source encoding, ADO.NET with a
  static DB-access class + manual transactions, SQL execution helpers,
  My.Settings, file logging, and multi-configuration msbuild. Also covers using
  the skill in read-only mode to understand VB source before porting/rewriting it
  in another language. Use when working with legacy VB.NET code. Triggers: .vb /
  .vbproj / .Designer.vb files, "VB.NET", "VB.net", "WinForms", "Windows Forms",
  "Option Strict", ".NET Framework", "port VB", "rewrite VB". For data
  migration/ETL tools, pair with the data-migration skill.
metadata:
  type: reference
---

# VB.NET WinForms (legacy .NET Framework)

Conventions common to **VB.NET WinForms applications on the .NET Framework**. Goal:
when reading, modifying, or extending such code, follow the existing legacy style
instead of imposing modern .NET idioms (async/await, EF Core, DI) onto an old codebase.

> This is *general* guidance. Always read the current code first and follow the repo's
> actual conventions — the items below are sensible defaults, not hard rules.

## Two modes of use

- **In-place work** (modify/extend the existing app): match the legacy style below.
- **Read-only comprehension → port** (understand the VB, then build new software in
  another language): use the same conventions to *decode intent*, but see
  [Reading & porting](#reading--porting-to-another-language) for separating essential
  behavior from incidental legacy artifacts. Do **not** carry legacy idioms into the
  new codebase.

## Technical context

- **VB.NET, .NET Framework (4.x), `WinExe`** (WinForms) — not .NET Core/5+.
- Multiple build configurations (`Debug`/`Release`) and targets (`x86`/`AnyCPU`/`x64`).
- `Option Strict`/`Option Infer`/`Option Explicit` may be set at the project level
  (`.vbproj`) *and* overridden at the top of each file. Check both; honor the stricter
  setting when writing new code.

## Code conventions (follow the repo)

1. **File header:** `Option ...` directives (if the file uses them), then `Imports`.
2. **Non-ASCII comments/encoding.** Old .vb files may be saved in a non-UTF-8 codepage
   (Shift-JIS, GB2312, ...), so comments render as mojibake when read as UTF-8. **Do not
   "fix" the mojibake and do not change the file encoding** — it is an encoding artifact,
   not a bug; changing it corrupts every comment and can break string literals. Prefer
   ASCII for new comments, or match the file's existing language.
3. **`#Region ... #End Region`** groups related members. Put new members in a sensible region.
4. **XML docs `''' <summary>`** on public members. Old code often leaves the body empty
   but keeps the scaffold.
5. **Single return variable** with a consistent name (e.g. `retAns`/`result`), initialized
   at the top, one `Return` at the end — instead of multiple return points.
6. **Explicit `ByVal`/`ByRef`** on parameters (old VB style).
7. **`Call Sub(...)`** is still used for Sub invocations — stay consistent with the file.
8. **`#If DEBUG Then ... #End If`** for logging/diagnostics that only run in debug builds.
9. Naming: PascalCase for public, camelCase/abbreviations for locals. **Do not mass-rename.**
10. **`Option Strict Off`** (common in old projects) permits late-binding and implicit
    conversions → watch for runtime errors the compiler won't catch. If a file is already
    `Option Strict On`, keep it that way.

## ADO.NET: static DB access + transactions

A very common pattern: **a static class holding a shared connection + transaction**.

- A `DbAccess`-style class with `Shared Conn` + `Shared Tran`.
- `ConnStart(connStr)` opens the connection and calls `BeginTransaction`; work runs inside
  `Try/Catch/Finally`; `Finally` calls `ConnEnd(success)` to **commit on success, roll back
  on failure**.
- An optional `ConnCommit` commits mid-run and then `BeginTransaction` again (batching).
- A safe "dry-run" mode: `ConnEnd` checks a flag (radio button) — commit only when the user
  chooses to; default to rollback so real data is never touched.
- **Execution helpers** wrap `ExecuteNonQuery`/`DataAdapter.Fill`, log internally, and
  **return a sentinel error value instead of throwing** (`DataSet` = `Nothing`, `Integer`
  = `-1`, `Boolean` = `False`). → **Always check the error value** before use
  (`If ds Is Nothing ...`).
- **Connection strings** are built manually with `String.Format` from a template + values
  from `My.Settings.*`, with Test/Production environments kept separate. **Never hardcode
  credentials in source.**
- **SQL-injection safety:** use `SqlParameter`/`MySqlParameter`/... for all user-supplied
  values — never string concatenation.

## File logging

- Logs are written to text files with a fixed encoding (UTF-16 or UTF-8-BOM), appended,
  with a timestamp. Called inside `Catch` to record `ex.ToString`.
- Log paths/directories live in `Shared` variables/constants, relative to the run directory.
- DML logging records both the SQL and the **parameters** for traceability.

## Build & assets

- Build each configuration: `msbuild <Project>.vbproj /p:Configuration=Debug /p:Platform=x86`
  (repeat for `Release` and every platform in use). Or open the solution in Visual Studio.
- Assets with `CopyToOutputDirectory=Always` (templates, config) are copied into **each**
  output folder → **build every configuration you will run**, otherwise the asset in an
  unbuilt configuration is stale and causes runtime errors.
- Don't switch to async, `Using`, EF, DI, or flip `Option Strict` globally for
  "cleanliness" — stay consistent with the legacy style unless explicitly asked.

## ADO.NET & DB pitfalls

- **Collation/charset with non-ASCII:** Unicode string literals in SQL Server need the
  `N'...'` prefix, otherwise characters become `?`; some metadata functions may silently
  return `NULL`. MySQL needs a consistent charset (utf8mb4) on the connection and columns.
- **Helpers return sentinel error values instead of throwing** → easy to forget the
  `Nothing`/`-1`/`False` check.
- `DataAdapter.Fill` won't throw where the helper has already caught the exception → check
  the `DataSet` before `.Tables(0)`.

## Reading & porting to another language

When the goal is to **understand the VB and rebuild in a different language** (C#, Python,
Java, etc.), use this skill to decode intent — but treat most legacy idioms as *incidental*,
not as behavior to reproduce.

**Separate essential behavior from legacy artifacts:**

| Essential — capture in the port | Incidental — drop, replace with target idiom |
| --- | --- |
| Business rules, validation, data transforms | `Option Strict`/`#Region`/`Call` syntax |
| SQL queries & schema assumptions | Static shared `Conn`/`Tran` globals |
| Transaction boundaries (what is atomic) | `retAns` single-return style |
| Commit/rollback & dry-run semantics | Sentinel error values (use exceptions/`Result`) |
| Encoding requirements of files it reads/writes | Mojibake comments (re-document in English) |
| Type/length/`NULL` handling rules | `My.Settings` file → use env/secret store |
| Import/processing order & dependencies | WinForms event plumbing / `.Designer.vb` |

**How to read for a port:**

1. **Map the entry points and control flow first** — form load, button handlers, the main
   worker Sub/Function. `.Designer.vb` is generated UI layout; skip it for logic.
2. **Extract SQL and schema** — the queries encode the real data model; preserve them.
3. **Note transaction & dry-run semantics precisely** — what commits together, what rolls
   back, when nothing is written. This is behavior, port it faithfully.
4. **Decode, don't copy, the idioms** — a static shared connection becomes a proper
   connection/unit-of-work in the target; sentinel returns become exceptions or a `Result`
   type; `#If DEBUG` becomes the target's logging levels.
5. **Re-document mojibake comments** — translate/restate intent in the new codebase's
   language; don't carry the encoding forward.
6. **Preserve external contracts** — file formats, encodings, DB schema, and integration
   points the app shares with other systems must stay byte-compatible unless you also
   migrate the other side.
7. **Verify against the original** — run both on the same input and diff outputs; legacy
   quirks (rounding, trimming, default values) are easy to miss.

When the VB app is a data-migration/ETL tool, the process behavior (intermediate files,
column mapping, dirty-data handling, import order) is the part worth porting carefully —
see the **legacy-data-migration** skill for that.

See `references/patterns.md` for concrete, copyable code snippets.
