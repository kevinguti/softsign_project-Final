import pytest
import time

from src.assertions.customergroup_assertions.customer_group_errors_assertions import AssertionCustomerGroupErrors
from src.assertions.customergroup_assertions.customer_group_get_content_assertions import AssertionCustomerGroupFields
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.customergroup_assertions.customer_group_performance_assertions import AssertionCustomerGroupPerformance
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response


# Admin > Customer - Group > Eliminar grupo de clientes existente
@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC293_eliminar_grupo_clientes_existente(setup_delete_customer_group):
    headers, customer_group_data = setup_delete_customer_group
    customer_group_code = customer_group_data["code"]
    delete_url = EndpointCustomerGroup.code(customer_group_code)
    delete_response = SyliusRequest.delete(delete_url, headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    get_response = SyliusRequest.get(delete_url, headers)
    AssertionStatusCode.assert_status_code_404(get_response)
    error_response = get_response.json()
    AssertionCustomerGroupFields.assert_customer_group_not_found_error(error_response)
    log_request_response(delete_url, delete_response, headers)


# Admin > Customer - Group > Verificar que no permita eliminar grupo con código inexistente
@pytest.mark.negative
@pytest.mark.functional
def test_TC294_eliminar_grupo_codigo_inexistente(auth_headers):
    codigo_inexistente = "grupo_inexistente_12345"
    endpoint = EndpointCustomerGroup.code(codigo_inexistente)
    response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_404(response)
    AssertionCustomerGroupErrors.assert_not_found_error(response)


# Admin > Customer - Group > Verificar que no permita eliminar grupo con token inválido
@pytest.mark.negative
@pytest.mark.security
def test_TC296_eliminar_grupo_token_invalido():
    codigo_existente = "retail"
    invalid_headers = {"Authorization": "Bearer token_invalido"}
    endpoint = EndpointCustomerGroup.code(codigo_existente)
    response = SyliusRequest.delete(endpoint, invalid_headers)
    log_request_response(endpoint, response, headers=invalid_headers)
    AssertionStatusCode.assert_status_code_401(response)


# Admin > Customer - Group > Verificar headers de respuesta al eliminar
@pytest.mark.functional
@pytest.mark.low
def test_TC298_verificar_headers_respuesta_eliminacion(auth_headers):
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    customer_group_code = create_response.json()["code"]
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.delete(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_204(response)
    performance_assertions = AssertionCustomerGroupPerformance()
    performance_assertions.assert_delete_empty_response(response)


# Admin > Customer - Group > Verificar que el grupo eliminado no exista más
@pytest.mark.functional
@pytest.mark.high
def test_TC299_verificar_grupo_eliminado_no_existe(setup_delete_customer_group):
    headers, customer_group_data = setup_delete_customer_group
    customer_group_code = customer_group_data["code"]
    delete_endpoint = EndpointCustomerGroup.code(customer_group_code)
    delete_response = SyliusRequest.delete(delete_endpoint, headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    get_endpoint = EndpointCustomerGroup.code(customer_group_code)
    get_response = SyliusRequest.get(get_endpoint, headers)
    log_request_response(get_endpoint, get_response, headers=headers)
    AssertionStatusCode.assert_status_code_404(get_response)
    AssertionCustomerGroupErrors.assert_not_found_error(get_response)


# Admin > Customer - Group > Verificar que no permita eliminar el mismo grupo dos veces
@pytest.mark.negative
@pytest.mark.functional
def test_TC300_eliminar_mismo_grupo_dos_veces(setup_delete_customer_group):
    headers, customer_group_data = setup_delete_customer_group
    customer_group_code = customer_group_data["code"]
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    first_delete_response = SyliusRequest.delete(endpoint, headers)
    AssertionStatusCode.assert_status_code_204(first_delete_response)
    second_delete_response = SyliusRequest.delete(endpoint, headers)
    log_request_response(endpoint, second_delete_response, headers=headers)
    AssertionStatusCode.assert_status_code_404(second_delete_response)
    AssertionCustomerGroupErrors.assert_not_found_error(second_delete_response)


# Admin > Customer - Group > Verificar eliminación de múltiples grupos secuencialmente
@pytest.mark.functional
@pytest.mark.positive
@pytest.mark.smoke
def test_TC307_eliminar_multiples_grupos_secuencialmente(setup_multiple_customer_groups):
    headers, created_group_codes = setup_multiple_customer_groups
    for group_code in created_group_codes:
        endpoint = EndpointCustomerGroup.code(group_code)
        response = SyliusRequest.delete(endpoint, headers)
        log_request_response(endpoint, response, headers=headers)
        AssertionStatusCode.assert_status_code_204(response)


#verificar que la respueta de eliminar un grupo de clientes este vacia por que no devuelve nada
@pytest.mark.functional
@pytest.mark.positive
def test_TC308_verificar_respuesta_eliminar_grupo_vacia(setup_delete_customer_group):
    headers, customer_group_data = setup_delete_customer_group
    customer_group_code = customer_group_data["code"]
    delete_url = EndpointCustomerGroup.code(customer_group_code)
    delete_response = SyliusRequest.delete(delete_url, headers)
    log_request_response(delete_url, delete_response, headers=headers)
    AssertionStatusCode.assert_status_code_204(delete_response)
    assert delete_response.text == "", "La respuesta de eliminar grupo de clientes no está vacía"