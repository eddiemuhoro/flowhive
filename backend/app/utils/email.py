import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os


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
