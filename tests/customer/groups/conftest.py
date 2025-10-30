import pytest

from src.data.customer_group import generate_customer_group_source_data
from src.resources.call_request.customer_group_call import CustomerGroupCall
from src.routes.endpoint_customer_group import EndpointCustomerGroup
from src.routes.request import SyliusRequest


@pytest.fixture(scope="module")
def setup_teardown_view_customer_group(auth_headers):
    """Fixture para tests que necesitan múltiples customer groups para operaciones de view/GET"""
    # Crear customer groups de prueba
    payload_group1 = generate_customer_group_source_data()
    payload_group2 = generate_customer_group_source_data()

    customer_group1_data = CustomerGroupCall().create(auth_headers, payload_group1)
    customer_group2_data = CustomerGroupCall().create(auth_headers, payload_group2)

    yield auth_headers, customer_group1_data, customer_group2_data

    # Cleanup - eliminar por código
    try:
        CustomerGroupCall().delete(auth_headers, customer_group1_data['code'])
        print(f"Customer group eliminado: {customer_group1_data['code']}")
    except Exception as e:
        print(f"Error al eliminar customer group {customer_group1_data['code']}: {e}")

    try:
        CustomerGroupCall().delete(auth_headers, customer_group2_data['code'])
        print(f"Customer group eliminado: {customer_group2_data['code']}")
    except Exception as e:
        print(f"Error al eliminar customer group {customer_group2_data['code']}: {e}")


@pytest.fixture(scope="class")
def setup_edit_customer_group(auth_headers):
    payload_group = generate_customer_group_source_data()
    customer_group_data = CustomerGroupCall().create(auth_headers, payload_group)

    assert "code" in customer_group_data, f"La respuesta de creación no contiene 'code': {customer_group_data}"

    yield auth_headers, customer_group_data

    CustomerGroupCall().delete(auth_headers, customer_group_data["code"])


@pytest.fixture(scope="function")
def setup_add_customer_group(auth_headers):
    created_customer_groups = []
    yield auth_headers, created_customer_groups
    for customer_group in created_customer_groups:
        try:
            if isinstance(customer_group, dict) and "code" in customer_group:
                customer_group_code = customer_group["code"]
            elif isinstance(customer_group, str):
                customer_group_code = customer_group
            elif hasattr(customer_group, "json") and isinstance(customer_group.json(), dict) and "code" in customer_group.json():
                customer_group_code = customer_group.json()["code"]
            else:
                print(f"[Cleanup] Formato desconocido: {customer_group}")
                continue
            from src.resources.call_request.customer_group_call import CustomerGroupCall
            delete_response = None
            try:
                delete_response = CustomerGroupCall.delete_by_code(auth_headers, customer_group_code)
            except Exception:
                try:
                    delete_response = CustomerGroupCall().delete(auth_headers, customer_group_code)
                except Exception:
                    delete_response = None
            if hasattr(delete_response, "status_code"):
                if delete_response.status_code != 204:
                    print(f"[Cleanup] Error al eliminar customer group {customer_group_code}: {delete_response.status_code} - {getattr(delete_response, 'text', '')}")
            else:
                print(f"[Cleanup] Resultado de eliminación no estándar para {customer_group_code}: {delete_response}")
        except Exception as e:
            print(f"[Cleanup] Excepción al eliminar customer group: {customer_group}. Error: {e}")

@pytest.fixture(scope="function")  
def setup_customer_group_cleanup(auth_headers):
    """
    Fixture alternativo para cleanup manual de customer groups.
    Útil cuando necesitas control específico sobre qué grupos eliminar.
    """
    groups_to_cleanup = []
    
    def add_group_for_cleanup(group_code):
        """Agregar un código de grupo para limpieza posterior"""
        groups_to_cleanup.append(group_code)
    
    # Retornar headers y función helper
    yield auth_headers, add_group_for_cleanup
    
    # Teardown: limpiar grupos marcados para eliminación
    for group_code in groups_to_cleanup:
        try:
            CustomerGroupCall().delete(auth_headers, group_code)
            print(f" Customer group limpiado: {group_code}")
        except Exception as e:
            print(f" Error durante cleanup de {group_code}: {e}")


@pytest.fixture
def setup_delete_customer_group(auth_headers):
    """Fixture que crea un customer group específicamente para tests de DELETE"""
    # Crear un customer group para eliminar
    payload = generate_customer_group_source_data()
    create_url = EndpointCustomerGroup.customer_group()
    create_response = SyliusRequest.post(create_url, auth_headers, payload)

    if create_response.status_code != 201:
        pytest.fail(f"No se pudo crear customer group para DELETE: {create_response.text}")

    customer_group_data = create_response.json()
    customer_group_code = customer_group_data["code"]

    yield auth_headers, customer_group_data

    # Cleanup: por si el test no eliminó el customer group
    try:
        delete_url = EndpointCustomerGroup.code(customer_group_code)
        SyliusRequest.delete(delete_url, auth_headers)
        print(f"Cleanup: Customer group eliminado: {customer_group_code}")
    except Exception as e:
        print(f"Cleanup: Customer group ya fue eliminado o error: {e}")


@pytest.fixture
def setup_multiple_customer_groups(auth_headers):
    created_codes = []
    created_data = []

    try:
        for i in range(5):
            payload = generate_customer_group_source_data()
            create_url = EndpointCustomerGroup.customer_group()
            create_response = SyliusRequest.post(create_url, auth_headers, payload)

            if create_response.status_code != 201:
                # Si falla una creación, hacemos fail para no continuar tests dependientes de estos grupos
                pytest.fail(f"No se pudo crear customer group #{i} para DELETE: {create_response.text}")

            data = create_response.json()
            created_codes.append(data["code"])
            created_data.append(data)

        yield auth_headers, created_codes

    finally:
        # Cleanup: intentamos eliminar cualquiera que quede
        for code in created_codes:
            try:
                delete_url = EndpointCustomerGroup.code(code)
                resp = SyliusRequest.delete(delete_url, auth_headers)
                # Opcional: loguear sólo si la entidad existía o para debug
                print(f"Cleanup multiple: intento eliminar {code}, status={resp.status_code}")
            except Exception as e:
                print(f"Cleanup multiple: error intentando eliminar {code}: {e}")