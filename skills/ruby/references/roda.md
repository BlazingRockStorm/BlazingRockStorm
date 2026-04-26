# Roda Reference

Use this reference when you need a composable routing tree, fine-grained plugin control, or are building a performance-critical Rack application.

## Core Concept: Routing Tree

Roda's routing is a tree, not a flat list. Routes are matched top-down; once a branch matches, only that branch executes. This eliminates ambiguous routes and makes the flow explicit.

```ruby
route do |r|
  r.on 'users' do
    r.is do
      r.get  { UserSerializer.collection(UserQuery.all) }
      r.post { CreateUser.call(r.params) }
    end

    r.on Integer do |id|
      @user = UserQuery.find(id)
      r.halt(404, '{"error":"not found"}') unless @user

      r.is do
        r.get    { UserSerializer.one(@user) }
        r.patch  { UpdateUser.call(@user, r.params) }
        r.delete { DeleteUser.call(@user) }
      end
    end
  end
end
```

## App Structure

```
app.rb              # Roda subclass, plugin loading, top-level route block
routes/             # Optional: extracted route branches required into app.rb
services/           # Plain Ruby business logic
config.ru           # run MyApp.freeze.app
Gemfile
```

For larger apps, extract branches into route files and `r.run` them:

```ruby
# routes/users.rb
class MyApp
  route(:users) do |r|
    # ...
  end
end

# app.rb — in the main route block:
r.on('users') { r.run UsersRoutes }
```

## Plugin Loading

Load only what you need — this is Roda's main advantage over Sinatra:

```ruby
class MyApp < Roda
  plugin :json               # auto Content-Type + JSON serialisation
  plugin :json_parser        # parse JSON request bodies into r.params
  plugin :halt               # r.halt shorthand
  plugin :request_headers    # r.headers convenience
  plugin :common_logger      # dev logging
  plugin :error_handler      # unified rescue block
  plugin :not_found          # catch-all 404 handler
end
```

Never `plugin :all` — always be explicit.

## Request & Response

```ruby
# Reading
r.params          # merged query + body params (after :json_parser)
r.env             # raw Rack env
r.headers['X-Api-Key']

# Early exits
r.halt 422, { error: 'invalid' }.to_json
r.redirect '/new-path', 301

# Response
response.status = 201
response['X-Custom'] = 'value'
```

## Error Handling

```ruby
plugin :error_handler do |e|
  case e
  when ActiveRecord::RecordNotFound then r.halt 404, { error: e.message }.to_json
  when ArgumentError                then r.halt 422, { error: e.message }.to_json
  else
    r.halt 500, { error: 'internal server error' }.to_json
  end
end
```

## Testing

Roda apps are plain Rack apps — use `rack-test` with RSpec:

```ruby
require 'rack/test'

RSpec.describe MyApp do
  include Rack::Test::Methods

  def app = MyApp.freeze.app

  it 'returns users' do
    get '/users'
    expect(last_response.status).to eq 200
    expect(JSON.parse(last_response.body)).to be_an(Array)
  end
end
```

## Performance Tips

- Call `.freeze.app` in `config.ru` — Roda optimises the routing tree at freeze time
- Avoid loading plugins inside route blocks; load all plugins at class definition time
- Use `plugin :caching` for HTTP cache headers on read-heavy endpoints
- Benchmark with `rack-mini-profiler` or `stackprof` before optimising

## Roda vs Sinatra Decision

| Sinatra | Roda |
|---|---|
| Flat route list, familiar DSL | Tree routing, explicit branch matching |
| Good for hackathons, quick APIs | Good for production microservices |
| `sinatra-contrib` for extras | Fine-grained plugin loading |
| Classic or modular style | Always class-based |

## When to Choose Roda

- You need the routing tree for deeply nested resources without route explosion
- Performance matters — Roda has significantly lower overhead than Sinatra
- You want precise control over which middleware and features are loaded
- Building a production microservice expected to scale
