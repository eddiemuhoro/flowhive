# Flowhive Backend

FastAPI backend for Flowhive productivity app.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

4. Create the database:
```bash
createdb flowhive  # or use your PostgreSQL GUI
```

5. Run migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
python -m app.main
```

Or use uvicorn directly:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migrations:
```bash
alembic downgrade -1
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API routes
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── users.py     # User management
│   │   ├── workspaces.py # Workspace management
│   │   ├── projects.py  # Project & task list management
│   │   ├── tasks.py     # Task management
│   │   ├── comments.py  # Comments
│   │   ├── attachments.py # File uploads
│   │   ├── analytics.py # Analytics & reports
│   │   └── websocket.py # Real-time updates
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── utils/           # Utility functions
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── uploads/             # File upload directory
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## Authentication

The API uses JWT Bearer token authentication.

1. Register: POST `/api/auth/register`
2. Login: POST `/api/auth/login`
3. Use the returned access token in the Authorization header:
   ```
   Authorization: Bearer <your_token>
   ```

## WebSocket

Connect to WebSocket for real-time updates:
```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws/workspace/{workspace_id}');
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate a secure random string)
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `ALLOWED_ORIGINS`: CORS allowed origins (comma-separated)
- `UPLOAD_DIR`: Directory for file uploads
- `MAX_UPLOAD_SIZE`: Maximum file upload size in bytes
