import pytest

from src.assertions.customergroup_assertions.customer_group_errors_assertions import AssertionCustomerGroupErrors
from src.assertions.customergroup_assertions.customer_group_post_content_assertions import AssertionCustomerGroupCreate
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.resources.call_request.customer_group_call import CustomerGroupCall
from src.data.customer_group import generate_customer_group_source_data
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response

@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.positive
def test_TC153_crear_grupo_clientes_datos_validos(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    AssertionCustomerGroup.assert_customer_group_input_schema(payload)
    AssertionCustomerGroupCreate.assert_customer_group_payload(payload)
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
    AssertionCustomerGroupCreate.assert_customer_group_response(payload, response_json)
    created_customer_groups.append(response_json)


@pytest.mark.functional
@pytest.mark.positive
@pytest.mark.smoke
def test_TC154_crear_grupo_clientes_estructura_json_correcta(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
    created_customer_groups.append(response_json)


# Admin > Customer - Group > TC_155 Verificar que no permita crear grupo con código duplicado
@pytest.mark.functional
@pytest.mark.negative
def test_TC155_crear_grupo_clientes_codigo_duplicado(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    first_response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, first_response, headers, payload)
    AssertionStatusCode.assert_status_code_201(first_response)
    first_response_json = first_response.json()
    created_customer_groups.append(first_response_json)
    duplicate_payload = generate_customer_group_source_data()
    duplicate_payload["code"] = payload["code"]
    second_response = SyliusRequest.post(endpoint, headers, duplicate_payload)
    log_request_response(endpoint, second_response, headers, duplicate_payload)
    AssertionStatusCode.assert_status_code_422(second_response)
    AssertionCustomerGroupErrors.assert_duplicate_error(second_response)


# Admin > Customer - Group > TC_156 Crear grupo sin campo obligatorio 'code'
@pytest.mark.functional
@pytest.mark.negative
def test_TC156_crear_grupo_clientes_sin_codigo(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload.pop("code", None)
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_missing_code_error(response)

# Admin > Customer - Group > TC_157 Crear grupo sin campo obligatorio 'name'
@pytest.mark.functional
@pytest.mark.negative
def test_TC157_crear_grupo_clientes_sin_nombre(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload.pop("name", None)
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_missing_name_error(response)

# Admin > Customer - Group > TC_161 Crear grupo con nombre invalido mas de 255 caracteres
@pytest.mark.functional
@pytest.mark.negative
def test_TC161_crear_grupo_clientes_nombre_mas_255_caracteres(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload["name"] = "A" * 256
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_name_too_long_error(response)

# Admin > Customer - Group > TC_162 Crear grupo con código invalido mas de 255 caracteres
@pytest.mark.functional
@pytest.mark.negative
def test_TC162_crear_grupo_clientes_codigo_mas_255_caracteres(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload["code"] = "C" * 256
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_code_too_long_error(response)

# Admin > Customer - Group > TC_169 Verificar que permita crear múltiples grupos simultáneamente
@pytest.mark.functional
@pytest.mark.positive
def test_TC169_crear_multiples_grupos_clientes_simultaneamente(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload1 = generate_customer_group_source_data()
    payload2 = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response1 = SyliusRequest.post(endpoint, headers, payload1)
    log_request_response(endpoint, response1, headers, payload1)
    AssertionStatusCode.assert_status_code_201(response1)
    response1_json = response1.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response1_json)
    created_customer_groups.append(response1_json)
    response2 = SyliusRequest.post(endpoint, headers, payload2)
    log_request_response(endpoint, response2, headers, payload2)
    AssertionStatusCode.assert_status_code_201(response2)
    response2_json = response2.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response2_json)
    created_customer_groups.append(response2_json)

# Admin > Customer - Group > TC_172 Verificar headers de respuesta
@pytest.mark.functional
@pytest.mark.positive
def test_TC172_crear_grupo_clientes_verificar_headers_respuesta(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    expected_headers = {
        "Content-Type": "application/ld+json; charset=utf-8",
        "Cache-Control": "no-cache, private",
        "Vary": "Accept",
    }
    for header, expected_value in expected_headers.items():
        actual_value = response.headers.get(header)
        assert actual_value == expected_value, f"Header '{header}' esperado '{expected_value}', encontrado '{actual_value}'"
    response_json = response.json()
    created_customer_groups.append(response_json)

# Admin > Customer - Group > TC_173 Verificar que permita crear grupo con código de 1 carácter
@pytest.mark.functional
@pytest.mark.negative
def test_TC173_crear_grupo_clientes_codigo_1_caracter(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload["code"] = "A"
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
    AssertionCustomerGroupCreate.assert_customer_group_response(payload, response_json)
    created_customer_groups.append(response_json)

# Admin > Customer - Group > TC_430 Verificar que permita crear grupo con nombre de 2 carácter
@pytest.mark.functional
@pytest.mark.negative
def test_TC430_crear_grupo_clientes_nombre_2_caracteres(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload["name"] = "AB"
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
    AssertionCustomerGroupCreate.assert_customer_group_response(payload, response_json)
    created_customer_groups.append(response_json)

# Admin > Customer - Group > intentar crear grupo con payload vacío
@pytest.mark.functional
@pytest.mark.negative
def test_crear_grupo_clientes_payload_vacio(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = {}
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_422(response)
    AssertionCustomerGroupErrors.assert_missing_code_error(response)
    AssertionCustomerGroupErrors.assert_missing_name_error(response)

# Admin > Customer - Group > intentar crear un grupo con caracteres especiales en el name
@pytest.mark.functional
@pytest.mark.negative
def test_crear_grupo_clientes_caracteres_especiales_en_nombre(setup_add_customer_group):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload["name"] = "Nómbr@ Especial$"
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)
    AssertionStatusCode.assert_status_code_201(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
    AssertionCustomerGroupCreate.assert_customer_group_response(payload, response_json)
    created_customer_groups.append(response_json)


test_cases = [
    ("Solo espacios", "     ", False),
    ("Solo números", "123456", False),
    ("Caracteres especiales", "Nómbr@ Especial$ & %", False),
    ("Mix válido", "Nombre123 Mix@", False),
    ("SQL Injection", "'; DROP TABLE", True),
    ("HTML tags", "<script>alert()</script>", True),
    ("Emojis", "Nombre 😊🌟", True),
    ("Caracteres raros", "Nombre 𝌆 Test", True),
    ("Muy corto", "A", True),
    ("Con acentos", "María José Niño", False)
]
@pytest.mark.functional
@pytest.mark.negative
@pytest.mark.parametrize("test_name,name_value,should_fail", test_cases)
def test_crear_grupo_clientes_caracteres_especiales_en_nombre(setup_add_customer_group, test_name, name_value,
                                                              should_fail):
    headers, created_customer_groups = setup_add_customer_group
    payload = generate_customer_group_source_data()
    payload["name"] = name_value

    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.post(endpoint, headers, payload)
    log_request_response(endpoint, response, headers, payload)

    if should_fail:
        pytest.xfail(f"Se esperaba que fallara: {test_name}")
        AssertionStatusCode.assert_status_code_422(response)
    else:
        AssertionStatusCode.assert_status_code_201(response)
        response_json = response.json()
        AssertionCustomerGroup.assert_customer_group_output_schema(response_json)
        AssertionCustomerGroupCreate.assert_customer_group_response(payload, response_json)
        created_customer_groups.append(response_json)