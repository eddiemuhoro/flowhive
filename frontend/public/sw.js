/**
 * Custom Service Worker for Flowhive PWA
 * Handles push notifications
 */

// Install event
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...')
  self.skipWaiting()
})

// Activate event
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...')
  event.waitUntil(self.clients.claim())
})

// Push notification event
self.addEventListener('push', (event) => {
  console.log('Push notification received', event)

  if (!event.data) {
    return
  }

  const data = event.data.json()

  const options = {
    body: data.message || 'You have a new notification',
    icon: data.icon || '/icon-192x192.svg',
    badge: data.badge || '/icon-192x192.svg',
    tag: data.tag || 'notification',
    data: {
      url: data.url || '/',
      ...data
    },
    requireInteraction: false,
    vibrate: [200, 100, 200]
  }

  event.waitUntil(
    self.registration.showNotification(
      data.title || 'Flowhive',
      options
    )
  )
})

// Notification click event
self.addEventListener('notificationclick', (event) => {
  console.log('Notification clicked', event)

  event.notification.close()

  const url = event.notification.data?.url || '/'

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // Check if there's already a window open
        for (const client of clientList) {
          if (client.url.includes(url) && 'focus' in client) {
            return client.focus()
          }
        }
        // Open new window if none exists
        if (clients.openWindow) {
          return clients.openWindow(url)
        }
      })
  )
})

// Notification close event (optional tracking)
self.addEventListener('notificationclose', (event) => {
  console.log('Notification closed', event)
})
