# Flutter Deployment — iOS and Android Test Environments

This reference covers building Flutter apps for distribution to test environments. You have prior hands-on experience deploying to both iOS and Android.

---

## iOS — TestFlight

TestFlight is Apple's official test distribution channel. **Internal testers** (up to 100, by Apple ID) get builds instantly. **External testers** require a brief App Review (usually under 24 hours).

### Prerequisites

| Requirement | Where |
|---|---|
| Apple Developer Program ($99/yr) | developer.apple.com |
| App ID registered | Certificates, Identifiers & Profiles → Identifiers |
| Distribution certificate | Xcode → Settings → Accounts → Manage Certificates |
| App Store provisioning profile | Certificates, Identifiers & Profiles → Profiles |
| App created in App Store Connect | appstoreconnect.apple.com |
| Bundle ID matches across all three | `ios/Runner.xcodeproj`, App ID, App Store Connect |

### Build

```bash
# Ensure version and build number are incremented in pubspec.yaml
# version: 1.2.0+42   (format: semver+buildNumber)
# Build number must strictly increase with every upload

flutter build ipa --release

# IPA location: build/ios/ipa/Runner.ipa
# Archive location: build/ios/archive/Runner.xcarchive
```

### Upload

**Option A — Xcode Organizer (manual):**
1. Open `build/ios/archive/Runner.xcarchive` in Xcode Organizer
2. Click **Distribute App** → **App Store Connect** → **Upload**

**Option B — `xcrun altool` (CLI):**

```bash
xcrun altool --upload-app \
  --type ios \
  --file build/ios/ipa/Runner.ipa \
  --apiKey YOUR_API_KEY_ID \
  --apiIssuer YOUR_ISSUER_ID
```

**Option C — Fastlane (recommended for automation):**

```bash
# Gemfile
gem 'fastlane'

# Fastfile
lane :beta do
  build_app(scheme: 'Runner', export_method: 'app-store')
  upload_to_testflight(skip_waiting_for_build_processing: true)
end
```

```bash
fastlane beta
```

### Signing checklist

- [ ] Bundle ID in `ios/Runner.xcodeproj` matches the App ID and App Store Connect entry exactly
- [ ] Distribution certificate is valid and not expired (`flutter doctor` will not catch this)
- [ ] Provisioning profile type: **App Store** for TestFlight, **Ad Hoc** for direct device install
- [ ] For Ad Hoc: all tester device UDIDs are registered in the portal and included in the profile
- [ ] Version string is `MAJOR.MINOR.PATCH`; build number is a positive integer, strictly increasing
- [ ] All required capabilities (Push Notifications, Sign in with Apple, etc.) are enabled both in Xcode → Signing & Capabilities **and** in App Store Connect
- [ ] `flutter analyze` and `flutter test` pass before building

---

## Android — Play Console Internal Testing

The **Internal Testing** track delivers builds to up to 100 testers immediately, with no Play review. The **Closed (Alpha)** track supports larger groups with a brief opt-in.

### Prerequisites

| Requirement | Where |
|---|---|
| Google Play Developer account ($25 one-time) | play.google.com/console |
| App created in Play Console | Create app → complete store listing |
| Release keystore generated (one-time) | See below |
| `key.properties` configured | `android/key.properties` |

### Generate the upload keystore (one-time only)

```bash
keytool -genkeypair -v \
  -keystore android/app/upload-keystore.jks \
  -storetype JKS \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias upload
```

**Back up the `.jks` file and its passwords securely.** If lost, you cannot sign future updates under the same app listing. Add to `.gitignore`:

```
android/app/upload-keystore.jks
android/key.properties
```

### Configure signing — android/key.properties

```properties
storePassword=your_store_password
keyPassword=your_key_password
keyAlias=upload
storeFile=app/upload-keystore.jks
```

### Wire signing into android/app/build.gradle

```groovy
def keyPropertiesFile = rootProject.file('key.properties')
def keyProperties = new Properties()
keyProperties.load(new FileInputStream(keyPropertiesFile))

android {
    signingConfigs {
        release {
            keyAlias       keyProperties['keyAlias']
            keyPassword    keyProperties['keyPassword']
            storeFile      file(keyProperties['storeFile'])
            storePassword  keyProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig    signingConfigs.release
            minifyEnabled    true
            shrinkResources  true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### Build

```bash
# App Bundle is required for Play Store; APK is fine for direct sideloading

flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab

flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk
```

### Upload

**Play Console (manual):** Internal Testing → Create new release → Upload `.aab` → Review → Save.

**Fastlane (automation):**

```bash
# Appfile
json_key_file("fastlane/google-play-key.json")
package_name("com.example.myapp")

# Fastfile
lane :internal do
  gradle(task: 'bundle', build_type: 'Release')
  upload_to_play_store(track: 'internal')
end
```

### Android signing checklist

- [ ] `key.properties` and `.jks` file are **not** committed to git
- [ ] `applicationId` in `build.gradle` matches the Play Console package name exactly
- [ ] Release build uses the upload keystore, not the debug keystore
- [ ] `versionCode` increments with every upload (controlled by build number in `pubspec.yaml`)
- [ ] Target SDK meets Play Store requirements (Google requires API 35 / Android 15 for new and updated apps as of August 2025)
- [ ] `flutter analyze` and `flutter test` pass before building

---

## Firebase App Distribution (cross-platform alternative)

Firebase App Distribution works for both iOS and Android without App Store Connect or Play Console. Ideal for dev/QA cycles before store submission, and for testers without Apple or Google Play accounts.

### Setup

```bash
npm install -g firebase-tools
firebase login

dart pub global activate flutterfire_cli
flutterfire configure        # generates google-services.json and GoogleService-Info.plist
```

### Distribute

```bash
# Android
flutter build apk --release
firebase appdistribution:distribute \
  build/app/outputs/flutter-apk/app-release.apk \
  --app YOUR_FIREBASE_ANDROID_APP_ID \
  --groups "qa-team" \
  --release-notes "Build $(git rev-parse --short HEAD)"

# iOS
flutter build ipa --release
firebase appdistribution:distribute \
  build/ios/ipa/Runner.ipa \
  --app YOUR_FIREBASE_IOS_APP_ID \
  --groups "qa-team" \
  --release-notes "Build $(git rev-parse --short HEAD)"
```

Find your App IDs in the Firebase Console → Project Settings → Your apps.

---

## Version Management

Flutter uses a single field in `pubspec.yaml`:

```yaml
version: 1.2.0+42
#        ^^^^^  ^^
#        semver  build number
#                → versionCode on Android
#                → CFBundleVersion on iOS
```

- Increment **build number** on every upload to any platform (must be strictly increasing per platform)
- Increment **version string** for user-visible releases

Automate with the `cider` pub package:

```bash
dart pub global activate cider
cider bump build          # 1.2.0+42 → 1.2.0+43
cider bump patch          # 1.2.0+43 → 1.2.1+43
```

---

## CI/CD — GitHub Actions

```yaml
name: Build & Distribute

on:
  push:
    branches: [main]

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.22.0'
          channel: 'stable'
      - name: Write key.properties
        run: |
          echo "storePassword=${{ secrets.KEYSTORE_STORE_PASSWORD }}" > android/key.properties
          echo "keyPassword=${{ secrets.KEYSTORE_KEY_PASSWORD }}"    >> android/key.properties
          echo "keyAlias=upload"                                      >> android/key.properties
          echo "storeFile=app/upload-keystore.jks"                   >> android/key.properties
      - name: Decode keystore
        run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/upload-keystore.jks
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test
      - run: flutter build appbundle --release

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.22.0'
          channel: 'stable'
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test
      - run: flutter build ipa --release
      # Use Fastlane match to manage certificates and profiles in CI
      # fastlane match appstore --readonly
```

**Store secrets** (`Settings → Secrets and variables → Actions`):
- `KEYSTORE_BASE64` — base64-encoded `.jks` file: `base64 -i upload-keystore.jks | pbcopy`
- `KEYSTORE_STORE_PASSWORD`
- `KEYSTORE_KEY_PASSWORD`

---

## Pre-release Checklist

- [ ] `flutter analyze` — zero errors
- [ ] `flutter test` — all green
- [ ] `flutter doctor` — no issues with Xcode or Android toolchain
- [ ] Build number incremented in `pubspec.yaml`
- [ ] `flutter clean && flutter pub get` — clean build
- [ ] Release build tested on a physical device (not just simulator/emulator)
- [ ] All environment secrets loaded from secure storage (not hardcoded)
- [ ] iOS: signing configuration correct; provisioning profile valid and not expired
- [ ] Android: signed with upload keystore; `key.properties` not in git
- [ ] Crash reporting (Sentry / Firebase Crashlytics) configured for release builds
