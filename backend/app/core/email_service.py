"""SendGrid transactional emails: signup confirmation, reset password."""
import asyncio

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config import get_settings


def _get_client():
    settings = get_settings()
    if not settings.SENDGRID_API_KEY:
        return None
    return SendGridAPIClient(settings.SENDGRID_API_KEY)


async def send_signup_confirmation(email: str, full_name: str | None) -> None:
    """Send welcome/signup confirmation email."""
    client = _get_client()
    if not client:
        return
    settings = get_settings()
    subject = "Bienvenue sur Césure"
    name = full_name or email
    html = f"""
    <p>Bonjour {name},</p>
    <p>Bienvenue sur Césure, la plateforme pour trouver votre stage de 6 mois.</p>
    <p>Vous pouvez dès à présent vous connecter et explorer les offres.</p>
    <p>L'équipe Césure</p>
    """
    message = Mail(
        from_email=(settings.SENDGRID_FROM_EMAIL, settings.SENDGRID_FROM_NAME),
        to_emails=email,
        subject=subject,
        html_content=html,
    )
    try:
        await asyncio.to_thread(client.send, message)
    except Exception:
        pass


async def send_reset_password_email(email: str, token: str) -> None:
    """Send reset password link email."""
    client = _get_client()
    if not client:
        return
    settings = get_settings()
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    subject = "Réinitialisation de votre mot de passe Césure"
    html = f"""
    <p>Bonjour,</p>
    <p>Vous avez demandé la réinitialisation de votre mot de passe.</p>
    <p>Cliquez sur le lien suivant (valide 1 heure) :</p>
    <p><a href="{reset_url}">{reset_url}</a></p>
    <p>Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.</p>
    <p>L'équipe Césure</p>
    """
    message = Mail(
        from_email=(settings.SENDGRID_FROM_EMAIL, settings.SENDGRID_FROM_NAME),
        to_emails=email,
        subject=subject,
        html_content=html,
    )
    try:
        await asyncio.to_thread(client.send, message)
    except Exception:
        pass
