/**
 * Push Notification Service
 * Handles push notification subscription and management
 */

import { apiClient } from './api'

export interface PushSubscription {
  endpoint: string
  keys: {
    p256dh: string
    auth: string
  }
}

class PushService {
  private vapidPublicKey: string | null = null

  /**
   * Get VAPID public key from backend
   */
  async getPublicKey(): Promise<string> {
    if (this.vapidPublicKey) {
      return this.vapidPublicKey
    }

    try {
      const response = await apiClient.get('/push/vapid-public-key')
      this.vapidPublicKey = response.data.publicKey
      return this.vapidPublicKey!
    } catch (error) {
      console.error('Failed to get VAPID public key:', error)
      throw error
    }
  }

  /**
   * Check if push notifications are supported
   */
  isSupported(): boolean {
    return 'serviceWorker' in navigator && 'PushManager' in window && 'Notification' in window
  }

  /**
   * Get current notification permission status
   */
  getPermissionStatus(): NotificationPermission {
    if (!('Notification' in window)) {
      return 'denied'
    }
    return Notification.permission
  }

  /**
   * Request notification permission from user
   */
  async requestPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      throw new Error('Notifications not supported')
    }

    const permission = await Notification.requestPermission()
    return permission
  }

  /**
   * Subscribe to push notifications
   */
  async subscribe(): Promise<PushSubscription | null> {
    if (!this.isSupported()) {
      throw new Error('Push notifications not supported')
    }

    // Check permission
    const permission = await this.requestPermission()
    if (permission !== 'granted') {
      throw new Error('Notification permission denied')
    }

    try {
      // Get service worker registration
      const registration = await navigator.serviceWorker.ready

      // Get VAPID public key
      const vapidPublicKey = await this.getPublicKey()

      // Convert VAPID key to Uint8Array
      const convertedKey = this.urlBase64ToUint8Array(vapidPublicKey)

      // Subscribe to push
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: convertedKey as BufferSource
      })

      // Convert subscription to our format
      const subJson = subscription.toJSON()
      const pushSubscription: PushSubscription = {
        endpoint: subJson.endpoint || '',
        keys: {
          p256dh: subJson.keys?.p256dh || '',
          auth: subJson.keys?.auth || ''
        }
      }

      // Send subscription to backend
      await apiClient.post('/push/subscribe', pushSubscription)

      console.log('Successfully subscribed to push notifications')
      return pushSubscription

    } catch (error) {
      console.error('Failed to subscribe to push notifications:', error)
      throw error
    }
  }

  /**
   * Unsubscribe from push notifications
   */
  async unsubscribe(): Promise<void> {
    if (!this.isSupported()) {
      return
    }

    try {
      const registration = await navigator.serviceWorker.ready
      const subscription = await registration.pushManager.getSubscription()

      if (subscription) {
        await subscription.unsubscribe()

        // Notify backend
        await apiClient.delete('/push/unsubscribe', {
          params: { endpoint: subscription.endpoint }
        })

        console.log('Successfully unsubscribed from push notifications')
      }
    } catch (error) {
      console.error('Failed to unsubscribe:', error)
      throw error
    }
  }

  /**
   * Check if user is currently subscribed
   */
  async isSubscribed(): Promise<boolean> {
    if (!this.isSupported()) {
      return false
    }

    try {
      const registration = await navigator.serviceWorker.ready
      const subscription = await registration.pushManager.getSubscription()
      return subscription !== null
    } catch (error) {
      console.error('Failed to check subscription status:', error)
      return false
    }
  }

  /**
   * Convert VAPID key from URL-safe base64 to Uint8Array
   */
  private urlBase64ToUint8Array(base64String: string): Uint8Array {
    const padding = '='.repeat((4 - base64String.length % 4) % 4)
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/')

    const rawData = window.atob(base64)
    const outputArray = new Uint8Array(rawData.length)

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i)
    }
    return outputArray
  }
}

export const pushService = new PushService()
