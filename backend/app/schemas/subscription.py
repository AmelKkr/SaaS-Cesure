"""Subscription schemas."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubscriptionBase(BaseModel):
    status: str
    plan_id: str | None = None
    current_period_end: datetime | None = None


class SubscriptionResponse(SubscriptionBase):
    id: UUID
    user_id: UUID
    stripe_customer_id: str | None = None
    stripe_subscription_id: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
