from enum import Enum
from utils.config import BASE_URL


class Endpoint(Enum):

    LOGIN = "/api/v2/admin/administrators/token"

    BASE_CUSTOMER_GROUP = "/api/v2/admin/customer-groups"
    BASE_CUSTOMER_GROUP_CODE = "/api/v2/admin/customer-groups/{code}"

    BASE_TAX_CATEGORY = "/api/v2/admin/tax-categories"
    BASE_TAX_CATEGORY_CODE = "/api/v2/admin/tax-categories/{code}"

    @classmethod
    def login(cls):
        return f"{BASE_URL}{cls.LOGIN.value}"