import logging

import resend
from django.conf import settings

logger = logging.getLogger(__name__)


def _audience_for(language: str) -> str:
    if language == "en":
        return settings.RESEND_AUDIENCE_EN
    return settings.RESEND_AUDIENCE_FR


def create_contact(email: str, language: str) -> str | None:
    """Create a contact in the correct Resend Audience. Returns the Resend contact ID or None on failure."""
    if not settings.RESEND_API_KEY:
        logger.info("RESEND_API_KEY not set; skipping Resend sync for %s", email)
        return None

    audience_id = _audience_for(language)
    if not audience_id:
        logger.warning("No Resend Audience configured for language=%s", language)
        return None

    resend.api_key = settings.RESEND_API_KEY
    try:
        response = resend.Contacts.create(
            {
                "email": email,
                "audience_id": audience_id,
                "unsubscribed": False,
            }
        )
        return response.get("id")
    except Exception as exc:
        logger.warning("Resend create_contact failed for %s: %s", email, exc)
        try:
            existing = resend.Contacts.get(email=email, audience_id=audience_id)
            return existing.get("id") if existing else None
        except Exception as inner:
            logger.warning("Resend fallback lookup failed for %s: %s", email, inner)
            return None


def remove_contact(email: str, language: str) -> bool:
    if not settings.RESEND_API_KEY:
        return False
    audience_id = _audience_for(language)
    if not audience_id:
        return False
    resend.api_key = settings.RESEND_API_KEY
    try:
        resend.Contacts.remove(email=email, audience_id=audience_id)
        return True
    except Exception as exc:
        logger.warning("Resend remove_contact failed for %s: %s", email, exc)
        return False
