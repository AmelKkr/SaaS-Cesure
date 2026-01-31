"""Link Stripe and DB: create/update subscription records."""
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.models.subscription import Subscription


async def get_or_create_subscription_for_user(
    db: AsyncSession, user_id: UUID
) -> Subscription | None:
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id).order_by(Subscription.created_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def upsert_subscription_from_stripe(
    db: AsyncSession,
    user_id: UUID,
    stripe_customer_id: str | None,
    stripe_subscription_id: str | None,
    status: str,
    plan_id: str | None = None,
    current_period_end: datetime | None = None,
) -> Subscription:
    """Create or update subscription record from Stripe webhook data."""
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == user_id).order_by(Subscription.created_at.desc()).limit(1)
    )
    sub = result.scalar_one_or_none()
    if sub:
        sub.stripe_customer_id = stripe_customer_id or sub.stripe_customer_id
        sub.stripe_subscription_id = stripe_subscription_id or sub.stripe_subscription_id
        sub.status = status
        if plan_id is not None:
            sub.plan_id = plan_id
        if current_period_end is not None:
            sub.current_period_end = current_period_end
        await db.flush()
        await db.refresh(sub)
        return sub
    sub = Subscription(
        user_id=user_id,
        stripe_customer_id=stripe_customer_id,
        stripe_subscription_id=stripe_subscription_id,
        status=status,
        plan_id=plan_id,
        current_period_end=current_period_end,
    )
    db.add(sub)
    await db.flush()
    await db.refresh(sub)
    return sub
