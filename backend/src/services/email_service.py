from typing import Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.config import settings


class EmailService:
    def __init__(self):
        self.smtp_server = settings.EMAIL_HOST
        self.smtp_port = settings.EMAIL_PORT
        self.username = settings.EMAIL_USER
        self.password = settings.EMAIL_PASSWORD

    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str = ""):
        """
        Send an email to the specified recipient.
        """
        if not self.smtp_server or not self.username or not self.password:
            # In development, we might not have email configured
            print(f"Email would be sent to {to_email} with subject: {subject}")
            print(f"HTML content: {html_content}")
            return True

        try:
            msg = MIMEMultipart("alternative")
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to_email

            # Create both text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, "plain")
                msg.attach(text_part)

            html_part = MIMEText(html_content, "html")
            msg.attach(html_part)

            # Connect to server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable encryption
                server.login(self.username, self.password)
                server.sendmail(self.username, to_email, msg.as_string())

            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def send_password_reset_email(self, to_email: str, reset_token: str):
        """
        Send a password reset email with the provided reset token.
        """
        subject = "Password Reset Request"

        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}" if hasattr(settings, 'FRONTEND_URL') else f"http://localhost:3000/reset-password?token={reset_token}"

        html_content = f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>You have requested to reset your password. Click the link below to reset your password:</p>
                <p><a href="{reset_link}">Reset Password</a></p>
                <p>If you didn't request this, please ignore this email.</p>
                <p>This link will expire in 1 hour.</p>
            </body>
        </html>
        """

        text_content = f"""
        Password Reset Request

        You have requested to reset your password. Click the link below to reset your password:

        {reset_link}

        If you didn't request this, please ignore this email.
        This link will expire in 1 hour.
        """

        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )

    def send_welcome_email(self, to_email: str, user_name: str = None):
        """
        Send a welcome email to a new user.
        """
        subject = "Welcome to Our Application!"

        name = user_name or "there"
        html_content = f"""
        <html>
            <body>
                <h2>Welcome, {name}!</h2>
                <p>Thank you for registering with our application.</p>
                <p>We're excited to have you on board!</p>
            </body>
        </html>
        """

        text_content = f"""
        Welcome, {name}!

        Thank you for registering with our application.
        We're excited to have you on board!
        """

        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )