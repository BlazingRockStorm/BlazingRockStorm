# React Native Deployment — iOS, Android, EAS, and OTA Updates

This reference covers building and distributing React Native apps to test environments. Read it alongside the main React Native skill.

The fastest path for most teams is **EAS Build + EAS Submit** (Expo's cloud build service). This reference covers EAS first, then the manual paths for bare projects or teams that want their own pipeline.

---

## EAS Build & Submit (recommended for Expo and bare)

EAS works for both Expo and bare React Native projects. It removes the need for local Xcode/Android Studio setup.

### One-time setup

```bash
npm install -g eas-cli
eas login
eas init                  # links the project to your Expo account
eas build:configure       # creates eas.json with development/preview/production profiles
```

### eas.json — typical profiles

```json
{
  "cli": { "version": ">= 12.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview"
    },
    "production": {
      "channel": "production",
      "autoIncrement": true
    }
  },
  "submit": {
    "production": {
      "ios":     { "appleId": "you@example.com", "ascAppId": "1234567890" },
      "android": { "serviceAccountKeyPath": "./play-service-account.json" }
    }
  }
}
```

### Build & submit

```bash
# Internal preview build — installable on registered devices via QR
eas build --profile preview --platform all

# Production build, then submit to App Store Connect + Play Console
eas build --profile production --platform all
eas submit --profile production --platform all
```

EAS handles signing automatically by generating and storing certificates and keystores in the cloud. To inspect or rotate them: `eas credentials`.

---

## iOS — TestFlight (manual path, bare or self-hosted)

Use this when you cannot or do not want to use EAS.

### Prerequisites

| Requirement | Where |
|---|---|
| Apple Developer Program ($99/yr) | developer.apple.com |
| App ID registered | Certificates, Identifiers & Profiles → Identifiers |
| Distribution certificate | Xcode → Settings → Accounts → Manage Certificates |
| App Store provisioning profile | Certificates, Identifiers & Profiles → Profiles |
| App created in App Store Connect | appstoreconnect.apple.com |
| Bundle ID matches across all three | `ios/{App}.xcodeproj`, App ID, App Store Connect |

### Build

```bash
# Bump version + build number first
# In ios/{App}/Info.plist:
#   CFBundleShortVersionString = 1.2.0
#   CFBundleVersion            = 42        ← strictly increasing per upload

# Install pods
cd ios && pod install && cd ..

# Archive via Xcode
xcodebuild -workspace ios/{App}.xcworkspace \
  -scheme {App} \
  -configuration Release \
  -archivePath build/{App}.xcarchive \
  archive

# Export IPA
xcodebuild -exportArchive \
  -archivePath build/{App}.xcarchive \
  -exportOptionsPlist ios/ExportOptions.plist \
  -exportPath build/ipa
```

### Upload

**Xcode Organizer (manual):** open `build/{App}.xcarchive` → Distribute App → App Store Connect → Upload.

**`xcrun altool` (CLI):**

```bash
xcrun altool --upload-app \
  --type ios \
  --file build/ipa/{App}.ipa \
  --apiKey YOUR_API_KEY_ID \
  --apiIssuer YOUR_ISSUER_ID
```

**Fastlane:**

```ruby
# fastlane/Fastfile
lane :beta do
  cocoapods(podfile: 'ios/Podfile')
  build_app(workspace: 'ios/{App}.xcworkspace', scheme: '{App}', export_method: 'app-store')
  upload_to_testflight(skip_waiting_for_build_processing: true)
end
```

### iOS signing checklist

- [ ] Bundle ID matches App ID and App Store Connect entry exactly
- [ ] Distribution certificate is valid and not expired
- [ ] Provisioning profile type: **App Store** for TestFlight, **Ad Hoc** for direct device install
- [ ] Build number (`CFBundleVersion`) strictly increases per upload
- [ ] Required capabilities (Push, Sign in with Apple, etc.) enabled in Xcode **and** App Store Connect
- [ ] `npm test` and `npx tsc --noEmit` pass before building

---

## Android — Play Console Internal Testing (manual path)

The **Internal Testing** track delivers builds to up to 100 testers immediately, no Play review.

### Prerequisites

| Requirement | Where |
|---|---|
| Google Play Developer account ($25 one-time) | play.google.com/console |
| App created in Play Console | Create app → complete store listing |
| Upload keystore (one-time) | See below |
| `gradle.properties` configured with keystore creds | `android/gradle.properties` (gitignored) |

### Generate the upload keystore (one-time)

```bash
keytool -genkeypair -v \
  -keystore android/app/upload-keystore.jks \
  -storetype JKS \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias upload
```

**Back up the `.jks` and passwords securely.** Losing them means you cannot sign updates under the existing app listing. Add to `.gitignore`:

```
android/app/upload-keystore.jks
android/gradle.properties
```

### Configure signing — android/gradle.properties

```properties
MYAPP_UPLOAD_STORE_FILE=upload-keystore.jks
MYAPP_UPLOAD_KEY_ALIAS=upload
MYAPP_UPLOAD_STORE_PASSWORD=your_store_password
MYAPP_UPLOAD_KEY_PASSWORD=your_key_password
```

### Wire signing — android/app/build.gradle

```groovy
android {
    signingConfigs {
        release {
            if (project.hasProperty('MYAPP_UPLOAD_STORE_FILE')) {
                storeFile     file(MYAPP_UPLOAD_STORE_FILE)
                storePassword MYAPP_UPLOAD_STORE_PASSWORD
                keyAlias      MYAPP_UPLOAD_KEY_ALIAS
                keyPassword   MYAPP_UPLOAD_KEY_PASSWORD
            }
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### Build

```bash
cd android

# App Bundle (required by Play Store)
./gradlew bundleRelease
# Output: android/app/build/outputs/bundle/release/app-release.aab

# APK (for sideloading / Firebase App Distribution)
./gradlew assembleRelease
# Output: android/app/build/outputs/apk/release/app-release.apk
```

### Upload

**Play Console (manual):** Internal Testing → Create new release → upload `.aab` → Review → Save.

**Fastlane:**

```ruby
lane :internal do
  gradle(task: 'bundle', build_type: 'Release', project_dir: 'android/')
  upload_to_play_store(track: 'internal', aab: 'android/app/build/outputs/bundle/release/app-release.aab')
end
```

### Android signing checklist

- [ ] `upload-keystore.jks` and `gradle.properties` are **not** in git
- [ ] `applicationId` in `build.gradle` matches the Play Console package name
- [ ] Release build uses upload keystore, not debug keystore
- [ ] `versionCode` increments with every upload
- [ ] Target SDK meets Play Store requirements (Google requires API 35 / Android 15 for new and updated apps as of August 2025)
- [ ] `npm test` and `npx tsc --noEmit` pass before building

---

## Firebase App Distribution (cross-platform alternative)

Useful for QA cycles before submitting to TestFlight / Play, and for testers without Apple/Google accounts.

```bash
npm install -g firebase-tools
firebase login

# iOS
firebase appdistribution:distribute \
  build/ipa/{App}.ipa \
  --app YOUR_FIREBASE_IOS_APP_ID \
  --groups "qa-team" \
  --release-notes "Build $(git rev-parse --short HEAD)"

# Android
firebase appdistribution:distribute \
  android/app/build/outputs/apk/release/app-release.apk \
  --app YOUR_FIREBASE_ANDROID_APP_ID \
  --groups "qa-team" \
  --release-notes "Build $(git rev-parse --short HEAD)"
```

App IDs are in Firebase Console → Project Settings → Your apps.

---

## OTA Updates

Over-the-air updates push new JS bundles + assets without going through the stores. Native code changes still require a full store release.

### EAS Update (recommended)

```bash
# In app.json / app.config.ts:
#   "runtimeVersion": { "policy": "appVersion" }
#   "updates": { "url": "https://u.expo.dev/<project-id>" }

eas update --branch production --message "Fix sign-in race condition"
```

Bind a build to a channel via `eas.json` `build.production.channel`. Channels map to branches at runtime, letting you ship preview/production updates from the same build pipeline.

### CodePush (Microsoft) — deprecating

App Center / CodePush is being retired. New projects should choose EAS Update or self-host (`expo-updates` against your own server). Existing CodePush integrations should be migrated.

### Rules of thumb

- Native module added/changed → **store release**, not OTA.
- JS-only bug fix → OTA is fine.
- Always increment `runtimeVersion` when native code changes — otherwise old builds receive incompatible JS bundles and crash.

---

## Version Management

| Place | What lives there |
|---|---|
| `package.json` `version` | Source of truth — semver `1.2.0` |
| iOS `CFBundleShortVersionString` | Mirrors `package.json` version |
| iOS `CFBundleVersion` | Strictly increasing build number |
| Android `versionName` | Mirrors `package.json` version |
| Android `versionCode` | Strictly increasing integer |
| Expo `app.config.ts` `version` / `ios.buildNumber` / `android.versionCode` | Single source for Expo |

For Expo projects, `eas.json` profile `autoIncrement: true` handles build numbers automatically.

For bare projects, automate with `react-native-version` or a simple script.

---

## CI/CD — GitHub Actions

### EAS Build via GitHub Actions

```yaml
name: EAS Build

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx tsc --noEmit
      - run: npm test
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --profile production --platform all --non-interactive --no-wait
```

Generate `EXPO_TOKEN` at expo.dev → Account Settings → Access Tokens.

### Bare RN Android build

```yaml
build-android:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-java@v4
      with: { distribution: 'temurin', java-version: '17' }
    - uses: actions/setup-node@v4
      with: { node-version: '20', cache: 'npm' }
    - run: npm ci
    - name: Decode keystore
      run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/upload-keystore.jks
    - name: Write gradle.properties
      run: |
        cat >> android/gradle.properties <<EOF
        MYAPP_UPLOAD_STORE_FILE=upload-keystore.jks
        MYAPP_UPLOAD_KEY_ALIAS=upload
        MYAPP_UPLOAD_STORE_PASSWORD=${{ secrets.KEYSTORE_STORE_PASSWORD }}
        MYAPP_UPLOAD_KEY_PASSWORD=${{ secrets.KEYSTORE_KEY_PASSWORD }}
        EOF
    - run: cd android && ./gradlew bundleRelease
```

**Store secrets** (`Settings → Secrets and variables → Actions`):
- `EXPO_TOKEN` (for EAS)
- `KEYSTORE_BASE64` — `base64 -i upload-keystore.jks | pbcopy`
- `KEYSTORE_STORE_PASSWORD`
- `KEYSTORE_KEY_PASSWORD`
- `APPLE_API_KEY_ID`, `APPLE_API_ISSUER_ID`, `APPLE_API_KEY_P8` (for iOS upload)

---

## Pre-release Checklist

- [ ] `npx tsc --noEmit` — no type errors
- [ ] `npm test` — all green
- [ ] `npm run lint` — clean
- [ ] Build number incremented (or `autoIncrement: true` in `eas.json`)
- [ ] iOS: signing config valid; provisioning profile not expired
- [ ] Android: upload keystore not in git; `applicationId` matches Play Console
- [ ] Release build tested on a physical device (simulator/emulator hides perf and signing issues)
- [ ] All env secrets loaded from secure storage / `EXPO_PUBLIC_*` (not hardcoded)
- [ ] Crash reporting configured for release (Sentry, Firebase Crashlytics)
- [ ] OTA: `runtimeVersion` bumped if native code changed
