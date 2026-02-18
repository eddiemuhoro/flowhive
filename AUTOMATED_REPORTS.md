# Automated Weekly Email Reports

## Overview
The system automatically sends field activity reports every Sunday at 5 PM (East Africa Time).

## Configuration

All settings are in `backend/.env`:

```env
# Weekly Report Automation
WEEKLY_REPORT_ENABLED=True              # Set to False to disable
WEEKLY_REPORT_DAY=6                     # 0=Monday, 6=Sunday
WEEKLY_REPORT_HOUR=17                   # 5 PM (24-hour format)
WEEKLY_REPORT_RECIPIENTS=email1@example.com,email2@example.com
WEEKLY_REPORT_TIMEZONE=Africa/Nairobi   # Your timezone
```

## How It Works

1. **Scheduler**: Runs every Sunday at 5 PM
2. **Date Range**: Automatically calculates last week (Monday-Sunday)
3. **Personalized Distribution**:
   - **Team Members**: Receive only their own activities
   - **Managers/Executives**: Receive complete report with all staff activities
   - **Configured Recipients**: Also receive full reports (if specified in .env)
   - Full activity details with dates, times, customers, locations
   - Link to view online report

## Setup Steps

1. **Add Recipients** (required):
   ```env
   WEEKLY_REPORT_RECIPIENTS=manager@company.com,director@company.com
   ```

2. **Verify Resend API Key** is set:
   ```env
   RESEND_API_KEY=re_your_key_here
   RESEND_FROM_EMAIL=noreply@reports.crystaline.co.ke
   ```

3. **Restart the server**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

4. **Check logs** on startup:
   ```
   INFO: Scheduler started - Weekly reports will run on day 6 at 17:00 Africa/Nairobi
   ```

## Manual Testing

You can trigger a test report without waiting for Sunday:

**Endpoint**: `POST /api/field-activities/trigger-weekly-report`

**Requirements**: Must be logged in as Executive

**Using curl**:
```bash
curl -X POST http://localhost:8000/api/field-activities/trigger-weekly-report \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response**:
```json
{
  "message": "Weekly report job triggered successfully",
  "timestamp": "2026-02-18T17:00:00"
}
```

## Individual vs Bulk Reports

### Option 1: Individual Reports (Recommended for Weekly Automation)

**When to use**: Automated weekly reports, privacy-focused distribution

**How it works**:
- ✅ Each team member receives only their own activities
- ✅ Managers/Executives receive complete reports with all staff
- ✅ Configured recipients also receive full reports
- ✅ No activities = no email (staff with no activities are skipped)

**From UI**: Check "Send individual reports to all workspace members"

**From API**:
```json
{
  "send_individual_reports": true,
  "date_from": "2026-02-10",
  "date_to": "2026-02-16",
  "recipient_emails": []  // Optional, for additional full reports
}
```

### Option 2: Bulk Report (Same for Everyone)

**When to use**: Ad-hoc reports, presentations, specific recipient list

**How it works**:
- ✅ All recipients receive identical full reports
- ✅ Includes all staff activities
- ✅ Good for managers reviewing team performance

**From UI**: Uncheck individual reports, add recipient emails

**From API**:
```json
{
  "send_individual_reports": false,
  "recipient_emails": ["manager@company.com", "director@company.com"],
  "date_from": "2026-02-10",
  "date_to": "2026-02-16"
}
```

## Customization

### Change Day/Time
Edit `.env`:
```env
WEEKLY_REPORT_DAY=0     # Send on Monday instead
WEEKLY_REPORT_HOUR=8    # Send at 8 AM instead
```

### Add More Recipients
Just add comma-separated emails:
```env
WEEKLY_REPORT_RECIPIENTS=email1@co.ke,email2@co.ke,email3@co.ke
```

### Disable Temporarily
```env
WEEKLY_REPORT_ENABLED=False
```

## Troubleshooting

**No emails received?**
1. Check logs for errors: `INFO: Weekly report job completed`
2. Verify `WEEKLY_REPORT_RECIPIENTS` is set
3. Verify `RESEND_API_KEY` is valid
4. Check if there are activities for the week
5. Check spam folder

**Wrong timezone?**
Update `WEEKLY_REPORT_TIMEZONE` to match your location:
```env
WEEKLY_REPORT_TIMEZONE=America/New_York
WEEKLY_REPORT_TIMEZONE=Europe/London
WEEKLY_REPORT_TIMEZONE=Asia/Dubai
```

**Test immediately:**
Use the manual trigger endpoint (executive access required)

## Technical Details

- **Scheduler**: APScheduler (AsyncIO)
- **Trigger**: CronTrigger (day of week + hour)
- **Database**: Queries all active workspaces
- **Date Range**: Previous Monday-Sunday
- **Email Service**: Resend API
- **Startup**: Auto-starts with FastAPI lifespan events
- **Shutdown**: Gracefully stops when server stops

## Files Modified

1. `backend/app/scheduler.py` - Scheduler logic
2. `backend/app/main.py` - Lifespan events
3. `backend/app/config.py` - Configuration settings
4. `backend/app/api/field_operations.py` - Manual trigger endpoint
5. `backend/.env` - Environment variables
6. `backend/requirements.txt` - Added APScheduler

## Next Steps

1. ✅ Set recipient emails in `.env`
2. ✅ Restart server
3. ✅ Test with manual trigger
4. ✅ Wait for Sunday at 5 PM or adjust schedule as needed
