"""Subscriptions routes: plans, checkout, portal."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.permissions import get_current_user
from app.core.stripe_service import create_checkout_session, create_customer_portal_session
from app.db.session import get_db
from app.db.models.user import User
from app.services.subscription_service import get_or_create_subscription_for_user

router = APIRouter()


@router.get("/plans")
async def get_plans():
    """List subscription plans (from config or Stripe)."""
    settings = get_settings()
    if not settings.STRIPE_PRICE_ID:
        return {"plans": []}
    return {
        "plans": [
            {
                "price_id": settings.STRIPE_PRICE_ID,
                "name": "Césure Pro",
                "description": "Accès complet aux stages 6 mois",
            }
        ]
    }


@router.post("/checkout")
async def create_checkout(
    current_user: User = Depends(get_current_user),
):
    """Create Stripe Checkout Session; return URL to redirect."""
    settings = get_settings()
    if not settings.STRIPE_PRICE_ID:
        raise HTTPException(status_code=503, detail="Stripe price not configured")
    success_url = f"{settings.FRONTEND_URL}/dashboard?checkout=success"
    cancel_url = f"{settings.FRONTEND_URL}/dashboard?checkout=cancel"
    result = create_checkout_session(
        customer_email=current_user.email,
        price_id=settings.STRIPE_PRICE_ID,
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=str(current_user.id),
    )
    return result


@router.post("/portal")
async def create_portal(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create Stripe Customer Portal session; return URL to redirect."""
    sub = await get_or_create_subscription_for_user(db, current_user.id)
    if not sub or not sub.stripe_customer_id:
        raise HTTPException(status_code=400, detail="No subscription or Stripe customer found")
    settings = get_settings()
    return_url = f"{settings.FRONTEND_URL}/dashboard"
    result = create_customer_portal_session(sub.stripe_customer_id, return_url)
    return result
