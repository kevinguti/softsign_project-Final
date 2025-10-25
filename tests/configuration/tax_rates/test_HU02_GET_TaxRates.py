import pytest

from src.assertions.taxRates_assertions.taxRates_schema_assertions import AssertionTaxRate
from src.assertions.taxRates_assertions.tax_rate_get_content_assertions import AssertionTaxRateGetContent
from src.assertions.status_code_assertions import AssertionStatusCode
from src.routes.endpoint_tax_rates import EndpointTaxRate
from src.routes.request import SyliusRequest
from utils.logger_helpers import log_request_response
from src.resources.call_request.taxRates_call import TaxRateCall
from src.services.client import SyliusClient

# Admin > Configuration > Tax Rate > Obtener listado de Tax Rates
@pytest.mark.positive
@pytest.mark.functional
@pytest.mark.smoke
def test_TC202_obtener_listado_tax_rates_valido(setup_teardown_view_tax_rate):
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
def test_TC203_obtener_tax_rate_por_codigo_valido(setup_teardown_view_tax_rate):
    headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate
    url = EndpointTaxRate.by_code(tax_rate1_data["code"])
    response = SyliusRequest.get(url, headers)
    AssertionStatusCode.assert_status_code_200(response)
    response_json = response.json()
    AssertionTaxRate.assert_tax_rate_code_schema(response_json)
    AssertionTaxRateGetContent.assert_tax_rate_complete_response_with_validation(response_json, tax_rate1_data)
    log_request_response(url, response, headers)


    @pytest.mark.positive
    @pytest.mark.functional
    @pytest.mark.smoke
    def test_TC204_obtener_tax_rate_por_id_valido(setup_teardown_view_tax_rate):
        """Test smoke para obtener un tax rate por ID específico"""
        headers, tax_rate1_data, tax_rate2_data = setup_teardown_view_tax_rate

        # Obtener el segundo tax rate por ID
        url = EndpointTaxRate.by_id(tax_rate2_data["id"])
        response = SyliusRequest.get(url, headers)

        AssertionStatusCode.assert_status_code_200(response)
        response_json = response.json()

        # Validar schema de respuesta individual
        AssertionTaxRate.assert_tax_rate_id_schema(response_json)

        # Validar contenido específico
        AssertionTaxRateGetContent.assert_tax_rate_complete_response(
            response_json,
            tax_rate2_data  # Datos esperados del segundo tax rate
        )

        # Verificaciones smoke
        assert response_json["id"] == tax_rate2_data["id"], "El ID no coincide"
        assert response_json["code"] == tax_rate2_data["code"], "El código no coincide"

        log_request_response(url, response, headers)

    @pytest.mark.negative
    @pytest.mark.functional
    def test_TC205_obtener_tax_rate_por_codigo_inexistente(setup_teardown_view_tax_rate):
        """Test para intentar obtener un tax rate con código que no existe"""
        headers, _, _ = setup_teardown_view_tax_rate

        # Intentar obtener con código que no existe
        url = EndpointTaxRate.by_code("CODIGO_INEXISTENTE_12345")
        response = SyliusRequest.get(url, headers)

        AssertionStatusCode.assert_status_code_404(response)
        response_json = response.json()

        # Validar estructura de error
        AssertionTaxRateGetContent.assert_tax_rate_not_found_error(response_json)

        log_request_response(url, response, headers)