import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.flowhive.app',
  appName: 'FlowHive',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    // For development, you can uncomment the following to test with your local backend
    // url: 'http://YOUR_LOCAL_IP:5173',
    // cleartext: true
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 2000,
      backgroundColor: '#ffffff',
      showSpinner: false
    }
  }
};

export default config;
