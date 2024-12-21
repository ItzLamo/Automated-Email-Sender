import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from config import *

class EmailSender:
    def __init__(self):
        self.status_callback = None

    def set_status_callback(self, callback):
        """Set callback for status updates"""
        self.status_callback = callback

    def update_status(self, message, is_error=False):
        """Update status with optional callback"""
        print(message)
        if self.status_callback:
            self.status_callback(message, is_error)

    def send_email(self, recipient_email, subject, body, attachment_paths=None):
        """Send an email with optional attachments"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            if attachment_paths:
                for path in attachment_paths:
                    if os.path.exists(path):
                        with open(path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename={os.path.basename(path)}'
                            )
                            msg.attach(part)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            
            self.update_status(f"✓ Email sent to {recipient_email}")
            return True

        except Exception as e:
            self.update_status(f"✗ Failed to send email to {recipient_email}: {str(e)}", True)
            return False