import sqlalchemy as sa
from models.DB import lock_and_release
from sqlalchemy.orm import Session, relationship
from enum import Enum
from models.BaseModel import BaseModel
from models.PaymentMethodAddress import PaymentMethodAddress
from models.ChargeOrder import ChargeOrder


class PaymentMethodName(Enum):
    SYRCASH = "Syriatel Cash🇸🇾"
    MTNCASH = "MTN Cash🇸🇾"
    USDT = "USDT"


class PaymentMethod(BaseModel):
    __tablename__ = "payment_methods"
    name = sa.Column(sa.Enum(PaymentMethodName), unique=True)
    is_on = sa.Column(sa.Boolean, default=1)
    addresses = relationship(PaymentMethodAddress)
    charge_orders = relationship(ChargeOrder)

    @classmethod
    @lock_and_release
    async def init_payment_methods(cls, s: Session = None):
        s.execute(
            sa.insert(cls)
            .values(
                [
                    {
                        "name": method,
                    }
                    for method in PaymentMethodName
                ]
            )
            .prefix_with("OR IGNORE")
        )
