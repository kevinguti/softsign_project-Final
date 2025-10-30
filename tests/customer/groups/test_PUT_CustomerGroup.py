import pytest

from src.assertions.customergroup_assertions.customer_group_errors_assertions import AssertionCustomerGroupErrors
from src.assertions.customergroup_assertions.customer_group_post_content_assertions import AssertionCustomerGroupCreate
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response

# Admin > Customer - Group > Actualizar grupo de clientes con datos válidos
@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC271_actualizar_grupo_clientes_valido(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    AssertionCustomerGroup.assert_customer_group_input_schema(update_data)
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
    AssertionCustomerGroupCreate.assert_customer_group_update_response(original_data=customer_group_data, update_payload=update_data, response_json=response_json)
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > Verificar estructura del JSON devuelto al actualizar
@pytest.mark.positive
@pytest.mark.functional
def test_TC272_verificar_estructura_json_actualizar_grupo_clientes(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    AssertionCustomerGroup.assert_customer_group_input_schema(update_data)
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_274 Actualizar grupo sin campo obligatorio 'name'
@pytest.mark.negative
@pytest.mark.functional
def test_TC274_actualizar_grupo_clientes_sin_nombre(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    update_data.pop("name", None)
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    assert response_json["name"] == customer_group_data["name"]
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_282 Verificar que no permita nombre muy largo
@pytest.mark.negative
@pytest.mark.functional
def test_TC282_actualizar_grupo_clientes_nombre_muy_largo(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    update_data["name"] = "A" * 256
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_name_too_long_error(response)
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_283 Verificar que no permita actualizar grupo con caracteres especiales en nombre
@pytest.mark.negative
@pytest.mark.functional
def test_TC283_actualizar_grupo_clientes_nombre_caracteres_especiales(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    update_data["name"] = "@@@###$$$%%%"
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    assert response_json["name"] == update_data["name"], f"El nombre no se actualizó correctamente. Esperado: {update_data['name']}, Obtenido: {response_json['name']}"
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_290 Verificar headers de respuesta
@pytest.mark.positive
@pytest.mark.functional
def test_TC290_verificar_headers_respuesta_actualizar_grupo_clientes(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_200(response)
    expected_headers = {
        "Content-Type": "application/ld+json; charset=utf-8",
        "Cache-Control": "no-cache, private",
        "Vary": "Accept",
    }
    for header, expected_value in expected_headers.items():
        actual_value = response.headers.get(header)
        assert actual_value == expected_value, f"Header '{header}' esperado: '{expected_value}', encontrado: '{actual_value}'"
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_291 Verificar que no permita actualizar grupo con nombre mínimo
@pytest.mark.negative
@pytest.mark.functional
def test_TC291_actualizar_grupo_clientes_nombre_minimo(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    update_data["name"] = "A"
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_422(response)
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_292 Verificar que no permita actualizar grupo con valores null
@pytest.mark.negative
@pytest.mark.functional
def test_TC292_actualizar_grupo_clientes_valores_null(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    update_data["name"] = None
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_400(response)
    AssertionCustomerGroupErrors.assert_name_null_error(response)
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_293 Verificar que no permita actualizar grupo con código inválido
@pytest.mark.negative
@pytest.mark.functional
def test_TC293_actualizar_grupo_clientes_codigo_invalido(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    invalid_code = "invalid_code_!@#"
    url = EndpointCustomerGroup.code(invalid_code)
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, headers, update_data)

# Admin > Customer - Group > TC_294 Verificar que no permita actualizar grupo sin autenticación
@pytest.mark.negative
@pytest.mark.functional
def test_TC294_actualizar_grupo_clientes_sin_autenticacion(setup_edit_customer_group):
    _, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    url = EndpointCustomerGroup.code(customer_group_data["code"])
    response = SyliusRequest.put_ld_json(url, headers={}, payload=update_data)
    AssertionStatusCode.assert_status_code_401(response)
    log_request_response(url, response, headers={}, payload=update_data)

# Admin > Customer - Group > TC_295 Verificar que no permita actualizar grupo con código vacío
@pytest.mark.negative
@pytest.mark.functional
def test_TC295_actualizar_grupo_clientes_codigo_vacio(setup_edit_customer_group):
    headers, customer_group_data = setup_edit_customer_group
    update_data = generate_customer_group_source_data()
    empty_code = ""
    url = EndpointCustomerGroup.code(empty_code)
    response = SyliusRequest.put_ld_json(url, headers, update_data)
    AssertionStatusCode.assert_status_code_404(response)
    log_request_response(url, response, headers, update_data)