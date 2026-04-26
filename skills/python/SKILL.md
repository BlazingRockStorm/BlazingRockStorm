---
name: python
description: Python development assistance for a developer with basic proficiency and strong Ruby background. Covers Python idioms, virtual environments, testing, and type hints. Supports Django (default web framework), FastAPI, and pure Python. Relates concepts to Ruby analogues where helpful.
---

# Python

You are assisting a developer with basic Python proficiency who has strong Ruby background. Explain non-obvious Python concepts by relating them to Ruby equivalents where it helps build mental models.

## Framework Selection

| Situation | Action |
|---|---|
| No framework mentioned, or existing Django project | Load `references/django.md` **(default)** |
| User says "Django" | Load `references/django.md` |
| API-only, user says "FastAPI", or project uses `fastapi` in `requirements.txt` | Load `references/fastapi.md` |
| Script, CLI tool, library, data processing, or user says "pure Python" | Use `SKILL.md` core only — do not load any framework reference |
| Another framework (Flask, Tornado, etc.) | Apply core Python principles; state you have no dedicated reference and ask if the user wants to provide context |

**When a framework is involved**, confirm before writing code:
_"Using Django (default) — let me know if you want FastAPI or pure Python instead."_

---

## Codebase Adaptation

Before writing or suggesting anything on an existing project, read the project context and adapt accordingly.

### Step 1 — Detect constraints

| File | What to read |
|---|---|
| `pyproject.toml` / `setup.py` / `setup.cfg` | Python version requirement, project metadata |
| `.python-version` / `.tool-versions` | Target Python version — never suggest features above it |
| `requirements.txt` / `requirements/*.txt` / `Pipfile` | Available packages — don't suggest adding ones that overlap |
| `pyproject.toml` `[tool.ruff]` / `.flake8` / `setup.cfg [flake8]` | Enforced lint rules — follow them |
| `mypy.ini` / `pyproject.toml` `[tool.mypy]` | Type checking strictness |
| Existing source files | Style: f-strings vs `.format()`, type hints usage, docstring style, test framework |

### Step 2 — Classify the project

| Classification | Signals | Approach |
|---|---|---|
| **Greenfield** | No source files, empty `requirements.txt` | Apply defaults from this skill |
| **Active project** | Has source, recent commits, modern Python | Match existing style; suggest improvements only when asked |
| **Legacy project** | Python 2, `print` statements, `unicode_literals`, old-style classes | Stay within Python 2 patterns if that is the target; flag migration only if asked |
| **Constrained** | No pip access, vendored dependencies, air-gapped | Never suggest installing packages; work with what is available |

### Step 3 — State what you found

_"Python 3.11, Ruff for linting, mypy strict — I'll use modern type hints and avoid deprecated patterns."_

---

## Core Principles

- Follow PEP 8: 4-space indentation, `snake_case` for variables/functions, `PascalCase` for classes
- Use f-strings for interpolation: `f"Hello, {name}!"` — equivalent to Ruby's `"Hello, #{name}!"`
- Prefer explicit over implicit — Python's `import` system makes dependencies visible
- Use `with` statements for resource management (files, connections) — equivalent to Ruby's block-based `open`
- Never use mutable default arguments: `def foo(items=None)` then `items = items or []`

## Ruby → Python Mental Model

| Ruby | Python equivalent |
|---|---|
| Block `{ |x| x * 2 }` | Lambda `lambda x: x * 2` or list comprehension `[x * 2 for x in items]` |
| `Enumerable#map` | `map(fn, iterable)` or `[fn(x) for x in iterable]` |
| `Enumerable#select` | `filter(fn, iterable)` or `[x for x in items if condition]` |
| `Enumerable#reduce` | `functools.reduce(fn, iterable)` |
| `nil` | `None` |
| `Symbol` | `str` (Python has no symbol type — use `Enum` for closed sets) |
| `Hash` | `dict` |
| `require` | `import` |
| `Struct` / `Data` | `dataclasses.dataclass` or `typing.NamedTuple` |
| `begin/rescue` | `try/except` |
| `frozen_string_literal` | Implicit — strings are immutable by default in Python |
| Mixin / module | Multiple inheritance or `Protocol` (for duck typing) |

## Language Features

- **List / dict / set comprehensions**: prefer over `map`/`filter` for readability
  ```python
  active_names = [u.name for u in users if u.active]
  counts = {k: len(v) for k, v in groups.items()}
  ```
- **Unpacking**: `first, *rest = items` — equivalent to Ruby's `first, *rest = items`
- **f-strings**: `f"{value:.2f}"` supports format specs inline
- **`dataclasses`**: use `@dataclass` for value objects — equivalent to Ruby's `Data.define`
  ```python
  from dataclasses import dataclass

  @dataclass(frozen=True)
  class Point:
      x: float
      y: float
  ```
- **`Enum`**: use for closed sets of values instead of string constants
- **Walrus operator** (3.8+): `if (n := len(data)) > 10:` — assigns and tests in one expression

## Type Hints

- Add type hints to all new code; leave existing untyped code alone unless asked
- Use `from __future__ import annotations` for forward references in Python < 3.10
- Prefer `X | Y` union syntax (3.10+) over `Union[X, Y]`
- Use `Optional[X]` (or `X | None`) for nullable values
- Run `mypy` or `pyright` in CI; configure strictness in `pyproject.toml`

```python
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}! " * times
```

## Virtual Environments & Tooling

- Always work inside a virtual environment: `python -m venv .venv && source .venv/bin/activate`
- **pip**: `pip install -r requirements.txt`; pin versions with `==` in `requirements.txt`
- **uv**: modern, fast alternative to pip + venv — use if the project already has it
- **Ruff**: preferred linter and formatter (replaces Flake8 + Black + isort in one tool)
- **pyproject.toml**: prefer over `setup.py` for new projects

## Testing

- Default to **pytest** — equivalent to RSpec in Ruby
- Use `pytest.fixture` for setup — equivalent to RSpec's `let` / `before`
- Use `pytest.mark.parametrize` for data-driven tests — equivalent to RSpec shared examples
- Mock with `unittest.mock.patch` or `pytest-mock`'s `mocker` fixture
- Structure: one test file per module (`test_users.py` for `users.py`); prefix test functions with `test_`

```python
import pytest

@pytest.fixture
def user():
    return User(name='Quan', active=True)

def test_user_is_active(user):
    assert user.active
```

## Code Review Checklist

Flag these when reviewing:
1. Mutable default argument: `def foo(items=[])` — replace with `None` sentinel
2. Bare `except:` — should be `except Exception:` or narrower
3. `type(x) == SomeClass` — replace with `isinstance(x, SomeClass)`
4. `print()` left in non-CLI code
5. Missing `with` for file/resource handling

## Version Guidance

- **Python 3.8**: walrus operator (`:=`), `typing.Protocol`, `positional-only` params (`/`)
- **Python 3.9**: `list[str]` / `dict[str, int]` built-in generics (no `from typing import List`)
- **Python 3.10**: `match/case` pattern matching (equivalent to Ruby's `case/in`), `X | Y` union syntax
- **Python 3.11**: `ExceptionGroup`, `tomllib` built-in, faster CPython
- **Python 3.12**: `@override` decorator, `type` statement for type aliases, f-string improvements
