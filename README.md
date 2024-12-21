# Automated Email Sender

This project is a simple Python-based tool for sending emails to multiple recipients with optional attachments and HTML templates.

## Features
- **Personalized Emails**: Customize email content using placeholders (e.g., `{name}`).
- **HTML Templates**: Use predefined templates for formatting emails.
- **Attachments**: Add files to your emails.
- **CSV Support**: Load recipient lists from a `.csv` file.

## Requirements
- **Python 3.8+**
- Libraries: `customtkinter`, `pandas`, `python-dotenv`

Install dependencies with:
```bash
pip install customtkinter pandas python-dotenv
```

## Setup
1. **Clone the Project**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Configure Email Credentials**:
   ```python
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_app_password
   ```

3. **Prepare Recipients**:
   Create a `recipients.csv` file with this format:
   ```csv
   name,email
   John Doe,john.doe@example.com
   Jane Smith,jane.smith@example.com
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage
1. Load a recipient list by selecting a `.csv` file.
2. Choose or create an email template.
3. Optionally, add attachments.
4. Click "Send Emails" to deliver messages to recipients.

## Notes
- Use App Passwords for Gmail accounts.
- Keep credentials secure by using a `.env` file.

## Troubleshooting
- Ensure email credentials are correct.
- Check recipient email addresses for typos.
- Verify SMTP settings if emails fail to send.

---

Enjoy using the Automated Email Sender!

