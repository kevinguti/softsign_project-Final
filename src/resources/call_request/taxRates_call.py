from src.routes.endpoint_tax_rates import EndpointTaxRate
from src.routes.request import SyliusRequest

class TaxRateCall:
    @classmethod
    def view_by_id(cls, headers, tax_rate_id):
        response = SyliusRequest().get(EndpointTaxRate.by_id(tax_rate_id), headers)
        return response

    @classmethod
    def view_by_code(cls, headers, tax_rate_code):
        response = SyliusRequest().get(EndpointTaxRate.by_code(tax_rate_code), headers)
        return response

    @classmethod
    def view_all(cls, headers, **params):
        url = EndpointTaxRate.tax_rate_with_params(**params) if params else EndpointTaxRate.tax_rate()
        response = SyliusRequest().get(url, headers)
        return response

    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest().post(EndpointTaxRate.tax_rate(), headers, payload)
        return response  # Devuelve el objeto Response completo

    @classmethod
    def update_by_id(cls, headers, payload, tax_rate_id):
        response = SyliusRequest().put(EndpointTaxRate.by_id(tax_rate_id), headers, payload)
        return response

    @classmethod
    def update_by_code(cls, headers, payload, tax_rate_code):
        response = SyliusRequest().put(EndpointTaxRate.by_code(tax_rate_code), headers, payload)
        return response

    @classmethod
    def delete_by_id(cls, headers, tax_rate_id):
        response = SyliusRequest().delete(EndpointTaxRate.by_id(tax_rate_id), headers)
        return response

    @classmethod
    def delete_by_code(cls, headers, tax_rate_code):
        response = SyliusRequest().delete(EndpointTaxRate.by_code(tax_rate_code), headers)
        return response