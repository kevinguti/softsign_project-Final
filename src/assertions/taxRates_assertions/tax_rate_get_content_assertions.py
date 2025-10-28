import pytest


class AssertionTaxRateGetContent:
    """
    Validaciones de contenido específicas para respuestas GET de Tax Rates
    (Complementa los JSON Schemas existentes)
    """

    @staticmethod
    def assert_tax_rate_basic_fields(tax_rate_data: dict) -> None:
        """Valida los campos básicos de un tax rate"""
        required_fields = [
            "@id", "@type", "id", "code", "name", "amount",
            "includedInPrice", "calculator", "zone", "category"
        ]

        for field in required_fields:
            assert field in tax_rate_data, f"Campo requerido '{field}' no encontrado"

    @staticmethod
    def assert_tax_rate_data_types(tax_rate_data: dict) -> None:
        """Valida los tipos de datos de los campos del tax rate"""
        assert isinstance(tax_rate_data["id"], int), "id debe ser integer"
        assert isinstance(tax_rate_data["code"], str), "code debe ser string"
        assert isinstance(tax_rate_data["name"], str), "name debe ser string"
        assert isinstance(tax_rate_data["amount"], (int, float)), "amount debe ser número"
        assert isinstance(tax_rate_data["includedInPrice"], bool), "includedInPrice debe ser boolean"
        assert isinstance(tax_rate_data["calculator"], str), "calculator debe ser string"

        # Campos que deben ser IRIs (URLs)
        assert tax_rate_data["zone"].startswith("/api/v2/admin/zones/"), "zone debe ser IRI válido"
        assert tax_rate_data["category"].startswith("/api/v2/admin/tax-categories/"), "category debe ser IRI válido"

    @staticmethod
    def assert_tax_rate_values(tax_rate_data: dict, expected_data: dict = None) -> None:
        """Valida los valores específicos del tax rate"""
        # Validaciones de formato
        assert len(tax_rate_data["code"]) > 0, "code no puede estar vacío"
        assert len(tax_rate_data["name"]) >= 2, "name debe tener al menos 2 caracteres"
        assert 0 <= tax_rate_data["amount"] <= 1, "amount debe estar entre 0 y 1"

        # Si se proporcionan datos esperados, validar coincidencia
        if expected_data:
            assert tax_rate_data["code"] == expected_data.get("code"), "code no coincide"
            assert tax_rate_data["name"] == expected_data.get("name"), "name no coincide"
            assert tax_rate_data["amount"] == expected_data.get("amount"), "amount no coincide"
            assert tax_rate_data["includedInPrice"] == expected_data.get(
                "includedInPrice"), "includedInPrice no coincide"

    @staticmethod
    def assert_tax_rate_complete_response(tax_rate_data: dict, expected_data: dict = None) -> None:
        """Valida completa y exhaustivamente un tax rate"""
        AssertionTaxRateGetContent.assert_tax_rate_basic_fields(tax_rate_data)
        AssertionTaxRateGetContent.assert_tax_rate_data_types(tax_rate_data)
        AssertionTaxRateGetContent.assert_tax_rate_values(tax_rate_data, expected_data)

    @staticmethod
    def assert_tax_rate_list_structure(list_data: dict) -> None:
        """Valida la estructura de una lista de tax rates"""
        # Campos requeridos de la estructura Hydra
        assert "@context" in list_data, "Falta @context"
        assert "@type" in list_data, "Falta @type"
        assert "hydra:totalItems" in list_data, "Falta hydra:totalItems"
        assert "hydra:member" in list_data, "Falta hydra:member"

        # Validar tipos
        assert isinstance(list_data["hydra:totalItems"], int), "hydra:totalItems debe ser integer"
        assert isinstance(list_data["hydra:member"], list), "hydra:member debe ser lista"

    @staticmethod
    def assert_tax_rate_list_content(list_data: dict, expected_count: int = None, expected_codes: list = None) -> None:
        """Valida el contenido de una lista de tax rates"""
        AssertionTaxRateGetContent.assert_tax_rate_list_structure(list_data)

        members = list_data["hydra:member"]

        # Validar count si se especifica
        if expected_count is not None:
            assert len(members) == expected_count, f"Expected {expected_count} items, got {len(members)}"

        # Validar cada tax rate en la lista
        for tax_rate in members:
            AssertionTaxRateGetContent.assert_tax_rate_basic_fields(tax_rate)
            AssertionTaxRateGetContent.assert_tax_rate_data_types(tax_rate)

        # Verificar tax rates específicos si se proporcionan
        if expected_codes:
            actual_codes = [tax_rate["code"] for tax_rate in members]
            for expected_code in expected_codes:
                assert expected_code in actual_codes, f"Tax rate con código '{expected_code}' no encontrado en la lista"

    @staticmethod
    def assert_tax_rate_pagination(list_data: dict, page: int = None, items_per_page: int = None) -> None:
        """Valida la paginación de la lista de tax rates"""
        if "hydra:view" in list_data:
            view_data = list_data["hydra:view"]
            if "hydra:first" in view_data:
                assert "/api/v2/admin/tax-rates?page=1" in view_data["hydra:first"], "Enlace first incorrecto"
            if "hydra:last" in view_data:
                assert "/api/v2/admin/tax-rates?" in view_data["hydra:last"], "Enlace last incorrecto"

    @staticmethod
    @staticmethod
    def assert_tax_rate_not_found_error(error_data: dict) -> None:
        """Valida el error cuando no se encuentra un tax rate"""
        # Verificar status code
        assert error_data["status"] == 404, f"Expected status 404, got {error_data['status']}"

        # Verificar estructura básica del error
        assert "@context" in error_data, "Falta @context en respuesta de error"
        assert "@type" in error_data, "Falta @type en respuesta de error"
        assert "detail" in error_data or "hydra:description" in error_data, "Falta mensaje de error"

        # Verificar que el mensaje indica "not found"
        error_text = f"{error_data.get('detail', '')} {error_data.get('hydra:description', '')}".lower()

        # Términos que podrían aparecer en el mensaje de error
        not_found_terms = ["not found", "not exist", "no found", "could not find", "does not exist"]
        assert any(term in error_text for term in not_found_terms), \
            f"Expected 'not found' message, got: {error_text}"

    @staticmethod
    def assert_tax_rate_matches_expected(tax_rate_data: dict, expected_data: dict) -> None:
        """Valida que los datos del tax rate coincidan con los esperados"""
        assert tax_rate_data["code"] == expected_data["code"], "El código no coincide"
        assert tax_rate_data["name"] == expected_data["name"], "El nombre no coincide"
        assert tax_rate_data["amount"] == expected_data["amount"], "El amount no coincide"
        assert tax_rate_data["includedInPrice"] == expected_data["includedInPrice"], "El includedInPrice no coincide"
        assert tax_rate_data["calculator"] == expected_data["calculator"], "El calculator no coincide"

    @staticmethod
    def assert_tax_rate_complete_response_with_validation(tax_rate_data: dict, expected_data: dict = None) -> None:
        """Valida completa y exhaustivamente un tax rate incluyendo comparación con datos esperados"""
        # Validar estructura y tipos
        AssertionTaxRateGetContent.assert_tax_rate_complete_response(tax_rate_data)

        # Si se proporcionan datos esperados, validar coincidencia
        if expected_data:
            AssertionTaxRateGetContent.assert_tax_rate_matches_expected(tax_rate_data, expected_data)

    @staticmethod
    def assert_jsonld_content_type(response) -> None:
        """Valida que el Content-Type sea application/ld+json"""
        content_type = response.headers.get("Content-Type", "")
        assert "application/ld+json" in content_type, (
            f"Content-Type debe ser 'application/ld+json'. Actual: {content_type}\n"
            f"Respuesta completa: {response.text}"
        )

    @staticmethod
    def assert_valid_json_response(response) -> None:
        """Valida que la respuesta sea JSON válido"""
        try:
            response.json()
        except ValueError as e:
            pytest.fail(f"La respuesta no es JSON válido: {str(e)}")

    @staticmethod
    def assert_authentication_error(error_data: dict) -> None:
        """Valida error de autenticación (401)"""
        # Verificar status code
        assert error_data["status"] == 401, f"Expected status 401, got {error_data['status']}"

        # Verificar estructura básica del error
        assert "@context" in error_data, "Falta @context en respuesta de error"
        assert "@type" in error_data, "Falta @type en respuesta de error"
        assert "detail" in error_data or "hydra:description" in error_data, "Falta mensaje de error"

        # Verificar que contiene mensaje de error de autenticación
        error_text = f"{error_data.get('detail', '')} {error_data.get('hydra:description', '')}".lower()

        # Términos que podrían aparecer en el mensaje de error de autenticación
        auth_terms = [
            "unauthorized",
            "authentication",
            "token",
            "jwt",
            "bearer",
            "access",
            "login",
            "credentials",
            "authorization"
        ]

        assert any(term in error_text for term in auth_terms), \
            f"Expected authentication error message, got: {error_text}"

