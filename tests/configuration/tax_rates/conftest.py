import pytest

from src.routes.endpoint_tax_rates import EndpointTaxRate
from src.resources.call_request.taxRates_call import TaxRateCall
from src.resources.payloads.payload_taxRates import PayloadTaxRate
from src.data.taxRates import generate_tax_rate_data
from src.routes.request import SyliusRequest


@pytest.fixture(scope="module")
def setup_teardown_view_tax_rate(auth_headers):
    """Fixture para tests que necesitan múltiples tax rates"""
    payload_tax1 = PayloadTaxRate.build_payload_tax_rate(generate_tax_rate_data())
    payload_tax2 = PayloadTaxRate.build_payload_tax_rate(generate_tax_rate_data())

    response1 = TaxRateCall.create(auth_headers, payload_tax1)
    response2 = TaxRateCall.create(auth_headers, payload_tax2)
    tax_rate1_data = response1.json()
    tax_rate2_data = response2.json()

    yield auth_headers, tax_rate1_data, tax_rate2_data

    # Cleanup - eliminar por ID
    TaxRateCall.delete_by_id(auth_headers, tax_rate1_data['id'])
    TaxRateCall.delete_by_id(auth_headers, tax_rate2_data['id'])


@pytest.fixture(scope="function")
def setup_add_tax_rate(auth_headers):
    """Fixture para tests de creación que maneja cleanup automático"""
    created_tax_rates = []
    yield auth_headers, created_tax_rates

    for tax_rate in created_tax_rates:
        try:
            if isinstance(tax_rate, dict) and "code" in tax_rate:
                tax_rate_code = tax_rate["code"]
            elif isinstance(tax_rate, str):
                tax_rate_code = tax_rate
            elif hasattr(tax_rate, "json") and isinstance(tax_rate.json(), dict) and "code" in tax_rate.json():
                tax_rate_code = tax_rate.json()["code"]
            else:
                print(f"[Cleanup] Formato desconocido: {tax_rate}")
                continue


            from src.resources.call_request.taxRates_call import TaxRateCall
            delete_response = TaxRateCall.delete_by_code(auth_headers, tax_rate_code)

            if delete_response.status_code != 204:
                print(
                    f"[Cleanup] Error al eliminar tax rate {tax_rate_code}: {delete_response.status_code} - {delete_response.text}")
        except Exception as e:
            print(f"[Cleanup] Excepción al eliminar tax rate: {tax_rate}. Error: {e}")


@pytest.fixture(scope="class")
def setup_edit_tax_rate(auth_headers):
    """Fixture para tests de edición"""
    payload_tax = PayloadTaxRate.build_payload_tax_rate(generate_tax_rate_data())
    response = TaxRateCall.create(auth_headers, payload_tax)
    tax_rate_data = response.json()

    # Verifica que tiene 'code'
    assert "code" in tax_rate_data, f"La respuesta de creación no contiene 'code': {tax_rate_data}"

    yield auth_headers, tax_rate_data

    # Cleanup por código (que es lo que usa la API)
    TaxRateCall.delete_by_code(auth_headers, tax_rate_data["code"])



@pytest.fixture(scope="function")
def setup_create_tax_rate(auth_headers):
    payload_tax = PayloadTaxRate.build_payload_tax_rate(generate_tax_rate_data())
    response = TaxRateCall.create(auth_headers, payload_tax)
    tax_rate_data = response.json()
    yield auth_headers, tax_rate_data


@pytest.fixture(scope='module')
def setup_e2e_tax_rate(auth_headers):
    """Fixture para tests end-to-end"""
    created_tax_rates = []

    yield auth_headers, created_tax_rates

    # Cleanup
    for tax_rate in created_tax_rates:
        if 'id' in tax_rate:
            try:
                TaxRateCall.delete_by_id(auth_headers, tax_rate['id'])
            except Exception as e:
                print(f"[Cleanup] Error al eliminar tax rate {tax_rate.get('id')}: {e}")


@pytest.fixture(scope="function")
def setup_tax_rate_with_dependencies(auth_headers):
    """Fixture que crea tax rate con sus dependencias (zona y categoría)"""
    # Obtener zonas disponibles
    from src.resources.call_request.zone_call import ZoneCall
    zones_response = ZoneCall.view_all(auth_headers)
    available_zones = zones_response.json()['hydra:member']

    # Obtener categorías disponibles
    from src.resources.call_request.taxCategory_call import TaxCategoryCall
    categories_response = TaxCategoryCall.view_all(auth_headers)
    available_categories = categories_response.json()['hydra:member']

    # Generar datos con dependencias reales
    tax_rate_data = generate_tax_rate_data(
        available_zones=available_zones,
        available_categories=available_categories
    )
    payload = PayloadTaxRate.build_payload_tax_rate(tax_rate_data)

    # Crear tax rate
    response = TaxRateCall.create(auth_headers, payload)
    tax_rate_data = response.json()

    yield auth_headers, tax_rate_data

    # Cleanup
    TaxRateCall.delete_by_id(auth_headers, tax_rate_data["id"])