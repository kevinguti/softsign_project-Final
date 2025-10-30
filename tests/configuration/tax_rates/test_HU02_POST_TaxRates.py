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


@pytest.mark.smoke
@pytest.mark.positive
@pytest.mark.functional
def test_TC193_Crear_tasa_impuesto_exitosamente(setup_add_tax_rate):
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

@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.functional
def test_TC194_crear_tax_rate_con_codigo_duplicado(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    url = EndpointTaxRate.tax_rate()
    first_response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(first_response)
    created_tax_rates.append(first_response.json())
    duplicate_response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(duplicate_response)
    response_json = duplicate_response.json()
    AssertionTaxRateErrors.assert_tax_rate_error_schema(response_json)
    AssertionTaxRateErrors.assert_duplicate_code_error(response_json)
    log_request_response(url, duplicate_response, headers, payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC195_crear_tax_rate_sin_nombre(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    del payload["name"]
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_tax_rate_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, expected_error_field="name")
    log_request_response(url, response, headers, payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC196_crear_tax_rate_con_nombre_superior_a_255_caracteres(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["name"] = "A" * 256
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_tax_rate_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, expected_error_field="name")
    log_request_response(url, response, headers, payload)


@pytest.mark.negative
@pytest.mark.functional
def test_TC197_crear_tax_rate_con_amount_fuera_de_rango(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["amount"] = 150.0
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_tax_rate_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, expected_error_field="amount")
    log_request_response(url, response, headers, payload)


@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.parametrize("invalid_amount,expected_status,xfail_reason", [
    ("INVALID_AMOUNT", 400, None),  #
    (-1.0, 422, None),
    ("", 400, "BUG: La app permite espacios vacíos"),
    ("150%", 400, "BUG: La app permite strings con símbolos"),
    (None, 400, "BUG: La app permite valores nulos"),
])
def test_TC197_crear_tax_rate_con_amount_invalido(setup_add_tax_rate, invalid_amount, expected_status, xfail_reason):
    if xfail_reason:
        pytest.xfail(reason=xfail_reason)
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["amount"] = invalid_amount
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    print(f"\nTesting amount: {invalid_amount} -> Expected: {expected_status}, Got: {response.status_code}")
    if expected_status == 400:
        AssertionStatusCode.assert_status_code_400(response)
    elif expected_status == 422:
        AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_tax_rate_error_schema(response_json)
    if invalid_amount == -1.0:
        AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, "amount")
    else:
        AssertionTaxRateErrors.assert_invalid_amount_error(response_json)
    log_request_response(url, response, headers, payload)


@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.parametrize("extreme_amount,description", [
    (999.99, "tax_rate_muy_alto"),
    (0.00, "tax_rate_cero"),
    (1.50, "tax_rate_mayor_100_porciento"),
])
def test_TC198_crear_tax_rate_con_amounts_extremos(setup_add_tax_rate, extreme_amount, description):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["amount"] = extreme_amount
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_output_schema(response_json)
    created_tax_rates.append(response_json)
    log_request_response(url, response, headers, payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC200_crear_tax_rate_sin_codigo(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    del payload["code"]
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_tax_rate_error_schema(response_json)
    AssertionTaxRateErrors.assert_required_field_error(response_json, "code")
    log_request_response(url, response, headers, payload)


@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.parametrize("invalid_included,expected_status,xfail_reason", [
    ("not_boolean", 400, None),
    (2, 400, None),
    ("", 400, "BUG: La app permite espacios vacíos"),
    (None, 400, "BUG: La app permite valores nulos"),
])
def test_TC199_crear_tax_rate_con_includedInPrice_invalido(setup_add_tax_rate, invalid_included, expected_status, xfail_reason):
    if xfail_reason:
        pytest.xfail(reason=xfail_reason)
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["includedInPrice"] = invalid_included
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    if expected_status == 400:
        AssertionStatusCode.assert_status_code_400(response)
    elif expected_status == 422:
        AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_tax_rate_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, expected_error_field="includedInPrice")
    log_request_response(url, response, headers, payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC201_crear_tax_rate_sin_zone(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["zone"] = "/api/v2/admin/zones/INEXISTENTE_12345"
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_zone_not_found_error(response_json)
    log_request_response(url, response, headers, payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC202_crear_tax_rate_sin_category(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["category"] = "/api/v2/admin/tax-categories/INEXISTENTE_12345"
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_category_not_found_error(response_json)
    log_request_response(url, response, headers, payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC205_crear_tax_rate_con_rango_fechas_invalido(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["startDate"] = "2024-12-31T23:59:59+00:00"
    payload["endDate"] = "2024-01-01T00:00:00+00:00"
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_invalid_date_range_error(response_json)
    log_request_response(url, response, headers, payload)


@pytest.mark.positive
@pytest.mark.functional
def test_TC203_crear_tax_rate_con_rango_fechas_validos(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data(include_dates=True)
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_output_schema(response_json)
    AssertionTaxRateCreate.assert_tax_rate_response(payload, response_json)
    AssertionTaxRateCreate.assert_tax_rate_dates(payload, response_json)
    created_tax_rates.append(response_json)
    log_request_response(url, response, headers, payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC204_crear_tax_rate_con_endDate_anterior_a_startDate(setup_add_tax_rate):
    headers, created_tax_rates = setup_add_tax_rate
    payload = generate_tax_rate_data()
    payload["startDate"] = "2024-12-31T23:59:59+00:00"
    payload["endDate"] = "2024-01-01T00:00:00+00:00"
    url = EndpointTaxRate.tax_rate()
    response = SyliusRequest.post(url, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRateErrors.assert_invalid_date_range_error(response_json)
    log_request_response(url, response, headers, payload)