import os
import json
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def authenticate():
    """Authenticate with Gmail API and create a token.json file if it doesn't exist."""
    if not os.path.exists("token.json"):
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)

        # Save credentials to token.json
        with open("token.json", "w") as token_file:
            token_file.write(json.dumps({
                "token": creds.token,
                "refresh_token": creds.refresh_token,
                "token_uri": creds.token_uri,
                "client_id": creds.client_id,
                "client_secret": creds.client_secret,
                "scopes": creds.scopes,
            }))
        print("Authentication successful. Token saved to token.json.")

def send_welcome_email(recipient_email: str, first_name: str):
    """Send a welcome email using Gmail API."""
    try:
        # Authenticate if token.json is missing
        authenticate()

        # Load credentials
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        service = build("gmail", "v1", credentials=creds)

        # Create the email
        message = EmailMessage()
        message.set_content(f"Hi {first_name},\n\nWelcome to our service!")
        message["To"] = recipient_email
        message["From"] = "your-email@gmail.com"  # Replace with your email
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
