import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"    # Replace with your email
EMAIL_PASSWORD = "app_key"          # Replace with your app password

# GUI Theme
THEME_COLOR = "#2B2B2B"
ACCENT_COLOR = "#1F538D"
TEXT_COLOR = "#FFFFFF"
# Email Templates
DEFAULT_TEMPLATES = {
    "Welcome": {
        "subject": "Welcome {name}!",
        "body": """
        <h1>Welcome {name}!</h1>
        <p>We're glad to have you on board.</p>
        """
    },
    "Newsletter": {
        "subject": "Monthly Newsletter",
        "body": """
        <h1>Hello {name}!</h1>
        <p>Here's your monthly newsletter.</p>
        """
    }
}
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print("Login successful!")
    server.quit()
except smtplib.SMTPAuthenticationError as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
