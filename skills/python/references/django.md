# Django Reference

Use this reference for full-stack Django applications, Django REST Framework APIs, or when inheriting an existing Django project.

## Project Structure

Django is opinionated about project layout — follow its conventions:

```
project/
  manage.py
  config/              # project-level settings, urls, wsgi/asgi
    settings/
      base.py          # shared settings
      development.py
      production.py
    urls.py
    wsgi.py
  apps/
    users/             # one directory per Django app
      models.py
      views.py
      urls.py
      serializers.py   # if using DRF
      admin.py
      tests/
```

Split settings by environment (`base.py` + `development.py` + `production.py`) from day one — retrofitting this is painful.

## Models

- Keep models focused — one model per concept; avoid God models
- Always define `__str__` on every model
- Use `related_name` on `ForeignKey` / `ManyToManyField` for readable reverse lookups
- Add `db_index=True` to fields used in `filter()`/`order_by()` queries
- Use `select_related` (for `ForeignKey`) and `prefetch_related` (for `ManyToMany`) to prevent N+1 — equivalent to Ruby's `includes`

```python
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

## Views

- Prefer **class-based views** (CBV) for standard CRUD; use **function-based views** (FBV) for one-off logic that doesn't fit a CBV
- Use `get_object_or_404` instead of `.get()` + manual 404 raising
- Move business logic out of views into service functions or model methods — fat models / thin views

## Django REST Framework (DRF)

When the project uses DRF:
- Use `ModelSerializer` for standard CRUD; override `validate_<field>` and `validate` for custom validation
- Use `ViewSet` + `Router` for full CRUD resources; `APIView` for custom endpoints
- Authenticate with `JWTAuthentication` (`djangorestframework-simplejwt`) for stateless APIs
- Return consistent error responses — override `exception_handler` in settings if needed

```python
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'created_at']
        read_only_fields = ['created_at']
```

## URLs

- Use `app_name` in each app's `urls.py` for namespacing: `{% url 'users:profile' %}`
- Use `include()` in the root `urls.py` to compose app URLs
- Name every URL pattern — unnamed patterns break `reverse()` calls

## Background Tasks

- Use **Celery** with Redis or RabbitMQ for async tasks
- Name tasks descriptively: `send_welcome_email`, `process_payment`
- Keep tasks idempotent — they may retry; use a task-level lock or idempotency key when needed
- Use `django-celery-beat` for scheduled tasks

## Admin

- Register every model with `admin.site.register()` or a `ModelAdmin` subclass
- Add `list_display`, `search_fields`, and `list_filter` to every `ModelAdmin` — makes it useful immediately
- Never put business logic in admin actions — delegate to service functions

## Testing

```python
from django.test import TestCase, Client
from django.urls import reverse

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='quan', password='pass')

    def test_list_posts(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('posts:list'))
        self.assertEqual(response.status_code, 200)
```

- Use `TestCase` for DB tests (wraps each test in a transaction, then rolls back)
- Use `pytest-django` with `@pytest.mark.django_db` for pytest-style tests
- Use `factory_boy` for test data — equivalent to Ruby's FactoryBot

## Performance

- Use `django-debug-toolbar` in development to catch N+1 and slow queries
- Cache with `django.core.cache` — Redis backend for production
- Use `StreamingHttpResponse` for large file downloads
- Defer heavy computation to background tasks (Celery)

## When to Choose Django

- Full-stack project needing auth, admin, ORM, forms, and templates out of the box
- Team that benefits from strong conventions and an established ecosystem
- Inheriting an existing Django codebase
