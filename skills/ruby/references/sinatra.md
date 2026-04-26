# Sinatra Reference

Use this reference for hackathons, quick prototypes, lightweight JSON APIs, or microservices where Rails conventions would be overkill.

## App Structure

Always use modular style (`Sinatra::Base` subclass) — never classic style for anything that ships:

```ruby
# app.rb
class MyApp < Sinatra::Base
  register Sinatra::Contrib
  # ...
end
```

Recommended layout for a non-trivial Sinatra project:

```
app/
  routes/        # one file per resource: users.rb, posts.rb
  services/      # plain Ruby business logic
  serializers/   # JSON shaping
config.ru        # Rack entry point, mounts routes
Gemfile
```

Mount multiple route files in `config.ru`:

```ruby
require_relative 'app/routes/users'
require_relative 'app/routes/posts'

run Rack::URLMap.new(
  '/users' => UsersRoutes,
  '/posts' => PostsRoutes
)
```

## Routes

- Keep route blocks thin — one or two lines max; delegate to a service object immediately
- Use `halt` for early exits: `halt 422, json(error: 'Invalid input')`
- Group related routes in one `Sinatra::Base` subclass per resource

```ruby
class UsersRoutes < Sinatra::Base
  get '/' do
    json UserQuery.all
  end

  post '/' do
    user = CreateUser.call(parsed_body)
    halt 422, json(user.errors) unless user.valid?
    json user, status: 201
  end
end
```

## Filters & Helpers

- Use `before` filters for authentication, request parsing, and logging
- Use `after` filters for response headers (CORS, content-type)
- Define helpers in a `helpers do ... end` block or a dedicated `Helpers` module included via `helpers MyHelpers`

```ruby
before do
  content_type :json
  @payload = JSON.parse(request.body.read, symbolize_names: true) if request.post?
end
```

## Recommended Gems

| Purpose | Gem |
|---|---|
| JSON helpers | `sinatra-contrib` (`sinatra/json`) |
| Auto-reload in dev | `sinatra-contrib` (`sinatra/reloader`) |
| Param validation | `sinatra-contrib` (`sinatra/param`) |
| ORM | `sequel` (lighter than ActiveRecord) or `activerecord` standalone |
| Auth | `rack-jwt` or hand-rolled `before` filter |

## Testing

Use `rack-test` with RSpec:

```ruby
require 'rack/test'

RSpec.describe UsersRoutes do
  include Rack::Test::Methods

  def app = UsersRoutes

  it 'returns all users' do
    get '/'
    expect(last_response).to be_ok
    expect(JSON.parse(last_response.body)).to be_an(Array)
  end
end
```

## Hackathon Tips

- Start with a single `app.rb` file; split into `routes/` only when it exceeds ~100 lines
- Use `sinatra/reloader` so you don't restart the server on every change
- Pair with `sqlite3` + `sequel` for zero-setup persistence; swap to Postgres before demo day
- Keep secrets in a `.env` file loaded with `dotenv`; never hardcode credentials

## When to Choose Sinatra

- Hackathon or time-boxed prototype (< 48 hours)
- Simple webhook receiver or internal microservice
- You want full control over what middleware runs — no Rails magic
- Team is small (1–2 devs) and conventions would slow you down more than help
