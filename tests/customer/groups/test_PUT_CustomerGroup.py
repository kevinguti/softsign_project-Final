import pytest
import time

from src.assertions.customergroup_assertions.customer_group_errors_assertions import AssertionCustomerGroupErrors
from src.assertions.customergroup_assertions.customer_group_post_content_assertions import AssertionCustomerGroupCreate
from src.assertions.customergroup_assertions.customer_group_schema_assertions import AssertionCustomerGroup
from src.assertions.customergroup_assertions.customer_group_performance_assertions import AssertionCustomerGroupPerformance
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest
from src.data.customer_group import generate_customer_group_source_data
from utils.logger_helpers import log_request_response

# Admin > Customer - Group > TC_271 Actualizar grupo de clientes con datos válidos
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC271_actualizar_grupo_clientes_datos_validos(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    update_data = {
        "name": "Updated Customer Group Name"
    }
    
    AssertionCustomerGroup.assert_customer_group_edit_input_schema(update_data)
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, update_data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=update_data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    AssertionCustomerGroupCreate.assert_customer_group_response(
        {"name": "Updated Customer Group Name", "code": customer_group_code}, 
        response.json()
    )


# Admin > Customer - Group > TC_272 Verificar estructura del JSON devuelto al actualizar
@pytest.mark.functional
@pytest.mark.smoke
@pytest.mark.high
def test_TC272_verificar_estructura_json_respuesta_actualizacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    update_data = {
        "name": "Updated Customer Group Name"
    }
    
    AssertionCustomerGroup.assert_customer_group_edit_input_schema(update_data)
    
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, update_data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=update_data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())



# Admin > Customer - Group > TC_274 Actualizar grupo sin campo obligatorio 'name'
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.xfail(reason="Known issue BugId: CG-03 Permite actualizar el campo name vacio cuando es obligatorio", run=True)
@pytest.mark.high
def test_TC274_actualizar_grupo_sin_campo_name(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {}  
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_281 Verificar que no permita actualizar grupo con nombre vacío
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.high
def test_TC281_actualizar_grupo_nombre_vacio(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": ""
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_282 Verificar que no permita nombre muy largo
@pytest.mark.negative
@pytest.mark.boundary
@pytest.mark.high
def test_TC282_actualizar_grupo_nombre_muy_largo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "a" * 256
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_422(response)


# Admin > Customer - Group > TC_283 Verificar que permita actualizar grupo con caracteres especiales en nombre
@pytest.mark.functional
@pytest.mark.boundary
@pytest.mark.medium
def test_TC283_actualizar_grupo_nombre_caracteres_especiales(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Test Pablo ñáéíóú-Co_123$@$@#"
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())


# Admin > Customer - Group > TC_290 Verificar headers de respuesta
@pytest.mark.functional
@pytest.mark.low
def test_TC290_verificar_headers_respuesta_actualizacion(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Nombre Actualizado Headers"
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())
    
    performance_assertions = AssertionCustomerGroupPerformance()
    performance_assertions.assert_update_content_type_header(response)


# Admin > Customer - Group > TC_291 Verificar que permita actualizar grupo con nombre mínimo
@pytest.mark.boundary
@pytest.mark.low
def test_TC291_actualizar_grupo_nombre_minimo(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "name": "Ak"
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_200(response)
    AssertionCustomerGroup.assert_customer_group_edit_output_schema(response.json())


# Admin > Customer - Group > TC_292 Verificar que no permita actualizar grupo con valores null
@pytest.mark.negative
@pytest.mark.medium
def test_TC292_actualizar_grupo_valores_null(setup_customer_group_cleanup):
    auth_headers, add_group_for_cleanup = setup_customer_group_cleanup
    
    initial_data = generate_customer_group_source_data()
    create_endpoint = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_endpoint, auth_headers, initial_data)
    AssertionStatusCode.assert_status_code_201(create_response)
    
    customer_group_code = create_response.json()["code"]
    add_group_for_cleanup(customer_group_code)
    
    data = {
        "code": None,
        "name": None
    }
    endpoint = EndpointCustomerGroup.code(customer_group_code)
    response = SyliusRequest.put(endpoint, auth_headers, data)
    
    log_request_response(endpoint, response, headers=auth_headers, payload=data)
    
    AssertionStatusCode.assert_status_code_400(response)
