"""Stripe webhooks: verify signature, update subscriptions."""
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import stripe

from app.core.stripe_service import construct_webhook_event
from app.db.session import get_db
from app.db.models.subscription import Subscription
from app.services.subscription_service import upsert_subscription_from_stripe

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Stripe webhook events (checkout.session.completed, customer.subscription.*)."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    try:
        event = construct_webhook_event(payload, sig_header)
    except HTTPException:
        raise

    if event.type == "checkout.session.completed":
        session = event.data.object
        client_reference_id = getattr(session, "client_reference_id", None)
        customer_id = getattr(session, "customer", None)
        subscription_id = getattr(session, "subscription", None)
        if not client_reference_id:
            return {"received": True}
        try:
            user_id = UUID(client_reference_id)
        except ValueError:
            return {"received": True}
        # Fetch subscription details from Stripe for period_end and plan
        current_period_end = None
        plan_id = None
        if subscription_id:
            sub_obj = stripe.Subscription.retrieve(subscription_id)
            current_period_end = getattr(sub_obj, "current_period_end", None)
            items = getattr(getattr(sub_obj, "items", None), "data", None) or []
            if items and getattr(items[0], "price", None):
                plan_id = getattr(items[0].price, "id", None)
        await upsert_subscription_from_stripe(
            db,
            user_id=user_id,
            stripe_customer_id=customer_id,
            stripe_subscription_id=subscription_id,
            status="active",
            plan_id=plan_id,
            current_period_end=datetime.fromtimestamp(current_period_end, tz=timezone.utc) if current_period_end else None,
        )
        return {"received": True}

    if event.type.startswith("customer.subscription."):
        sub_obj = event.data.object
        customer_id = sub_obj.customer
        subscription_id = sub_obj.id
        status = sub_obj.status
        current_period_end_ts = getattr(sub_obj, "current_period_end", None)
        current_period_end = datetime.fromtimestamp(current_period_end_ts, tz=timezone.utc) if current_period_end_ts else None
        plan_id = None
        if getattr(sub_obj, "items", None) and getattr(sub_obj.items, "data", None):
            items = sub_obj.items.data or []
            if items and getattr(items[0], "price", None):
                plan_id = getattr(items[0].price, "id", None)
        # Find subscription by stripe_customer_id
        result = await db.execute(
            select(Subscription).where(Subscription.stripe_customer_id == customer_id).limit(1)
        )
        existing = result.scalar_one_or_none()
        if existing:
            await upsert_subscription_from_stripe(
                db,
                user_id=existing.user_id,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                status=status,
                plan_id=plan_id,
                current_period_end=current_period_end,
            )
        return {"received": True}

    return {"received": True}
