from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import get_db
import json

router = APIRouter()


class ConnectionManager:
    """Manage WebSocket connections"""

    def __init__(self):
        # workspace_id -> set of websockets
        self.active_connections: Dict[int, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, workspace_id: int):
        """Connect a websocket to a workspace room"""
        await websocket.accept()

        if workspace_id not in self.active_connections:
            self.active_connections[workspace_id] = set()

        self.active_connections[workspace_id].add(websocket)

    def disconnect(self, websocket: WebSocket, workspace_id: int):
        """Disconnect a websocket from a workspace room"""
        if workspace_id in self.active_connections:
            self.active_connections[workspace_id].discard(websocket)

            # Clean up empty rooms
            if not self.active_connections[workspace_id]:
                del self.active_connections[workspace_id]

    async def broadcast_to_workspace(self, workspace_id: int, message: dict):
        """Broadcast a message to all connections in a workspace"""
        if workspace_id in self.active_connections:
            disconnected = set()

            for connection in self.active_connections[workspace_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.add(connection)

            # Remove disconnected clients
            for connection in disconnected:
                self.active_connections[workspace_id].discard(connection)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific websocket"""
        try:
            await websocket.send_json(message)
        except Exception:
            pass


manager = ConnectionManager()


@router.websocket("/workspace/{workspace_id}")
async def websocket_endpoint(websocket: WebSocket, workspace_id: int):
    """
    WebSocket endpoint for real-time updates within a workspace

    Clients should connect to this endpoint to receive real-time updates about:
    - Task creation, updates, and deletion
    - Comment additions
    - Assignment changes
    - Status changes
    - New notifications
    """
    await manager.connect(websocket, workspace_id)

    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()

            try:
                message = json.loads(data)

                # Echo confirmation back to sender
                await manager.send_personal_message({
                    "type": "confirmation",
                    "message": "Message received",
                    "original": message
                }, websocket)

                # Broadcast to all other clients in the workspace
                await manager.broadcast_to_workspace(workspace_id, {
                    "type": "broadcast",
                    "workspace_id": workspace_id,
                    "data": message
                })

            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format"
                }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, workspace_id)


async def notify_workspace(workspace_id: int, event_type: str, data: dict):
    """
    Helper function to send notifications to a workspace

    Usage example in other routes:
    await notify_workspace(workspace_id, "task_created", {"task_id": task.id, "title": task.title})
    """
    await manager.broadcast_to_workspace(workspace_id, {
        "type": event_type,
        "workspace_id": workspace_id,
        "data": data
    })
