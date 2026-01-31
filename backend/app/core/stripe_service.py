"""Stripe client: checkout session, customer portal, webhook verification."""
from typing import Any

import stripe
from fastapi import Request, HTTPException

from app.config import get_settings


def get_stripe():
    settings = get_settings()
    if not settings.STRIPE_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Stripe not configured")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def create_checkout_session(
    customer_email: str,
    price_id: str,
    success_url: str,
    cancel_url: str,
    client_reference_id: str | None = None,
) -> dict[str, Any]:
    """Create Stripe Checkout Session for subscription."""
    stripe_api = get_stripe()
    session = stripe_api.checkout.Session.create(
        mode="subscription",
        customer_email=customer_email,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=client_reference_id,
    )
    return {"url": session.url, "session_id": session.id}


def create_customer_portal_session(customer_id: str, return_url: str) -> dict[str, Any]:
    """Create Stripe Customer Portal session for managing subscription."""
    stripe_api = get_stripe()
    session = stripe_api.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )
    return {"url": session.url}


def construct_webhook_event(payload: bytes, sig_header: str) -> stripe.Event:
    """Verify and construct Stripe webhook event."""
    settings = get_settings()
    if not settings.STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook secret not configured")
    try:
        return stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {e}")
    except stripe.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {e}")
