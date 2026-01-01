# Vercel Deployment Guide for FlowHive Backend

## Prerequisites
1. Vercel account
2. PostgreSQL database (use Vercel Postgres or external like Supabase)

## Deployment Steps

### 1. Install Vercel CLI (optional)
```bash
npm i -g vercel
```

### 2. Set Environment Variables in Vercel

Go to your Vercel project settings and add these environment variables:

```
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:5173
DEBUG=false
APP_NAME=FlowHive
APP_VERSION=1.0.0
UPLOAD_DIR=/tmp/uploads
```

**Important Notes:**
- Use `/tmp/uploads` for UPLOAD_DIR on Vercel (ephemeral storage)
- For production, consider using cloud storage (AWS S3, Cloudinary, etc.) instead of local file storage
- Set `ALLOWED_ORIGINS` to include your frontend domain
- Generate a secure `SECRET_KEY` (use: `openssl rand -hex 32`)

### 3. Deploy to Vercel

**Option A: Using Vercel CLI**
```bash
cd backend
vercel
```

**Option B: Using Vercel Dashboard**
1. Go to https://vercel.com/new
2. Import your Git repository
3. Set the root directory to `backend`
4. Add environment variables
5. Deploy

### 4. Update Frontend API URL

Update your frontend's API base URL to point to your Vercel backend URL:
```typescript
// frontend/src/services/api.ts
const API_BASE_URL = 'https://your-backend.vercel.app/api'
```

### 5. Database Migrations

**Important:** Vercel is serverless, so you cannot run Alembic migrations on Vercel directly.

Run migrations from your local machine or a CI/CD pipeline:
```bash
# Set DATABASE_URL to your production database
export DATABASE_URL="postgresql://user:password@host:port/database"
alembic upgrade head
```

## Limitations on Vercel

1. **Ephemeral File System**: Files uploaded to `/tmp` are deleted after the serverless function completes. Use cloud storage for persistent files.

2. **WebSocket Limitations**: Vercel serverless functions have limitations with WebSockets. Consider using a separate service for real-time features.

3. **No Background Tasks**: Serverless functions are stateless. Consider using Vercel Cron Jobs or external task queues.

4. **Cold Starts**: First request may be slower due to cold start.

## Alternative: Use Vercel Postgres

If you want to use Vercel's built-in PostgreSQL:

```bash
vercel postgres create
```

Then add the connection string to your environment variables.

## Recommended Production Setup

For production, consider:
1. **Database**: Supabase, Railway, or Vercel Postgres
2. **File Storage**: AWS S3, Cloudinary, or Vercel Blob
3. **Real-time**: Separate WebSocket service (Railway, Render)
4. **Monitoring**: Sentry, Datadog

## Testing Deployment

After deployment, test these endpoints:
- `https://your-backend.vercel.app/` - Root endpoint
- `https://your-backend.vercel.app/health` - Health check
- `https://your-backend.vercel.app/docs` - API documentation
