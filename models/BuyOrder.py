import sqlalchemy as sa
from models.BaseModel import BaseModel
from common.constants import *


class BuyOrder(BaseModel):
    __tablename__ = "buy_orders"

    order_id = sa.Column(sa.Integer, unique=True)
    user_id = sa.Column(sa.ForeignKey("users.user_id"))
    product = sa.Column(sa.String)
    group = sa.Column(sa.String)
    category = sa.Column(sa.String)
    price = sa.Column(sa.Float)
    urlsocial = sa.Column(sa.String)
    order_date = sa.Column(sa.TIMESTAMP)
