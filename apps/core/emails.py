"""
Outbound email helpers built on Resend.

All send_* functions are **best-effort**: if the API key is missing or Resend
returns an error, they log and return False instead of raising. Callers can
fire-and-forget them from a background thread (see `run_in_thread`).
"""

from __future__ import annotations

import logging
import threading
from html import escape
from typing import Callable

import resend
from django.conf import settings

logger = logging.getLogger(__name__)


def _send(
    to: str | list[str],
    subject: str,
    html: str,
    reply_to: str | None = None,
) -> bool:
    """Low-level send. Returns True on success, False otherwise."""
    if not settings.RESEND_API_KEY:
        logger.info("RESEND_API_KEY not set; skipping email to %s", to)
        return False

    resend.api_key = settings.RESEND_API_KEY
    try:
        payload: dict = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [to] if isinstance(to, str) else to,
            "subject": subject,
            "html": html,
        }
        if reply_to:
            payload["reply_to"] = reply_to
        resend.Emails.send(payload)
        return True
    except Exception as exc:  # noqa: BLE001 — Resend SDK raises various concrete errors
        logger.warning("Resend send failed (to=%s, subject=%s): %s", to, subject, exc)
        return False


def run_in_thread(fn: Callable[[], None]) -> None:
    """Start a daemon thread to fire `fn`. Used by views via `transaction.on_commit`."""
    threading.Thread(target=fn, daemon=True).start()


# ─── Templates ────────────────────────────────────────────────────────────

def _shell(title: str, body_html: str) -> str:
    """Minimal, safe HTML wrapper. No external assets, inlined styles only."""
    site_url = settings.FRONTEND_URL
    site_label = site_url.replace("https://", "").replace("http://", "").rstrip("/")
    return f"""\
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{escape(title)}</title></head>
<body style="margin:0;padding:0;background:#0a0f18;color:#e8e8ea;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0a0f18;padding:32px 0;">
    <tr><td align="center">
      <table width="520" cellpadding="0" cellspacing="0" border="0" style="background:#111826;border-radius:16px;padding:32px;border:1px solid #1f2937;">
        <tr><td>
          <p style="margin:0 0 24px;font-family:Georgia,serif;font-size:20px;letter-spacing:-0.01em;color:#fff;">
            <span style="display:inline-block;width:8px;height:8px;background:#e0a53e;border-radius:50%;margin-right:8px;vertical-align:middle;"></span>
            Arivex
          </p>
          {body_html}
          <p style="margin:32px 0 0;padding-top:24px;border-top:1px solid #1f2937;font-size:12px;color:#6b7280;">
            Arivex — Saguenay, QC<br>
            <a href="{escape(site_url)}" style="color:#6b7280;">{escape(site_label)}</a>
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>"""


# ─── Contact notification (to the founder) ────────────────────────────────

def send_contact_notification(
    *,
    name: str,
    email: str,
    message: str,
    company: str = "",
    service: str = "",
    budget: str = "",
    source: str = "",
) -> bool:
    """Ping the founder's inbox when someone fills the /contact form."""
    to = settings.CONTACT_NOTIFY_EMAIL
    if not to:
        return False

    rows = [
        ("Nom", name),
        ("Courriel", email),
        ("Entreprise", company),
        ("Service", service),
        ("Budget", budget),
        ("Provenance", source),
    ]
    rows_html = "".join(
        f'<tr><td style="padding:6px 12px 6px 0;color:#6b7280;font-size:13px;vertical-align:top;">{escape(k)}</td>'
        f'<td style="padding:6px 0;color:#e8e8ea;font-size:14px;">{escape(v)}</td></tr>'
        for k, v in rows
        if v
    )
    body = f"""
      <h2 style="margin:0 0 12px;font-size:22px;color:#fff;">Nouveau message</h2>
      <p style="margin:0 0 20px;color:#9ca3af;font-size:14px;">Reçu via le formulaire de contact.</p>
      <table cellpadding="0" cellspacing="0" border="0" style="width:100%;margin-bottom:20px;">{rows_html}</table>
      <div style="background:#0a0f18;border-left:2px solid #e0a53e;padding:16px;border-radius:4px;">
        <p style="margin:0;white-space:pre-wrap;color:#e8e8ea;font-size:14px;line-height:1.6;">{escape(message)}</p>
      </div>
      <p style="margin:20px 0 0;font-size:13px;color:#9ca3af;">
        Réponds directement à ce courriel — ça ira à {escape(email)}.
      </p>
    """
    return _send(to, f"[Arivex] Message de {name}", _shell("Nouveau message", body), reply_to=email)


