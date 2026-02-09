# Meeting Minutes with Cloudinary Setup Guide

## 🎉 Implementation Complete!

The Meeting Minutes feature has been fully implemented with **Cloudinary** for file storage! This allows you to upload PDFs, images, and documents directly to the cloud.

---

## ✅ What's Been Implemented

### Backend

- ✅ Cloudinary integration utility (`app/utils/cloudinary.py`)
- ✅ Database models for meeting minutes, attachments, and action items
- ✅ Migration file created
- ✅ Full REST API with 10+ endpoints
- ✅ PDF, image, and document upload to Cloudinary
- ✅ Secure file deletion from Cloudinary

### Frontend

- ✅ TypeScript types for minutes
- ✅ Service layer for API calls
- ✅ Pinia store for state management
- ✅ Minutes listing page with filters
- ✅ Minute detail page with attachments
- ✅ Action items management
- ✅ File upload (drag & drop ready)

---

## 🔧 Setup Instructions

### 1. Install Cloudinary Library

```bash
cd backend
pip install cloudinary
```

Or use the updated `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Get Cloudinary Credentials

1. Go to [cloudinary.com](https://cloudinary.com/)
2. Sign up for a free account
3. From your dashboard, copy:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

### 3. Update `.env` File

Add these to your `backend/.env`:

```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

### 4. Run Database Migration

```bash
cd backend
alembic upgrade head
```

This creates three new tables:

- `meeting_minutes`
- `minute_attachments` (stores Cloudinary URLs)
- `minute_action_items`

### 5. Start Servers

**Backend:**

```bash
cd backend
python -m uvicorn app.main:main --reload
```

**Frontend:**

```bash
cd frontend
npm run dev
```

---

## 📁 File Structure Created

### Backend

```
backend/
├── app/
│   ├── api/
│   │   └── meeting_minutes.py          # 10 API endpoints
│   ├── models/
│   │   └── meeting_minute.py           # 3 database models
│   ├── schemas/
│   │   └── meeting_minute.py           # Pydantic schemas
│   ├── utils/
│   │   └── cloudinary.py               # ✨ Cloudinary helper
│   └── config.py                        # Updated with Cloudinary config
├── alembic/versions/
│   └── 20260209_1400_...py             # New migration
└── requirements.txt                     # Updated with cloudinary
```

### Frontend

```
frontend/src/
├── views/field/
│   ├── FieldMinutes.vue                # List view
│   └── FieldMinuteDetail.vue           # Detail view with uploads
├── stores/
│   └── meetingMinute.ts                # State management
├── services/
│   └── meetingMinute.service.ts        # API calls
└── types/
    └── meetingMinute.ts                # TypeScript types
```

---

## 🚀 Features

### Meeting Minutes

- ✅ Create minutes with title, date, time, location
- ✅ Add attendees
- ✅ Document agenda, discussions, decisions
- ✅ Filter by date range and search
- ✅ Edit and delete minutes

### Attachments (Cloudinary)

- ✅ Upload PDFs, images, Word docs, Excel files
- ✅ Files stored in Cloudinary cloud
- ✅ CDN-backed delivery (fast loading)
- ✅ Secure URLs stored in database
- ✅ Delete files from both DB and Cloudinary

### Action Items

- ✅ Create tasks from meetings
- ✅ Assign to team members
- ✅ Set due dates
- ✅ Track status (pending/in progress/completed)

---

## 📡 API Endpoints

| Method | Endpoint                                       | Description               |
| ------ | ---------------------------------------------- | ------------------------- |
| GET    | `/api/meeting-minutes/workspace/{id}`          | List all minutes          |
| GET    | `/api/meeting-minutes/{id}`                    | Get single minute         |
| POST   | `/api/meeting-minutes`                         | Create minute             |
| PUT    | `/api/meeting-minutes/{id}`                    | Update minute             |
| DELETE | `/api/meeting-minutes/{id}`                    | Delete minute             |
| POST   | `/api/meeting-minutes/{id}/attachments`        | Upload file to Cloudinary |
| DELETE | `/api/meeting-minutes/{id}/attachments/{aid}`  | Delete attachment         |
| POST   | `/api/meeting-minutes/{id}/action-items`       | Create action item        |
| PUT    | `/api/meeting-minutes/{id}/action-items/{aid}` | Update action item        |
| DELETE | `/api/meeting-minutes/{id}/action-items/{aid}` | Delete action item        |

---

## 🎯 How It Works

### Upload Flow

1. **User selects file** → Frontend creates FormData
2. **POST to backend** → FastAPI receives UploadFile
3. **Upload to Cloudinary** → `cloudinary.uploader.upload()`
4. **Get URL** → Cloudinary returns `secure_url` and `public_id`
5. **Save to DB** → Store URL and metadata in `minute_attachments`
6. **Display** → Frontend loads file from Cloudinary URL

### Storage Benefits

- 📦 **No server disk usage** - Files in cloud
- 🚀 **CDN delivery** - Fast worldwide access
- 🔒 **Secure** - Signed URLs, access control
- 💾 **Scalable** - No storage limits
- 🌐 **Production-ready** - Works on Vercel/Heroku

---

## 💡 Usage Example

### Navigate to Minutes

1. Open field operations workspace
2. Click "Minutes" in sidebar/bottom nav
3. Click "+ New Minutes"

### Create Meeting Minute

1. Fill in title, date, location
2. Add agenda and discussions
3. Click "Create Minutes"
4. You'll be taken to detail page

### Upload Files

1. On detail page, click "+ Add Files"
2. Select PDF, images, or documents
3. Files upload to Cloudinary automatically
4. URLs saved, thumbnails shown

### Add Action Items

1. Click "+ Add Action Item"
2. Enter description and due date
3. Assign to team member
4. Track completion status

---

## 🔐 Security

- ✅ Workspace membership required
- ✅ Only creators/managers can delete
- ✅ File type validation (no executables)
- ✅ File size limit (10MB default)
- ✅ HTML sanitization on save
- ✅ Cloudinary secure URLs

---

## 🎨 Cloudinary Free Tier

Your free account includes:

- 25 GB storage
- 25 GB bandwidth/month
- 25,000 transformations
- More than enough for getting started!

---

## 🐛 Troubleshooting

### "Module 'cloudinary' not found"

```bash
pip install cloudinary
```

### "Cloudinary configuration error"

- Check `.env` file has all 3 variables set
- Restart FastAPI server after updating `.env`
- Verify credentials from Cloudinary dashboard

### Migration fails

```bash
alembic downgrade -1
alembic upgrade head
```

### Upload fails

- Check file size < 10MB
- Verify file type is allowed
- Check Cloudinary credentials are correct
- Look at backend console for error details

---

## 🎉 You're All Set!

Navigate to `/field/minutes` and start documenting your field meetings with cloud-powered file storage!

**Questions?** Check the API docs at `http://localhost:8000/docs`
