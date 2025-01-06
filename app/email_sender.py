import os
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the email from the .env file
EMAIL = os.getenv("GMAIL_USER")

def send_welcome_email(recipient_email: str, first_name: str):
    """Send a welcome email using Gmail API."""
    try:
        # Load credentials from the token file
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])
        service = build("gmail", "v1", credentials=creds)

        # Create the email
        message = EmailMessage()
        message.set_content(f"Hi {first_name},\n\nWelcome to our service!")

        message["To"] = recipient_email
        message["From"] = EMAIL  # Use email from .env
        message["Subject"] = "Welcome to Our Service"

        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        # Send the email
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f"Email sent successfully. Message ID: {send_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")
