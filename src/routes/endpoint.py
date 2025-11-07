from enum import Enum
from utils.config import BASE_URL


class Endpoint(Enum):

    LOGIN = "/api/v2/admin/administrators/token"

    BASE_CUSTOMER_GROUP = "/api/v2/admin/customer-groups"
    BASE_CUSTOMER_GROUP_CODE = "/api/v2/admin/customer-groups/{code}"

    BASE_TAX_CATEGORY = "/api/v2/admin/tax-categories"
    BASE_TAX_CATEGORY_CODE = "/api/v2/admin/tax-categories/{code}"

    BASE_TAX_RATE = "/api/v2/admin/tax-rates"
    BASE_TAX_RATE_ID = "/api/v2/admin/tax-rates/{id}"
    BASE_TAX_RATE_CODE = "/api/v2/admin/tax-rates/{code}"

    BASE_ZONE = "/api/v2/admin/zones"
    BASE_ZONE_CODE = "/api/v2/admin/zones/{code}"


    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"