import sqlalchemy as sa
from models.BaseModel import BaseModel
from models.Language import Language
from models.ReferralLink import ReferralLink
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"

    user_id = sa.Column(sa.BigInteger, unique=True)
    username = sa.Column(sa.String)
    name = sa.Column(sa.String)
    lang = sa.Column(sa.Enum(Language), default=Language.ARABIC)
    is_banned = sa.Column(sa.Boolean, default=0)
    is_admin = sa.Column(sa.Boolean, default=0)

    balance = sa.Column(sa.Float, default=0)

    charge_orders = relationship("ChargeOrder")
    referral_links: list[ReferralLink] = relationship("ReferralLink")
    invited_users = relationship(
        "ReferralRelation", foreign_keys="[ReferralRelation.inviter_id]"
    )
    referrals_received = relationship(
        "ReferralRelation", foreign_keys="[ReferralRelation.referred_id]"
    )

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, name={self.name}, is_admin={bool(self.is_admin)}, is_banned={bool(self.is_banned)}"
