import sqlalchemy as sa
from models.BaseModel import BaseModel
from models.Language import Language
from sqlalchemy.orm import relationship
from models.ChargeOrder import ChargeOrder


class User(BaseModel):
    __tablename__ = "users"

    user_id = sa.Column(sa.BigInteger, unique=True)
    username = sa.Column(sa.String)
    name = sa.Column(sa.String)
    lang = sa.Column(sa.Enum(Language), default=Language.ARABIC)
    is_banned = sa.Column(sa.Boolean, default=0)
    is_admin = sa.Column(sa.Boolean, default=0)

    charge_orders = relationship(ChargeOrder)

    balance = sa.Column(sa.Float, default=0)

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, name={self.name}, is_admin={bool(self.is_admin)}, is_banned={bool(self.is_banned)}"
