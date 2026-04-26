# FastAPI Reference

Use this reference for API-only Python services, high-performance async APIs, or when the project uses `fastapi` in its dependencies.

## Project Structure

```
project/
  main.py              # FastAPI app instance, router includes, lifespan
  routers/             # one file per resource: users.py, posts.py
  schemas/             # Pydantic models for request/response
  services/            # business logic — plain Python, no FastAPI dependency
  models/              # SQLAlchemy ORM models (if using a DB)
  dependencies/        # shared FastAPI Depends() callables
  core/
    config.py          # settings via pydantic-settings
    database.py        # DB engine and session factory
  tests/
```

Keep `routers/` thin — delegate to `services/` immediately. FastAPI routers are just HTTP plumbing.

## App Setup

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: connect DB, warm cache
    yield
    # shutdown: close connections

app = FastAPI(title='My API', lifespan=lifespan)
app.include_router(users.router, prefix='/users', tags=['users'])
```

Use `lifespan` (not deprecated `startup`/`shutdown` events) for resource management.

## Schemas with Pydantic

Pydantic is FastAPI's type validation layer — equivalent to Rails strong parameters + ActiveModel validations combined:

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=150)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {'from_attributes': True}  # enables ORM mode
```

- Separate schemas for input (`UserCreate`) and output (`UserResponse`) — never reuse the same model for both
- Use `model_config = {'from_attributes': True}` to deserialise SQLAlchemy models directly

## Routing

```python
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get('/', response_model=list[UserResponse])
async def list_users(db: Session = Depends(get_db)):
    return await UserService.list(db)

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return await UserService.create(db, data)

@router.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = await UserService.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user
```

## Dependency Injection

FastAPI's `Depends()` is the primary pattern for sharing resources — equivalent to Rails `before_action` + service injection:

```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # decode token, return user or raise 401
    ...
```

## Async vs Sync

- Use `async def` for route handlers that do I/O (DB queries, HTTP calls, file reads)
- Use `def` (sync) for CPU-bound work — FastAPI runs sync routes in a thread pool automatically
- Never mix blocking I/O inside `async def` — use `asyncio.to_thread()` if unavoidable

```python
# Good — async DB query
@router.get('/{id}')
async def get_item(id: int, db: AsyncSession = Depends(get_async_db)):
    return await db.get(Item, id)

# Good — blocking CPU work offloaded
@router.post('/process')
async def process(data: bytes):
    result = await asyncio.to_thread(heavy_cpu_function, data)
    return result
```

## Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={'detail': str(exc)})
```

Use `HTTPException` for standard HTTP errors; custom exception handlers for domain errors.

## Settings

Use `pydantic-settings` — equivalent to Rails credentials / environment config:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False

    model_config = {'env_file': '.env'}

settings = Settings()
```

## Testing

```python
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    response = client.post('/users/', json={'name': 'Quan', 'email': 'q@example.com', 'age': 30})
    assert response.status_code == 201
    assert response.json()['name'] == 'Quan'
```

- `TestClient` is synchronous even for async routes — no `asyncio` boilerplate needed in tests
- Use `httpx.AsyncClient` when you need truly async test execution
- Override dependencies in tests with `app.dependency_overrides`

```python
def override_get_db():
    yield test_db_session

app.dependency_overrides[get_db] = override_get_db
```

## When to Choose FastAPI

- Pure JSON API with no need for Django's admin, forms, or template engine
- Performance-sensitive service — FastAPI is one of the fastest Python frameworks
- You want automatic OpenAPI docs (`/docs`, `/redoc`) out of the box
- Modern async codebase with `asyncio`-native libraries (SQLAlchemy 2.0 async, `httpx`, etc.)
