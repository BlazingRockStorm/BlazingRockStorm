---
name: mobile
description: Mobile development routing skill for React Native and Flutter. For React Native JavaScript/TypeScript projects, prefer pnpm as the package manager.
---

# Mobile Developer

You are assisting with mobile app development across iOS and Android.

## Framework Selection

| Situation | Action |
|---|---|
| No framework mentioned | Ask whether the app is React Native or Flutter before writing code |
| React Native project or user mentions Expo/RN | Load `react-native` skill |
| Flutter project or user mentions Dart | Load `flutter` skill |

## Skill Delegation

| Question type | Skill to apply |
|---|---|
| React Native app architecture, Expo, native modules | `react-native` skill |
| Flutter widget tree, Dart, pub tooling | `flutter` skill |
| Pure JavaScript runtime issues in RN code | `javascript` skill |
| TypeScript typing issues in RN code | `typescript` skill |
| Backend API design for mobile services | `backend` skill |

## Package Manager Rule (React Native JS/TS projects)

- Prefer **pnpm** over npm for JavaScript/TypeScript mobile projects
- Use `pnpm install` / `pnpm add` / `pnpm run <script>`
- Use `pnpm dlx` for one-off CLIs
