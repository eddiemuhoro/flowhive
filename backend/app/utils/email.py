import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List, Dict, Any
import os
import resend
from datetime import datetime


class EmailService:
    """Email service for sending password reset emails"""

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user)
        self.from_name = os.getenv("FROM_NAME", "Flowhive")

    def send_password_reset_email(
        self,
        to_email: str,
        reset_token: str,
        username: str,
        frontend_url: str = "http://localhost:5173"
    ) -> bool:
        """Send password reset email with reset link"""
        try:
            # Create reset link
            reset_link = f"{frontend_url}/reset-password?token={reset_token}"

            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Reset Your Flowhive Password"
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email

            # HTML email body
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2563eb;">Password Reset Request</h2>
                        <p>Hi {username},</p>
                        <p>We received a request to reset your password for your Flowhive account.</p>
                        <p>Click the button below to reset your password:</p>
                        <div style="margin: 30px 0;">
                            <a href="{reset_link}"
                               style="background-color: #2563eb;
                                      color: white;
                                      padding: 12px 24px;
                                      text-decoration: none;
                                      border-radius: 5px;
                                      display: inline-block;">
                                Reset Password
                            </a>
                        </div>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="color: #666; font-size: 14px; word-break: break-all;">{reset_link}</p>
                        <p style="margin-top: 30px; color: #666; font-size: 14px;">
                            This link will expire in 1 hour.
                        </p>
                        <p style="color: #666; font-size: 14px;">
                            If you didn't request this password reset, please ignore this email.
                        </p>
                        <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                        <p style="color: #999; font-size: 12px;">
                            © 2026 Flowhive. All rights reserved.
                        </p>
                    </div>
                </body>
            </html>
            """

            # Plain text version
            text = f"""
            Password Reset Request

            Hi {username},

            We received a request to reset your password for your Flowhive account.

            Click the link below to reset your password:
            {reset_link}

            This link will expire in 1 hour.

            If you didn't request this password reset, please ignore this email.

            © 2026 Flowhive. All rights reserved.
            """

            # Attach both versions
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)

            # Send email if SMTP is configured
            if not self.smtp_user or not self.smtp_password:
                print(f"[DEV MODE] Password reset email would be sent to: {to_email}")
                print(f"[DEV MODE] Reset link: {reset_link}")
                return True

            # Send via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            # In development, still return True and log the link
            print(f"[DEV MODE] Reset link: {reset_link}")
            return True


# Create singleton instance
email_service = EmailService()


def send_activity_report_email(
    to_emails: List[str],
    subject: str,
    activities_by_staff: List[Dict[str, Any]],
    date_from: str,
    date_to: str,
    summary: Dict[str, Any],
    resend_api_key: str,
    from_email: str,
    from_name: str,
    frontend_url: str
) -> Dict[str, Any]:
    """
    Send activity report email via Resend

    Args:
        to_emails: List of recipient email addresses
        subject: Email subject line
        activities_by_staff: List of activity data grouped by staff
        date_from: Start date of report
        date_to: End date of report
        summary: Summary statistics
        resend_api_key: Resend API key
        from_email: From email address
        from_name: From name
        frontend_url: Frontend URL for links

    Returns:
        dict with success status and message/error
    """
    # Set Resend API key
    resend.api_key = resend_api_key

    # Generate HTML content
    html_content = generate_report_html(
        activities_by_staff, date_from, date_to, summary, frontend_url
    )

    try:
        # Send email
        params = {
            "from": f"{from_name} <{from_email}>",
            "to": to_emails,
            "subject": subject,
            "html": html_content,
        }

        email = resend.Emails.send(params)

        return {
            "success": True,
            "message": f"Report sent successfully to {len(to_emails)} recipient(s)",
            "email_id": email.get("id")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def generate_report_html(
    activities_by_staff: List[Dict[str, Any]],
    date_from: str,
    date_to: str,
    summary: Dict[str, Any],
    frontend_url: str
) -> str:
    """Generate HTML email template for activity report"""

    # Format dates nicely
    try:
        from_date = datetime.strptime(date_from, "%Y-%m-%d").strftime("%B %d, %Y")
        to_date = datetime.strptime(date_to, "%Y-%m-%d").strftime("%B %d, %Y")
    except:
        from_date = date_from
        to_date = date_to

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #111827;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9fafb;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        }}
        .header {{
            border-bottom: 4px solid #2563eb;
            padding-bottom: 24px;
            margin-bottom: 32px;
            text-align: center;
        }}
        h1 {{
            color: #1f2937;
            margin: 0 0 12px 0;
            font-size: 32px;
            font-weight: 700;
        }}
        .period {{
            color: #6b7280;
            font-size: 16px;
            font-weight: 500;
        }}
        .summary {{
            background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
            border-left: 5px solid #2563eb;
            border-radius: 8px;
            padding: 24px;
            margin: 24px 0 32px 0;
        }}
        .summary h2 {{
            margin: 0 0 20px 0;
            color: #1e40af;
            font-size: 22px;
            font-weight: 700;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .stat {{
            background-color: rgba(255, 255, 255, 0.8);
            padding: 16px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-label {{
            font-size: 12px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: 800;
            color: #1e40af;
            margin-top: 8px;
        }}
        .staff-section {{
            margin: 40px 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e5e7eb;
        }}
        .staff-header {{
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
            padding: 20px 24px;
            color: white;
        }}
        .staff-name {{
            font-size: 22px;
            font-weight: 700;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .staff-stats {{
            font-size: 14px;
            margin-top: 6px;
            opacity: 0.95;
            font-weight: 500;
        }}
        .activities-list {{
            padding: 24px;
            background-color: #f9fafb;
        }}
        .activity-card {{
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 16px;
            transition: box-shadow 0.2s;
        }}
        .activity-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .activity-header {{
            display: flex;
            gap: 14px;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid #f3f4f6;
        }}
        .activity-number {{
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            min-width: 36px;
            height: 36px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 15px;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.3);
        }}
        .activity-title {{
            font-size: 18px;
            font-weight: 700;
            color: #1f2937;
            margin: 0 0 6px 0;
            line-height: 1.3;
        }}
        .activity-meta {{
            color: #6b7280;
            font-size: 13px;
            font-weight: 500;
        }}
        .activity-meta-icon {{
            margin: 0 4px;
            color: #9ca3af;
        }}
        .detail-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin: 16px 0;
        }}
        .detail {{
            font-size: 14px;
            padding: 8px;
            background-color: #f9fafb;
            border-radius: 6px;
        }}
        .detail-label {{
            color: #6b7280;
            font-weight: 600;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 4px;
        }}
        .detail-value {{
            color: #1f2937;
            font-weight: 500;
        }}
        .description {{
            background-color: #f0fdf4;
            border-left: 4px solid #22c55e;
            padding: 16px;
            margin-top: 16px;
            border-radius: 6px;
        }}
        .description strong {{
            color: #166534;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 8px;
        }}
        .description-content {{
            color: #1f2937;
            font-size: 14px;
            line-height: 1.6;
        }}
        .description-content ol,
        .description-content ul {{
            margin: 8px 0;
            padding-left: 24px;
        }}
        .description-content li {{
            margin: 6px 0;
        }}
        .description-content p {{
            margin: 8px 0;
        }}
        .remarks {{
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 16px;
            margin-top: 16px;
            border-radius: 6px;
        }}
        .remarks strong {{
            color: #92400e;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: block;
            margin-bottom: 8px;
        }}
        .remarks-content {{
            color: #1f2937;
            font-size: 14px;
            line-height: 1.6;
        }}
        .footer {{
            margin-top: 48px;
            padding-top: 24px;
            border-top: 2px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 13px;
        }}
        .footer-link {{
            display: inline-block;
            margin-top: 16px;
            padding: 12px 24px;
            background-color: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: background-color 0.2s;
        }}
        .footer-link:hover {{
            background-color: #1d4ed8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Weekly Activity Report</h1>
            <p class="period">{from_date} → {to_date}</p>
        </div>

        <div class="summary">
            <h2>📈 Summary Overview</h2>
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-label">Activities</div>
                    <div class="stat-value">{summary.get('total_activities', 0)}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Total Hours</div>
                    <div class="stat-value">{summary.get('total_hours', 0):.1f}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Staff</div>
                    <div class="stat-value">{summary.get('unique_staff', 0)}</div>
                </div>
            </div>
        </div>
"""

    # Add activities grouped by staff
    for staff_group in activities_by_staff:
        staff_name = staff_group.get('staff_name', 'Unknown')
        activities = staff_group.get('activities', [])
        total_hours = staff_group.get('total_hours', 0)

        html += f"""
        <div class="staff-section">
            <div class="staff-header">
                <h3 class="staff-name">
                    <span>👤</span>
                    <span>{staff_name}</span>
                </h3>
                <div class="staff-stats">
                    {len(activities)} activities • {total_hours:.1f} hours worked
                </div>
            </div>
            <div class="activities-list">
"""

        for idx, activity in enumerate(activities, 1):
            # Format dates and times
            try:
                activity_date = datetime.strptime(activity['activity_date'], "%Y-%m-%d").strftime("%A, %B %d, %Y")
            except:
                activity_date = activity.get('activity_date', '')

            start_time = activity.get('start_time', '')[:5] if activity.get('start_time') else '--:--'
            end_time = activity.get('end_time', '')[:5] if activity.get('end_time') else '--:--'
            duration = activity.get('duration_hours', 0)

            html += f"""
            <div class="activity-card">
                <div class="activity-header">
                    <div class="activity-number">{idx}</div>
                    <div style="flex: 1;">
                        <h4 class="activity-title">{activity.get('title', 'Untitled Activity')}</h4>
                        <div class="activity-meta">
                            📅 {activity_date}
                            <span class="activity-meta-icon">•</span>
                            🕐 {start_time} - {end_time}
                            <span class="activity-meta-icon">•</span>
                            ⏱️ {duration:.1f}h
                        </div>
                    </div>
                </div>

                <div class="detail-grid">
                    <div class="detail">
                        <span class="detail-label">🏢 Customer</span>
                        <div class="detail-value">{activity.get('customer_name', 'N/A')}</div>
                    </div>
                    <div class="detail">
                        <span class="detail-label">📍 Location</span>
                        <div class="detail-value">{activity.get('location', 'N/A')}</div>
                    </div>
"""

            if activity.get('customer_rep'):
                html += f"""
                    <div class="detail">
                        <span class="detail-label">👨‍💼 Customer Rep</span>
                        <div class="detail-value">{activity.get('customer_rep', 'N/A')}</div>
                    </div>
"""

            html += """
                </div>
"""

            # Task description - render HTML properly
            if activity.get('task_description'):
                desc = activity.get('task_description', '')
                html += f"""
                <div class="description">
                    <strong>📝 Task Description</strong>
                    <div class="description-content">
                        {desc}
                    </div>
                </div>
"""

            # Remarks - render HTML properly
            if activity.get('remarks'):
                remarks = activity.get('remarks', '')
                html += f"""
                <div class="remarks">
                    <strong>💬 Remarks</strong>
                    <div class="remarks-content">
                        {remarks}
                    </div>
                </div>
"""

            html += """
            </div>
"""

        html += """
            </div>
        </div>
"""

    html += f"""
        <div class="footer">
            <p style="margin: 0 0 8px 0; font-weight: 600; color: #4b5563;">
                Generated by Crystaline FlowHive
            </p>
            <p style="margin: 0 0 16px 0;">
                {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
            </p>
            <a href="{frontend_url}/field/reports?from={date_from}&to={date_to}"
               class="footer-link">
                📊 View Full Report Online
            </a>
            <p style="margin-top: 20px; color: #9ca3af; font-size: 12px;">
                © {datetime.now().year} Crystaline. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>
"""

    return html
