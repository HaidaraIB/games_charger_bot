import os
import sys
from dotenv import load_dotenv
import asyncio

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import *
from common.common import get_lang


async def main():
    load_dotenv()
    create_tables()
    # p = PaymentMethod.get_by(conds={"id": 1}, eager_load=["addresses"])
    # p = PaymentMethod.get_by(conds={"id": 1})
    # print(p.addresses)
    a = PaymentMethodAddress.get_by(conds={"id": 1})
    print(a.payment_method_name)


asyncio.run(main())
