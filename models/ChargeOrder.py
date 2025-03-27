import sqlalchemy as sa
from models.BaseModel import BaseModel


class ChargeOrder(BaseModel):
    __tablename__ = "charge_orders"

    user_id = sa.Column(sa.ForeignKey("users.user_id"))
    payment_method_name = sa.Column(sa.ForeignKey("payment_methods.name"))
    photo = sa.Column(sa.String)
    operation_number = sa.Column(sa.String)
    order_date = sa.Column(sa.TIMESTAMP)