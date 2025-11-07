import pytest
import requests
from src.assertions.taxRates_assertions.taxRates_schema_assertions import AssertionTaxRate
from src.assertions.taxRates_assertions.tax_rate_get_content_assertions import AssertionTaxRateGetContent
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_rates import EndpointTaxRate
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response
from src.resources.call_request.taxRates_call import TaxRateCall
from src.services.client import SyliusClient


@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC210_obtener_listado_tax_rates_valido(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_list_schema(response_json)
    expected_codes = [tax_rate1_data["code"], tax_rate2_data["code"]]
    AssertionTaxRateGetContent.assert_tax_rate_list_content(response_json, expected_count=None, expected_codes=expected_codes)
    AssertionTaxRateGetContent.assert_tax_rate_pagination(response_json)
    log_request_response(url, response, headers)


@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC211_obtener_tax_rate_por_codigo_valido(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.by_code(tax_rate1_data["code"])
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_code_schema(response_json)
    AssertionTaxRateGetContent.assert_tax_rate_complete_response_with_validation(response_json, tax_rate1_data)
    log_request_response(url, response, headers)


@pytest.mark.negative
@pytest.mark.functional
def test_TC212_obtener_tax_rate_por_codigo_inexistente(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    nonexistent_code = "NONEXISTENT_CODE_123"
    url = EndpointTaxRate.by_code(nonexistent_code)
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, headers)


@pytest.mark.positive
@pytest.mark.functional
def test_TC213_verificar_formato_jsonld_tax_rates(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    content_type = response.headers.get("Content-Type", "")
    AssertionTaxRateGetContent.assert_jsonld_content_type(response)
    AssertionTaxRateGetContent.assert_valid_json_response(response)
    log_request_response(url, response, headers)

@pytest.mark.positive
@pytest.mark.functional
def test_TC214_verificar_esquema_tax_rate_listado(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_list_schema(response_json)
    log_request_response(url, response, headers)

@pytest.mark.positive
@pytest.mark.functional
def test_TC215_verificar_codigo_respuesta_200_OK(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    log_request_response(url, response, headers)

@pytest.mark.positive
@pytest.mark.functional
def test_TC216_validar_paginacion_basica_tax_rate(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.get(EndpointTaxRate.tax_rate_with_params(page=1, itemsPerPage=1), headers)
    AssertionStatusCode.assert_status_code_200(response)
    data = response.json()
    assert isinstance(data.get("hydra:member", []), list)
    assert len(data["hydra:member"]) <= 1
    log_request_response(url, response, headers)


@pytest.mark.negative
@pytest.mark.functional
def test_TC217_verificar_respuesta_token_invalido_sin_autenticacion_tax_rate(auth_headers):
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.get(url, headers={})
    AssertionStatusCode.assert_status_code_401(response)
    response_json = response.json()
    log_request_response(url, response)


@pytest.mark.negative
@pytest.mark.functional
def test_TC218_verificar_respuesta_token_invalido_tax_rate(auth_headers):
    url = EndpointTaxRate.tax_rate()
    invalid_headers = auth_headers.copy()
    invalid_headers["Authorization"] = "Bearer INVALID_TOKEN_123"
    response = SyliusRequest.get(url, headers=invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)
    response_json = response.json()
    log_request_response(url, response, invalid_headers)

@pytest.mark.negative
@pytest.mark.functional
def test_TC219_verificar_respuesta_token_expirado_tax_rate(auth_headers):
    url = EndpointTaxRate.tax_rate()
    expired_headers = auth_headers.copy()
    expired_headers["Authorization"] = "Bearer EXPIRED_TOKEN_123"
    response = SyliusRequest.get(url, headers=expired_headers)
    AssertionStatusCode.assert_status_code_401(response)
    response_json = response.json()
    log_request_response(url, response, expired_headers)

@pytest.mark.negative
@pytest.mark.functional
def test_TC220_verificar_respuesta_metodo_no_permitido_tax_rate(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    log_request_response(url, response, headers)

@pytest.mark.positive
@pytest.mark.functional
def test_TC221_verificar_headers_respuesta_tax_rate(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    content_type = response.headers.get("Content-Type", "")
    assert "application/ld+json" in content_type, "El Content-Type no es application/ld+json"
    log_request_response(url, response, headers)