from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.api import (
    auth, users, workspaces, projects, tasks, comments, 
    attachments, analytics, websocket, field_operations, task_categories, meeting_minutes, customers
)
import os

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Full-stack productivity app for task management"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist (skip in serverless)
if not os.environ.get('VERCEL'):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    # Mount static files for uploads (skip in serverless)
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(workspaces.router, prefix="/api/workspaces", tags=["Workspaces"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(comments.router, prefix="/api/comments", tags=["Comments"])
app.include_router(attachments.router, prefix="/api/attachments", tags=["Attachments"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(websocket.router, prefix="/api/ws", tags=["WebSocket"])
app.include_router(field_operations.router, prefix="/api/field-activities", tags=["Field Operations"])
app.include_router(task_categories.router, prefix="/api/task-categories", tags=["Task Categories"])
app.include_router(meeting_minutes.router, prefix="/api/meeting-minutes", tags=["Meeting Minutes"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/test-upload", tags=["Testing"])
async def test_file_upload(
    file: UploadFile = File(..., description="File to upload for testing")
):
    """
    Test endpoint for file upload functionality in Swagger.
    
    This endpoint accepts a single file upload and returns information about the uploaded file.
    Useful for testing file upload functionality without authentication.
    """
    contents = await file.read()
    file_size = len(contents)
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size_bytes": file_size,
        "file_size_kb": round(file_size / 1024, 2)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
