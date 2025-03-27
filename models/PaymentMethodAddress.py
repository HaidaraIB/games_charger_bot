import sqlalchemy as sa
from models.BaseModel import BaseModel


class PaymentMethodAddress(BaseModel):
    __tablename__ = "payment_method_addresses"
    payment_method_name = sa.Column(sa.ForeignKey("payment_methods.name"))
    address = sa.Column(sa.String)

    __table_args__ = (
        sa.UniqueConstraint(
            "payment_method_name",
            "address",
            name="payment_method_name_address_unq",
        ),
    )
