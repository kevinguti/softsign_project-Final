import pytest

from src.assertions.taxRates_assertions.taxRates_schema_assertions import AssertionTaxRate
from src.assertions.taxRates_assertions.tax_rate_post_content_assertions import AssertionTaxRateCreate
from src.assertions.taxRates_assertions.tax_rate_errors_assertions import AssertionTaxRateErrors
from src.assertions.status_code_assertions import AssertionStatusCode
from src.resources.payloads.payload_taxRates import PayloadTaxRate
from src.routes.endpoint_tax_rates import EndpointTaxRate
from src.routes.request import SyliusRequest
from src.data.taxRates import generate_tax_rate_data, generate_tax_rate_update_data
from utils.logger_helpers import log_request_response
from src.resources.call_request.taxRates_call import TaxRateCall
from src.services.client import SyliusClient

#Admin > Configuration > Tax Rate > Actualizar Tax Rate válido
@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC206_actualizar_tax_rate_valido(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_output_schema(response_json)
    AssertionTaxRateCreate.assert_tax_rate_update_response(original_data=tax_rate_data, update_payload=update_payload, response_json=response_json)
    log_request_response(url, response, headers, update_payload)


def test_TC207_actualizar_con_nombre_vacio(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data(name="")
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_name_not_blank_error(response_json)
    log_request_response(url, response, headers, update_payload)


def test_TC208_actualizar_con_codigo_inexistente(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data(code="NONEXISTENTCODE")
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_404(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_not_found_error(response_json)
    log_request_response(url, response, headers, update_payload)