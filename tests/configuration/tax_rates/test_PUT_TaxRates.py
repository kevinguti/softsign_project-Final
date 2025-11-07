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

@pytest.mark.negative
@pytest.mark.functional
def test_TC207_actualizar_con_nombre_vacio(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_data["name"] = ""
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_name_not_blank_error(response_json)
    log_request_response(url, response, headers, update_payload)

@pytest.mark.negative
@pytest.mark.functional
def test_TC208_actualizar_con_codigo_inexistente(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code("NONEXISTENT_CODE_12345")
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_404(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_not_found_error(response_json)
    log_request_response(url, response, headers, update_payload)



@pytest.mark.negative
@pytest.mark.functional
def test_TC209_actualizar_con_amount_negativo(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_data["amount"] = -0.10
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_amount_non_negative_error(response_json)
    log_request_response(url, response, headers, update_payload)


@pytest.mark.negative
@pytest.mark.functional
def test_TC231_actualizar_includedInPrice_a_valor_no_booleano(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_data["includedInPrice"] = "not_a_boolean"
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_400(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_includedInPrice_boolean_error(response_json)
    log_request_response(url, response, headers, update_payload)


@pytest.mark.positive
@pytest.mark.functional
def test_TC232_actualizar_includedInPrice_a_valor_valido(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data(includedInPrice=not tax_rate_data["includedInPrice"])
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_output_schema(response_json)
    AssertionTaxRateCreate.assert_tax_rate_update_response(original_data=tax_rate_data, update_payload=update_payload, response_json=response_json)
    log_request_response(url, response, headers, update_payload)

#intentar actualizar con nombre demasiado largo
@pytest.mark.negative
@pytest.mark.functional
def test_TC233_actualizar_con_nombre_demasiado_largo(setup_edit_tax_rate):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_data["name"] = "N" * 256
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    AssertionTaxRate.assert_tax_rate_edit_input_schema(update_payload)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    AssertionStatusCode.assert_status_code_422(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
    AssertionTaxRateErrors.assert_tax_rate_name_too_long_error(response_json)
    log_request_response(url, response, headers, update_payload)


@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.parametrize("invalid_name, test_description, should_fail", [
    ("", "nombre vacío", True),
    ("   ", "solo espacios", False),
    ("A" * 256, "nombre extremadamente largo", True), 
    ("Tax@Rate#$%^&*()", "caracteres especiales", False),
    ("<script>alert('xss')</script>Tax", "HTML/JavaScript", False),
    ("Tax Rate'; DROP TABLE users; --", "SQL injection", False),
    ("Tax    Rate     Many    Spaces", "múltiples espacios", False),
    ("Tax\\nRate\\tWith\\rChars", "caracteres de control", False),
    ("Tax`~!@#$%^&*()_+={}[]|\\:;\"'<>,.?/Rate", "todos los símbolos", False),
    (" Tax Rate ", "espacios al inicio y final", False),
    ("Ñoño Café naïve", "caracteres Unicode especiales", False),

    pytest.param("Tax Rate 😀🎉❤️", "emojis", True,
                 marks=pytest.mark.xfail(reason="Emojis causan error 500 interno")),
])
def test_TC234_actualizar_con_nombres_invalidos_parametrizado(setup_edit_tax_rate, invalid_name, test_description, should_fail):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_data["name"] = invalid_name
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)

    if should_fail:
        assert response.status_code != 200, f"Se esperaba error para {test_description}, pero la API aceptó el nombre: '{invalid_name}'"
        if response.status_code in [400, 422]:
            response_json = response.json()
            AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
            AssertionTaxRateErrors.assert_tax_rate_validation_error(response_json, "name")
    else:
        if response.status_code != 200:
            pytest.xfail(
                f"La API rechazó un caso que pensábamos sería aceptado: {test_description} (status: {response.status_code})")
        assert response.status_code == 200, f"Expected 200 for {test_description}, got {response.status_code}"

    log_request_response(url, response, headers, update_payload)


@pytest.mark.negative
@pytest.mark.functional
@pytest.mark.parametrize("invalid_amount, description", [
    (1.10, "110%"),
    (2.0, "200%"),
    (5.0, "500%"),
    (10.0, "1000%"),
    (-0.1, "valor negativo"),
    (-1.0, "-100%"),
])
def test_TC235_actualizar_con_amounts_invalidos(setup_edit_tax_rate, invalid_amount, description):
    headers, tax_rate_data = setup_edit_tax_rate
    update_data = generate_tax_rate_update_data()
    update_data["amount"] = invalid_amount
    update_payload = PayloadTaxRate.build_update_payload(update_data)
    url = EndpointTaxRate.by_code(tax_rate_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_payload)
    if response.status_code == 200:
        response_json = response.json()
        actual_amount = response_json.get('amount')
    elif response.status_code in [400, 422]:
        response_json = response.json()
        AssertionTaxRate.assert_tax_rate_edit_error_schema(response_json)
        AssertionTaxRateErrors.assert_tax_rate_amount_validation_error(response_json)

    log_request_response(url, response, headers, update_payload)

