# Capacitor Android Setup Guide

## ✅ Setup Complete!

Your FlowHive app is now configured with Capacitor for Android APK generation.

## 📱 Prerequisites

Before building the APK, you need:

1. **Android Studio** - [Download here](https://developer.android.com/studio)
2. **Java Development Kit (JDK) 17** - Usually installed with Android Studio
3. **Android SDK** - Installed via Android Studio

## 🚀 Quick Start

### Development Workflow

```bash
# Navigate to frontend directory
cd frontend

# Build Vue app and sync with Android
pnpm run build:android
```

This command will:
1. Build your Vue.js app
2. Sync the build to the Android project
3. Open Android Studio automatically

### Individual Commands

```bash
# Build the Vue app only
pnpm build

# Sync changes to Android
pnpm cap:sync

# Open Android Studio
pnpm cap:open:android
```

## 📦 Building the APK

### Option 1: Using Android Studio (Recommended)

1. Run `pnpm run build:android` to open Android Studio
2. Wait for Gradle sync to complete
3. Click **Build** → **Build Bundle(s) / APK(s)** → **Build APK(s)**
4. Once complete, click "locate" in the notification or find the APK at:
   ```
   frontend/android/app/build/outputs/apk/debug/app-debug.apk
   ```

### Option 2: Using Command Line

```bash
cd frontend/android
./gradlew assembleDebug  # For debug APK
# or
./gradlew assembleRelease  # For release APK (requires signing)
```

## 🔐 Release APK (Production)

For a signed release APK, you need to:

1. **Generate a keystore** (one-time setup):
   ```bash
   keytool -genkey -v -keystore flowhive-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias flowhive
   ```

2. **Configure signing** in `frontend/android/app/build.gradle`:
   ```gradle
   android {
       signingConfigs {
           release {
               storeFile file('../../flowhive-release-key.jks')
               storePassword 'your-store-password'
               keyAlias 'flowhive'
               keyPassword 'your-key-password'
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
               minifyEnabled false
               proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
           }
       }
   }
   ```

3. **Build release APK**:
   ```bash
   cd frontend/android
   ./gradlew assembleRelease
   ```

## ⚙️ Configuration

### App Details

Edit `frontend/capacitor.config.ts` to customize:

```typescript
{
  appId: 'com.flowhive.app',        // Change for your app
  appName: 'FlowHive',               // App name shown on device
  webDir: 'dist',                    // Build output directory
}
```

### App Icon and Splash Screen

1. Place your app icon at `frontend/android/app/src/main/res/`
2. Use Android Studio's Image Asset tool: **Right-click res → New → Image Asset**
3. For splash screen, edit `frontend/android/app/src/main/res/values/styles.xml`

### API Configuration

For production, update your API endpoint in [src/services/api.ts](frontend/src/services/api.ts) to use your deployed backend URL instead of localhost.

## 🔄 Making Changes

After updating your Vue app:

```bash
pnpm build && pnpm cap:sync
```

Then rebuild in Android Studio or use Gradle commands.

## 🐛 Troubleshooting

### Gradle Build Failures
- Ensure you have JDK 17 installed
- Clear Gradle cache: `cd android && ./gradlew clean`

### App Crashes on Device
- Check logcat in Android Studio: **View → Tool Windows → Logcat**
- Ensure API URLs are accessible from the device (not localhost)

### Changes Not Reflecting
- Always run `pnpm build` before syncing
- Clear app data on device: **Settings → Apps → FlowHive → Storage → Clear Data**

## 📱 Testing on Device

1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect device via USB
4. Run from Android Studio (click the green play button)

## 🎯 Next Steps

1. **Test the APK** on a physical Android device
2. **Configure app signing** for release builds
3. **Update API endpoints** for production
4. **Add app icon and branding**
5. **Prepare for Google Play Store** (if publishing)

## 📚 Resources

- [Capacitor Docs](https://capacitorjs.com/docs)
- [Android Developer Guide](https://developer.android.com/guide)
- [Vue.js with Capacitor](https://capacitorjs.com/docs/getting-started/with-ionic)
