from aiosmtplib import SMTP
from email.message import EmailMessage
from backend.app.core.config import EMAIL_USERNAME, EMAIL_PASSWORD, API_URL

smtp = SMTP(hostname="smtp.gmail.com", port=587, username=EMAIL_USERNAME, password=EMAIL_PASSWORD)


async def send_new_account_email(user_email: str, confirm_token: str):
    message = EmailMessage()
    message["From"] = EMAIL_USERNAME
    message["To"] = user_email
    message["Subject"] = "Email confirmation"
    message.set_content(f"Follow the link to confirm your email:"
                                 f" {API_URL}/confirm-email/{confirm_token}")

    async with smtp:
        await smtp.send_message(message)
