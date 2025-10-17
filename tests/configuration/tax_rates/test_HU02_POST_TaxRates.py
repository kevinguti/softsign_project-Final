import pytest

from src.assertions.taxRates_assertions.taxRates_schema_assertions import AssertionTaxRate
from src.assertions.taxRates_assertions.tax_rate_post_content_assertions import AssertionTaxRateCreate
from src.assertions.taxRates_assertions.tax_rate_errors_assertions import AssertionTaxRateErrors
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_rates import EndpointTaxRate
from src.routes.request import SyliusRequest
from src.data.taxRates import generate_tax_rate_data
from utils.logger_helpers import log_request_response
from src.resources.call_request.taxRates_call import TaxRateCall
from src.services.client import SyliusClient

"""
TCXX - Crear tasa de impuesto exitosamente: La API debe permitir crear una tasa de impuesto
cuando se envían datos válidos. Esperado: HTTP 201 Created y estructura JSON correcta.
"""
@pytest.mark.high
@pytest.mark.smoke
@pytest.mark.functional
def test_TCXX_Crear_tasa_impuesto_exitosamente(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionTaxRate.assert_tax_rate_input_schema(payload)
    AssertionTaxRateCreate.assert_tax_rate_payload(payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_output_schema(response_json)
    AssertionTaxRateCreate.assert_tax_rate_response(payload, response_json)
    log_request_response(url, response, headers, payload)
    created_tax_rates.append(response_json)