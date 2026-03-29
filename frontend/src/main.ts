import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { VueQueryPlugin } from '@tanstack/vue-query'
import { Capacitor } from '@capacitor/core'
import { App as CapacitorApp } from '@capacitor/app'
import App from './App.vue'
import router from './router'
import { useAppStore } from './stores/app'
import './style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(VueQueryPlugin)

if (Capacitor.getPlatform() === 'android') {
	CapacitorApp.addListener('backButton', ({ canGoBack }) => {
		if (canGoBack) {
			window.history.back()
			return
		}

		CapacitorApp.exitApp()
	})
}

const appStore = useAppStore(pinia)
appStore.bootstrap()

app.mount('#app')
