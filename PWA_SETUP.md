# PWA Setup Guide for Flowhive

This guide explains how your Progressive Web App (PWA) is configured and how to ensure smooth installation for users.

## ✅ What's Been Implemented

### 1. **PWA Plugin Configuration**
- Installed `vite-plugin-pwa` for automatic PWA generation
- Service worker configured with automatic updates
- Offline caching strategy implemented

### 2. **App Manifest**
- App name, description, and theme color defined
- Icons configured for different sizes (192x192, 512x512)
- Display mode set to "standalone" for app-like experience

### 3. **Icons & Assets**
- Created placeholder icons (you should replace these with your actual branding)
- Favicon and Apple touch icons configured
- SVG format for scalability

### 4. **Install Prompts**
- Custom install prompt component that appears for eligible users
- Update notification when new version is available
- Dismissal logic to avoid annoying users

### 5. **Meta Tags**
- Proper viewport settings for mobile
- Theme color for browser chrome
- Apple-specific meta tags for iOS installation

## 🎨 Customizing Icons

Replace the placeholder icons in `/frontend/public/` with your actual brand icons:

1. **favicon.svg** (32x32) - Browser tab icon
2. **icon-192x192.svg** (192x192) - Android install icon
3. **icon-512x512.svg** (512x512) - High-res app icon
4. **apple-touch-icon.svg** (180x180) - iOS home screen icon

You can use tools like:
- [Figma](https://figma.com) - Design your icons
- [Favicon.io](https://favicon.io) - Generate from text/image
- [RealFaviconGenerator](https://realfavicongenerator.net/) - Generate all sizes

## 🧪 Testing Your PWA

### Development Testing
```bash
cd frontend
pnpm dev
```

The PWA features work in development mode. Open Chrome DevTools:
1. Go to **Application** tab
2. Check **Manifest** to verify your app manifest
3. Check **Service Workers** to see if it's registered

### Production Testing
```bash
cd frontend
pnpm build
pnpm preview
```

Then test installation:
1. Open in Chrome (Desktop or Android)
2. Look for the install icon in the address bar
3. Click to install the app

### Lighthouse Audit
Run a PWA audit to check your score:
1. Open Chrome DevTools
2. Go to **Lighthouse** tab
3. Select "Progressive Web App" category
4. Click "Generate report"

Aim for a score of 90+ in all categories.

## 📱 Platform-Specific Behavior

### Android
- Users see an "Add to Home Screen" prompt automatically
- Install banner appears after criteria are met
- App opens in fullscreen mode
- Back button navigates within the app

### iOS (Safari)
- No automatic install prompt
- Users must manually: Share → Add to Home Screen
- Your custom install prompt won't show on iOS
- Still works as a standalone app once installed

### Desktop (Chrome, Edge, etc.)
- Install icon appears in address bar
- Users can install from browser menu
- App opens in its own window
- Integrated with OS (appears in app launcher)

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Replace placeholder icons with actual brand icons
- [ ] Test on real devices (Android phone, iPhone, desktop)
- [ ] Run Lighthouse audit and fix any issues
- [ ] Verify HTTPS is enabled (required for PWA)
- [ ] Test offline functionality
- [ ] Check install prompts appear correctly
- [ ] Verify service worker updates properly

## 📊 PWA Install Criteria

For the browser to show install prompts, your app must:

1. ✅ Be served over HTTPS
2. ✅ Have a valid web app manifest
3. ✅ Register a service worker
4. ✅ Have at least one icon
5. ⚠️ **User engagement**: User must visit at least twice with 5 minutes between visits

The last requirement is automatic - just means users won't see the prompt on their first visit.

## 🔧 Troubleshooting

### Install prompt doesn't appear
- Check HTTPS is enabled
- Open DevTools → Application → Manifest (should show no errors)
- Check Console for any errors
- Wait for user engagement criteria (revisit after 5 minutes)

### Service worker not updating
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Clear site data in DevTools → Application → Storage
- Check that `autoUpdate` is enabled in vite.config.ts

### App not working offline
- Check Service Worker is installed and activated
- Verify caching strategy in vite.config.ts
- Check Network tab in DevTools (should show "from ServiceWorker")

## 🔐 Backend Considerations

Your backend needs to support PWA:

1. **CORS Headers**: Allow requests from your app domain
2. **HTTPS**: Required for service workers
3. **Cache Headers**: Set appropriate cache control headers
4. **API Versioning**: Handle offline/online sync gracefully

## 📈 Analytics

Consider tracking PWA metrics:
- Installation rate
- Standalone vs browser usage
- Offline usage patterns
- Update adoption rate

You can add these to your existing analytics service.

## 🎯 Next Steps

1. **Replace icons** with your brand assets
2. **Test thoroughly** on different devices
3. **Deploy to production** with HTTPS
4. **Monitor** installation and usage metrics
5. **Iterate** based on user feedback

## 🔗 Resources

- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [Vite PWA Plugin](https://vite-pwa-org.netlify.app/)
- [Web App Manifest Spec](https://w3c.github.io/manifest/)
- [Workbox Documentation](https://developers.google.com/web/tools/workbox)

---

Your app is now ready to be installed as a native-like application! Users can add it to their home screen and use it offline.
