# Flowhive Frontend

Vue.js 3 frontend application for Flowhive productivity platform.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env if needed (API URL configuration)
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at http://localhost:5173

## Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── assets/          # Static assets
│   ├── components/      # Reusable Vue components
│   ├── layouts/         # Layout components
│   ├── router/          # Vue Router configuration
│   ├── services/        # API service layer
│   ├── stores/          # Pinia stores
│   ├── types/           # TypeScript type definitions
│   ├── views/           # Page components
│   ├── App.vue          # Root component
│   ├── main.ts          # Application entry point
│   └── style.css        # Global styles
├── public/              # Public static files
├── index.html           # HTML entry point
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # TailwindCSS configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies and scripts
```

## Features

- **Authentication**: Login and registration with JWT
- **Workspaces**: Create and manage workspaces
- **Projects**: Organize work into projects and task lists
- **Tasks**: Create, edit, and track tasks with subtasks
- **Multiple Views**: List, Board (Kanban), and Calendar views
- **Real-time Updates**: WebSocket integration for live updates
- **Comments**: Collaborate with team comments
- **File Attachments**: Upload and attach files to tasks
- **Analytics**: Executive dashboard with charts and metrics
- **Notifications**: Real-time notification system

## Tech Stack

- **Vue.js 3** with Composition API (script setup)
- **TypeScript** for type safety
- **Pinia** for state management
- **Vue Router** for navigation
- **TailwindCSS** for styling
- **Axios** for API calls
- **VueUse** for composables
- **Chart.js** for analytics charts
- **Vite** as build tool

## Development

### Key Directories

- `src/services/`: API service layer with separate files for each domain
- `src/stores/`: Pinia stores for state management
- `src/types/`: TypeScript interfaces and types
- `src/views/`: Page-level components
- `src/components/`: Reusable components
- `src/layouts/`: Layout wrapper components

### State Management

The application uses Pinia stores:
- `auth.ts`: Authentication and user management
- `workspace.ts`: Workspaces and projects
- `task.ts`: Tasks, comments, and attachments
- `notification.ts`: Real-time notifications

### API Integration

All API calls are handled through service files in `src/services/`:
- `auth.service.ts`: Authentication endpoints
- `workspace.service.ts`: Workspaces and projects
- `task.service.ts`: Tasks, comments, attachments
- `websocket.service.ts`: WebSocket connection management

### Routing

Routes are defined in `src/router/index.ts` with:
- Authentication guards
- Role-based access control
- Lazy-loaded components

## Environment Variables

- `VITE_API_URL`: Backend API URL (default: http://localhost:8000/api)
- `VITE_WS_URL`: WebSocket URL (default: ws://localhost:8000/api/ws)
