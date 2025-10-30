import pytest

from src.assertions.customergroup_assertions.customer_group_get_content_assertions import AssertionCustomerGroupFields
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.customergroup_assertions.customer_group_performance_assertions import AssertionCustomerGroupPerformance
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response



@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.positive
def test_TC130_obtener_lista_grupos_clientes_exitoso(setup_teardown_view_customer_group):
    headers, group1_data, group2_data = setup_teardown_view_customer_group
    url = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_list_schema(response_json)
    expected_codes = [group1_data["code"], group2_data["code"]]
    AssertionCustomerGroupFields.assert_customer_group_list_content(response_json, expected_count=None, expected_codes=expected_codes)
    AssertionCustomerGroupFields.assert_customer_group_pagination(response_json)
    log_request_response(url, response, headers)

# Admin > Customer - Group > TC_177 Verificar estructura del JSON devuelto
@pytest.mark.functional
@pytest.mark.positive
def test_TC177_verificar_estructura_json_respuesta(setup_teardown_view_customer_group):
    headers, group1_data, group2_data = setup_teardown_view_customer_group
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, headers)
    log_request_response(endpoint, response, headers=headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(response_json)
    AssertionCustomerGroupFields.assert_customer_group_list_content(response_json, expected_codes=[group1_data["code"], group2_data["code"]])


# Admin > Customer - Group > TC_178 Verificar que se puede obtener un grupo específico usando un código existente
@pytest.mark.functional
@pytest.mark.positive
@pytest.mark.smoke
def test_TC178_obtener_grupo_por_codigo_existente(setup_teardown_view_customer_group):
    headers, group1_data, group2_data = setup_teardown_view_customer_group
    endpoint = EndpointCustomerGroup.code(group1_data["code"])
    response = SyliusRequest.get(endpoint, headers)
    log_request_response(endpoint, response, headers=headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionCustomerGroup.assert_customer_group_code_schema(response_json)
    AssertionCustomerGroupFields.assert_customer_group_complete_response(response_json, group1_data)


# Admin > Customer - Group > TC_180 Verificar que los campos code y name no sean nulos o vacíos
@pytest.mark.functional
@pytest.mark.negative
def test_TC180_verificar_campos_no_vacios(setup_teardown_view_customer_group):
    headers, group1_data, group2_data = setup_teardown_view_customer_group
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, headers)
    log_request_response(endpoint, response, headers=headers)
    AssertionStatusCode.assert_status_code_200(response)
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    AssertionCustomerGroupFields.assert_customer_groups_field_length_limits(data)


# Admin > Customer - Group > Validar paginación básica con page y itemsPerPage
@pytest.mark.functional
def test_TC181_validar_paginacion_basica(auth_headers):
    page, items_per_page = 1, 2
    params = {"page": page, "itemsPerPage": items_per_page}
    endpoint = EndpointCustomerGroup.customer_group_with_params(**params)
    response = SyliusRequest.get(endpoint, auth_headers)
    log_request_response(endpoint, response, headers=auth_headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionCustomerGroupFields.assert_customer_group_pagination(response_json, params)
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(response_json)


# Admin > Customer - Group > TC_190 Verificar que no permita obtener grupo con código inexistente
@pytest.mark.negative
@pytest.mark.functional
def test_TC190_obtener_grupo_codigo_inexistente(setup_teardown_view_customer_group):
    headers, _, _ = setup_teardown_view_customer_group
    codigo_inexistente = "grupo_que_no_existe_12345"
    endpoint = EndpointCustomerGroup.code(codigo_inexistente)
    response = SyliusRequest.get(endpoint, headers)
    log_request_response(endpoint, response, headers=headers)
    AssertionStatusCode.assert_status_code_404(response)
    response_json = response.json()
    AssertionCustomerGroupFields.assert_customer_group_not_found_error(response_json)


# Admin > Customer - Group > TC_192 Verificar respuesta con parámetros itemsPerPage malformados
@pytest.mark.negative
@pytest.mark.xfail(reason="Known issue BugId: CG-02 No controla los parámetros itemsPerPage malformados", run=True)
@pytest.mark.functional
def test_TC192_verificar_parametros_itemsPerPage_malformados(setup_teardown_view_customer_group):
    headers, _, _ = setup_teardown_view_customer_group
    malformed_param = "xyz"
    endpoint = EndpointCustomerGroup.customer_group() + f"?page=1&itemsPerPage={malformed_param}"
    response = SyliusRequest.get(endpoint, headers)
    log_request_response(endpoint, response, headers=headers)
    AssertionStatusCode.assert_status_code_400(response)


# Admin > Customer - Group > TC_198 Verificar headers de respuesta HTTP
@pytest.mark.functional
@pytest.mark.positive
def test_TC198_verificar_headers_respuesta(setup_teardown_view_customer_group):
    headers, group1_data, group2_data = setup_teardown_view_customer_group
    endpoint = EndpointCustomerGroup.customer_group()
    response = SyliusRequest.get(endpoint, headers)
    log_request_response(endpoint, response, headers=headers)
    AssertionStatusCode.assert_status_code_200(response)
    data = response.json()
    AssertionCustomerGroupFields.assert_customer_group_root_metadata(data)
    AssertionCustomerGroupPerformance.assert_content_type_header(response.headers)
    AssertionCustomerGroupFields.assert_customer_group_list_content(data, expected_codes=[group1_data["code"], group2_data["code"]])
