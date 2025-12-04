# Flowhive - Full-Stack Productivity App

A comprehensive task management and productivity platform with workspace hierarchy, real-time collaboration, and executive analytics.

## 🚀 Features

- **Task Management**: Create, edit, delete, and organize tasks with subtasks
- **Deadline Tracking**: Set deadlines with reminders and notifications
- **Multiple Views**: List, Board (Kanban), and Calendar views
- **Workspace Hierarchy**: Workspaces → Projects → Task Lists → Tasks
- **Collaboration**: Task assignments, comments, and activity timeline
- **File Attachments**: Upload and attach files to tasks
- **Real-time Updates**: WebSocket-powered live updates
- **Role-Based Access**: Team members, managers, and executives with different permissions
- **Executive Dashboard**: Progress reports and analytics with charts
- **Progress Tracking**: Track task completion and team productivity

## 🛠️ Tech Stack

### Frontend
- Vue.js 3 with TypeScript
- Composition API (script setup)
- Pinia for state management
- Vue Router for navigation
- TailwindCSS for styling
- Vite as build tool
- Axios for API calls
- VueUse for composables
- Chart.js for analytics visualization

### Backend
- FastAPI (Python 3.11+)
- SQLAlchemy 2.0 ORM
- PostgreSQL database
- Alembic for migrations
- JWT authentication
- WebSockets for real-time updates
- Pydantic for data validation

## 📁 Project Structure

```
flowhive/
├── frontend/          # Vue.js application
└── backend/           # FastAPI application
```

## 🏃 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Configure your environment variables
alembic upgrade head      # Run migrations
python -m app.main        # Start the server
```

Backend will run on http://localhost:8000

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env      # Configure your environment variables
npm run dev               # Start dev server
```

Frontend will run on http://localhost:5173

## 📚 Documentation

- [Backend API Documentation](http://localhost:8000/docs) - Available when backend is running
- [Frontend Setup Guide](./frontend/README.md)
- [Backend Setup Guide](./backend/README.md)

## 🔐 Default Roles

- **Team Member**: Create and manage own tasks, collaborate on assigned tasks
- **Manager**: Manage team tasks, assign tasks, view team analytics
- **Executive**: Full access, view all analytics and reports

## 📄 License

MIT License - See LICENSE file for details
