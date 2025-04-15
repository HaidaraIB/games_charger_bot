import sqlalchemy as sa
from models.BaseModel import BaseModel
from sqlalchemy.orm import relationship


class ReferralLink(BaseModel):
    __tablename__ = "referral_links"

    user_id = sa.Column(sa.ForeignKey("users.user_id"))
    link_code = sa.Column(sa.String, unique=True)
    creation_date = sa.Column(sa.TIMESTAMP)

    referral_relations = relationship("ReferralRelation")
