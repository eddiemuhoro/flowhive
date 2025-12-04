const WS_URL =  'ws://localhost:8000/api/ws'

export interface WebSocketMessage {
  type: string
  workspace_id?: number
  data?: any
}

export class WebSocketService {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private messageHandlers: Map<string, Set<(data: any) => void>> = new Map()

  connect(workspaceId: number): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return
    }

    const url = `${WS_URL}/workspace/${workspaceId}`
    this.ws = new WebSocket(url)

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.reconnectAttempts = 0
    }

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data)
        this.handleMessage(message)
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    this.ws.onclose = () => {
      console.log('WebSocket closed')
      this.attemptReconnect(workspaceId)
    }
  }

  private attemptReconnect(workspaceId: number): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectDelay * this.reconnectAttempts

      console.log(`Attempting to reconnect in ${delay}ms...`)
      setTimeout(() => {
        this.connect(workspaceId)
      }, delay)
    } else {
      console.error('Max reconnection attempts reached')
    }
  }

  private handleMessage(message: WebSocketMessage): void {
    const handlers = this.messageHandlers.get(message.type)
    if (handlers) {
      handlers.forEach(handler => handler(message.data))
    }

    // Also call wildcard handlers
    const wildcardHandlers = this.messageHandlers.get('*')
    if (wildcardHandlers) {
      wildcardHandlers.forEach(handler => handler(message))
    }
  }

  on(eventType: string, handler: (data: any) => void): void {
    if (!this.messageHandlers.has(eventType)) {
      this.messageHandlers.set(eventType, new Set())
    }
    this.messageHandlers.get(eventType)!.add(handler)
  }

  off(eventType: string, handler: (data: any) => void): void {
    const handlers = this.messageHandlers.get(eventType)
    if (handlers) {
      handlers.delete(handler)
    }
  }

  send(data: any): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
    this.messageHandlers.clear()
  }
}

export const wsService = new WebSocketService()
