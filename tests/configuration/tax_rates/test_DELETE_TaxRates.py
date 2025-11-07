import pytest
from src.assertions.taxRates_assertions.taxRates_schema_assertions import AssertionTaxRate
from src.assertions.taxRates_assertions.tax_rate_errors_assertions import AssertionTaxRateErrors
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_rates import EndpointTaxRate
from src.routes.request import SyliusRequest
from src.data.taxRates import generate_tax_rate_data
from utils.logger_helpers import log_request_response
from src.resources.call_request.taxRates_call import TaxRateCall
from src.services.client import SyliusClient
from src.assertions.taxRates_assertions.tax_rate_get_content_assertions import AssertionTaxRateGetContent


@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC222_eliminar_tax_rate_existente(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    tax_rate_code = tax_rate_data["code"]
    delete_url = EndpointTaxRate.by_code(tax_rate_code)
    delete_response = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    get_response = SyliusRequest.get(delete_url, headers)
    AssertionStatusCode.assert_status_code_404(get_response)
    log_request_response(delete_url, delete_response, headers)

@pytest.mark.negative
@pytest.mark.functional
def test_TC223_eliminar_tax_rate_inexistente(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    nonexistent_code = "NONEXISTENT_CODE_456"
    delete_url = EndpointTaxRate.by_code(nonexistent_code)
    delete_response = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_404(delete_response)
    log_request_response(delete_url, delete_response, headers)


@pytest.mark.negative
@pytest.mark.functional
def test_TC224_eliminar_tax_rate_sin_autenticacion():
    nonexistent_code = "NONEXISTENT_CODE_789"
    delete_url = EndpointTaxRate.by_code(nonexistent_code)
    delete_response = SyliusRequest.delete(delete_url, headers={})
    AssertionStatusCode.assert_status_code_401(delete_response)
    log_request_response(delete_url, delete_response, headers={})

@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC225_eliminar_varios_tax_rates(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    tax_rate1_code = tax_rate1_data["code"]
    tax_rate2_code = tax_rate2_data["code"]
    delete_url1 = EndpointTaxRate.by_code(tax_rate1_code)
    delete_url2 = EndpointTaxRate.by_code(tax_rate2_code)
    delete_response1 = SyliusRequest.delete(delete_url1, headers)
    AssertionStatusCode.assert_status_code_204(delete_response1)
    delete_response2 = SyliusRequest.delete(delete_url2, headers)
    AssertionStatusCode.assert_status_code_204(delete_response2)
    get_response1 = SyliusRequest.get(delete_url1, headers)
    AssertionStatusCode.assert_status_code_404(get_response1)
    get_response2 = SyliusRequest.get(delete_url2, headers)
    AssertionStatusCode.assert_status_code_404(get_response2)
    log_request_response(delete_url1, delete_response1, headers)
    log_request_response(delete_url2, delete_response2, headers)

@pytest.mark.positive
@pytest.mark.functional
def test_TC226_eliminar_tax_rate_y_verificar_respuesta_sin_cuerpo(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    tax_rate_code = tax_rate_data["code"]
    delete_url = EndpointTaxRate.by_code(tax_rate_code)
    delete_response = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    assert delete_response.text == "", "La respuesta de eliminación no está vacía"
    log_request_response(delete_url, delete_response, headers)

@pytest.mark.negative
@pytest.mark.functional
def test_TC227_eliminar_tax_rate_con_token_expirado(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    tax_rate_code = tax_rate_data["code"]
    expired_headers = headers.copy()
    expired_headers["Authorization"] = "Bearer expired_token_example"
    delete_url = EndpointTaxRate.by_code(tax_rate_code)
    delete_response = SyliusRequest.delete(delete_url, expired_headers)
    AssertionStatusCode.assert_status_code_401(delete_response)
    log_request_response(delete_url, delete_response, expired_headers)


#verificar que no se pueda eliminar el mismo tax rate dos veces
@pytest.mark.negative
@pytest.mark.functional
def test_TC228_eliminar_mismo_tax_rate_dos_veces(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    tax_rate_code = tax_rate_data["code"]
    delete_url = EndpointTaxRate.by_code(tax_rate_code)
    delete_response1 = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_204(delete_response1)
    delete_response2 = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_404(delete_response2)
    log_request_response(delete_url, delete_response1, headers)
    log_request_response(delete_url, delete_response2, headers)

@pytest.mark.negative
@pytest.mark.functional
def test_TC229_eliminar_tax_rate_con_headers_incorrectos(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    tax_rate_code = tax_rate_data["code"]
    incorrect_headers = {
        "Authorization": "Bearer token_invalido_12345",
        "Content-Type": "application/ld+json"
    }
    delete_url = EndpointTaxRate.by_code(tax_rate_code)
    delete_response = SyliusRequest.delete(delete_url, incorrect_headers)
    AssertionStatusCode.assert_status_code_401(delete_response)
    log_request_response(delete_url, delete_response, incorrect_headers)


@pytest.mark.negative
@pytest.mark.functional
def test_TC230_eliminar_tax_rate_con_codigo_malformado(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    malformed_code = "!!!@@@###"
    delete_url = EndpointTaxRate.by_code(malformed_code)
    delete_response = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_404(delete_response)
    log_request_response(delete_url, delete_response, headers)

@pytest.mark.negative
@pytest.mark.functional
def test_TC231_eliminar_tax_rate_con_codigo_nulo(setup_delete_tax_rate):
    headers, tax_rate_data = setup_delete_tax_rate
    null_code = ""
    delete_url = EndpointTaxRate.by_code(null_code)
    delete_response = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_404(delete_response)
    log_request_response(delete_url, delete_response, headers)
