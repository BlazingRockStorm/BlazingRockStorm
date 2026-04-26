# Frontend Deployment Reference

Covers Vercel, Netlify, and AWS Amplify. Load alongside the framework reference — deployment decisions depend on the framework in use.

## Platform Selection

| Situation | Platform |
|---|---|
| Next.js project, or want zero-config deployment | **Vercel** — Next.js native, best DX |
| Static site, SPA, or need form/function primitives without AWS | **Netlify** |
| Project already on AWS, needs AWS service integrations (Cognito, AppSync, S3) | **AWS Amplify** |

---

## Vercel

### Setup
- Connect GitHub repo → Vercel auto-detects framework and sets build command
- For non-Next.js projects, set manually in project settings:
  - React (Vite): build command `vite build`, output dir `dist`
  - Vue (Vite): same — `vite build` / `dist`

### Environment Variables
- Set in **Project Settings → Environment Variables**
- Scope per environment: Production, Preview, Development
- Prefix with `NEXT_PUBLIC_` (Next.js) or `VITE_` (Vite) to expose to the browser — never expose secrets this way
- Pull locally with `vercel env pull .env.local`

### Preview Deployments
- Every PR/branch gets a unique preview URL automatically — share with stakeholders before merging
- Override environment variables per branch in project settings when preview needs different API endpoints

### Custom Domains
- Add in **Project Settings → Domains**
- Vercel handles SSL automatically via Let's Encrypt
- For apex domain (`example.com`): use Vercel's nameservers or add `A` record pointing to Vercel's IP

### Vercel CLI
```bash
npm i -g vercel
vercel          # deploy to preview
vercel --prod   # deploy to production
vercel env pull # sync env vars locally
vercel logs     # tail production logs
```

### Edge Functions vs Serverless Functions
- **Serverless Functions**: `api/` directory, Node.js runtime, full npm ecosystem
- **Edge Functions**: `middleware.ts` (Next.js) or `api/` with `export const runtime = 'edge'`; faster cold starts, limited APIs — use for auth checks, redirects, geolocation

---

## Netlify

### Setup
- Connect GitHub repo → Netlify auto-detects build settings for common frameworks
- Manual config via `netlify.toml` at repo root (preferred over UI for reproducibility):

```toml
[build]
  command = "npm run build"
  publish = "dist"         # or "build" for Create React App

[build.environment]
  NODE_VERSION = "20"

# SPA fallback — required for client-side routing
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### SPA Routing — Critical
Without the redirect rule above, refreshing any route other than `/` returns a 404. Always add it for React/Vue SPAs.

### Environment Variables
- Set in **Site Settings → Environment Variables**
- Prefix with `VITE_` (Vite) or `REACT_APP_` (CRA) to expose to the browser
- Pull locally with Netlify CLI: `netlify env:list`

### Netlify Functions
Serverless functions live in `netlify/functions/`:

```ts
// netlify/functions/hello.ts
import type { Handler } from '@netlify/functions'

export const handler: Handler = async (event) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello' }),
  }
}
```

Available at `/.netlify/functions/hello` — or use redirects to expose at a cleaner path.

### Deploy Previews
- Every PR gets a preview URL — same as Vercel
- Use **branch deploys** for staging environments with their own env vars

### Netlify CLI
```bash
npm i -g netlify-cli
netlify dev          # local dev server with Functions support
netlify deploy       # deploy to draft URL
netlify deploy --prod  # deploy to production
netlify env:list     # list environment variables
```

---

## AWS Amplify

### When to Use
Amplify is the right choice when the project needs AWS service integrations: Cognito auth, AppSync (GraphQL), S3 uploads, Lambda, or when the team already manages infrastructure on AWS.

### Hosting Setup (Amplify Console)
- Connect GitHub repo in **AWS Console → Amplify → New App → Host web app**
- Amplify auto-detects build settings; override with `amplify.yml` at repo root:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: dist    # or build for CRA
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
```

### SPA Routing — Critical
Same issue as Netlify — add a rewrite rule in **Amplify Console → Rewrites and Redirects**:

| Source | Target | Type |
|---|---|---|
| `</^[^.]+$\|\.(?!(css\|gif\|ico\|jpg\|js\|png\|txt\|svg\|woff\|woff2\|ttf\|map\|json)$)([^.]+$)/>` | `/index.html` | 200 (Rewrite) |

Or configure via `amplify.yml` `customHeaders` / redirect rules.

### Environment Variables
- Set in **Amplify Console → Environment Variables** per branch
- Prefix with `VITE_` or `REACT_APP_` to expose to the browser
- Amplify injects them at build time — not at runtime like a server

### Branch Deployments
- `main` → production
- Any other branch → preview environment with its own URL
- Configure branch-specific env vars for staging API endpoints

### Custom Domains
- Set in **Amplify Console → Domain Management**
- For Route 53 domains: Amplify configures DNS automatically
- For external DNS: add the CNAME records Amplify provides

### Amplify CLI (for backend services)
```bash
npm i -g @aws-amplify/cli
amplify init           # initialise backend in project
amplify add auth       # add Cognito auth
amplify add storage    # add S3 storage
amplify push           # deploy backend changes
amplify status         # show backend resource status
```

### Amplify vs Vercel/Netlify Trade-offs

| | Vercel | Netlify | AWS Amplify |
|---|---|---|---|
| DX / setup speed | Best | Very good | Moderate |
| Next.js support | Native | Good | Good |
| AWS integrations | Via API calls | Via API calls | Native |
| Pricing model | Per request/GB | Per build minute/GB | Per build minute/GB + AWS costs |
| Best for | Next.js, speed | Static/SPA, forms | AWS-native stacks |
