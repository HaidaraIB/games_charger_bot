import sqlalchemy as sa
from models.BaseModel import BaseModel, lock_and_release
from models.User import User
from sqlalchemy.orm import Session
from enum import Enum
from datetime import datetime
from common.constants import *


class OrderStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


class ChargeOrder(BaseModel):
    __tablename__ = "charge_orders"

    user_id = sa.Column(sa.ForeignKey("users.user_id"))
    payment_method_name = sa.Column(sa.ForeignKey("payment_methods.name"))
    photo = sa.Column(sa.String)
    operation_number = sa.Column(sa.String)
    status = sa.Column(sa.Enum(OrderStatus), default=OrderStatus.PENDING)
    decline_reason = sa.Column(sa.String)
    order_date = sa.Column(sa.TIMESTAMP)
    approve_date = sa.Column(sa.TIMESTAMP)
    decline_date = sa.Column(sa.TIMESTAMP)

    @classmethod
    @lock_and_release
    async def decline(
        cls,
        order_id: int,
        decline_reason: str,
        s: Session = None,
    ):

        s.query(cls).filter_by(id=order_id).update(
            {
                cls.status: OrderStatus.DECLINED,
                cls.decline_date: datetime.now(tz=TIMEZONE),
                cls.decline_reason: decline_reason,
            }
        )

    @classmethod
    @lock_and_release
    async def approve(
        cls,
        order_id: int,
        user_id: int,
        amount: float,
        s: Session = None,
    ):
        s.query(cls).filter_by(id=order_id).update(
            {
                cls.status: OrderStatus.APPROVED,
                cls.approve_date: datetime.now(tz=TIMEZONE),
            }
        )
        s.query(User).filter_by(user_id=user_id).update(
            {
                User.balance: User.balance + amount,
            }
        )
