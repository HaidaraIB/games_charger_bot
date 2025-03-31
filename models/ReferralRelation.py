import sqlalchemy as sa
from models.BaseModel import BaseModel
from models.DB import connect_and_close
from sqlalchemy.orm import Session


class ReferralRelation(BaseModel):
    __tablename__ = "referral_relations"

    inviter_id = sa.Column(sa.ForeignKey("users.user_id"))
    referred_id = sa.Column(sa.ForeignKey("users.user_id"), unique=True)
    link_code = sa.Column(sa.ForeignKey("referral_links.link_code"))
    join_date = sa.Column(sa.TIMESTAMP)

    @classmethod
    @connect_and_close
    def count_relations_by_link(cls, user_id: int, s: Session = None):
        res = s.execute(
            sa.select(cls.link_code, sa.func.count())
            .select_from(cls)
            .where(cls.inviter_id == user_id)
            .group_by(cls.link_code)
        )
        return res.all()