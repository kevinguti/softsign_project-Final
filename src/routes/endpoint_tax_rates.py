import urllib.parse
from src.routes.endpoint import Endpoint
from utils.config import BASE_URL

class EndpointTaxRate:

    @classmethod
    def tax_rate(cls):
        return f"{BASE_URL}{Endpoint.BASE_TAX_RATE.value}"

    @classmethod
    def tax_rate_with_params(cls, **params):
        base_url = f"{BASE_URL}{Endpoint.BASE_TAX_RATE.value}"
        if params:
            query_string = urllib.parse.urlencode(params)
            return f"{base_url}?{query_string}"
        return base_url

    @staticmethod
    def build_url_tax_rate(base, identifier):
        return f"{BASE_URL}{base.format(id=identifier, code=identifier)}"

    @classmethod
    def by_id(cls, tax_rate_id):
        return cls.build_url_tax_rate(Endpoint.BASE_TAX_RATE_ID.value, tax_rate_id)

    @classmethod
    def by_code(cls, tax_rate_code):
        return cls.build_url_tax_rate(Endpoint.BASE_TAX_RATE_CODE.value, tax_rate_code)

# NUEVA CLASE PARA ZONES
class EndpointZone:

    @classmethod
    def zone(cls):
        return f"{BASE_URL}{Endpoint.BASE_ZONE.value}"

    @classmethod
    def zone_with_params(cls, **params):
        base_url = f"{BASE_URL}{Endpoint.BASE_ZONE.value}"
        if params:
            query_string = urllib.parse.urlencode(params)
            return f"{base_url}?{query_string}"
        return base_url

    @staticmethod
    def build_url_zone(base, zone_code):
        return f"{BASE_URL}{base.format(code=zone_code)}"

    @classmethod
    def by_code(cls, zone_code):
        return cls.build_url_zone(Endpoint.BASE_ZONE_CODE.value, zone_code)