# ─── Lead notification (founder ping on product signup) ───────────────────

def send_lead_notification(
    *,
    email: str,
    source: str,
    name: str = "",
    company: str = "",
    phone: str = "",
    notes: str = "",
) -> bool:
    to = settings.CONTACT_NOTIFY_EMAIL
    if not to:
        return False

    rows = [
        ("Produit", source),
        ("Courriel", email),
        ("Nom", name),
        ("Entreprise", company),
        ("Téléphone", phone),
        ("Notes", notes),
    ]
    rows_html = "".join(
        f'<tr><td style="padding:6px 12px 6px 0;color:#6b7280;font-size:13px;vertical-align:top;">{escape(k)}</td>'
        f'<td style="padding:6px 0;color:#e8e8ea;font-size:14px;">{escape(v)}</td></tr>'
        for k, v in rows
        if v
    )
    body = f"""
      <h2 style="margin:0 0 12px;font-size:22px;color:#fff;">Nouveau lead {escape(source)}</h2>
      <table cellpadding="0" cellspacing="0" border="0" style="width:100%;">{rows_html}</table>
    """
    return _send(to, f"[Arivex] Lead {source} — {email}", _shell("Nouveau lead", body), reply_to=email)


# ─── Welcome email (to the new subscriber) ────────────────────────────────

def send_newsletter_welcome(email: str, language: str) -> bool:
    """Welcome the new subscriber right after they've been added to Resend."""
    if language == "en":
        subject = "Welcome to Arivex"
        body = """
          <h2 style="margin:0 0 12px;font-size:22px;color:#fff;">Welcome 👋</h2>
          <p style="margin:0 0 16px;color:#d1d5db;font-size:15px;line-height:1.6;">
            Thanks for subscribing. You'll get one email every couple of weeks —
            short, practical, about automation, AI and building useful software
            for Québec SMBs. No spam, no cross-selling.
          </p>
          <p style="margin:0 0 16px;color:#d1d5db;font-size:15px;line-height:1.6;">
            Got an automation headache in your team? Reply to this email and
            tell me about it — the next newsletter might answer it.
          </p>
          <p style="margin:24px 0 0;color:#e8e8ea;font-size:14px;">Darius — Arivex</p>
        """
    else:
        subject = "Bienvenue chez Arivex"
        body = """
          <h2 style="margin:0 0 12px;font-size:22px;color:#fff;">Bienvenue 👋</h2>
          <p style="margin:0 0 16px;color:#d1d5db;font-size:15px;line-height:1.6;">
            Merci pour l'inscription. Tu recevras un courriel toutes les deux
            semaines environ — court, concret, sur l'automatisation, l'IA et
            l'outillage qui aide vraiment les PME québécoises. Pas de spam,
            pas de revente.
          </p>
          <p style="margin:0 0 16px;color:#d1d5db;font-size:15px;line-height:1.6;">
            Tu as un processus qui te fait perdre des heures chaque semaine ?
            Réponds à ce courriel, raconte-moi — la prochaine newsletter
            répond peut-être à ta question.
          </p>
          <p style="margin:24px 0 0;color:#e8e8ea;font-size:14px;">Darius — Arivex</p>
        """
    return _send(email, subject, _shell(subject, body))
