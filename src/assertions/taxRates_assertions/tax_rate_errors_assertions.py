class AssertionTaxRateErrors:

    @staticmethod
    def assert_tax_rate_error_response(response_json, expected_error_field=None):
        """Valida la estructura de respuesta de error para tax rates"""
        assert "@context" in response_json, "La respuesta de error debe contener '@context'"
        assert "@type" in response_json, "La respuesta de error debe contener '@type'"
        assert "hydra:title" in response_json, "La respuesta de error debe contener 'hydra:title'"
        assert "hydra:description" in response_json, "La respuesta de error debe contener 'hydra:description'"

        if expected_error_field:
            violations = response_json.get("violations")
            if violations:
                assert any(
                    v.get("propertyPath") == expected_error_field for v in violations
                ), f"Debe haber una violación para el campo: {expected_error_field}"
            else:
                # Fallback: aceptar mensajes en 'detail' cuando no hay 'violations'
                assert "detail" in response_json, "La respuesta de error debe contener 'violations' o 'detail'"
                detail = str(response_json.get("detail", "")).lower()
                # Comprueba que el detalle mencione el campo o un indicio de error de tipo/valor
                hints = [expected_error_field.lower(), "numeric", "number", "invalid", "required", "not found", "blank"]
                assert any(
                    h in detail for h in hints), f"El 'detail' no indica problema con {expected_error_field}: {detail}"

    @staticmethod
    def assert_tax_rate_error_schema(response_json):
        """Valida el schema básico de error"""
        AssertionTaxRateErrors.assert_tax_rate_error_response(response_json)

    @staticmethod
    def assert_duplicate_code_error(response_json):
        """Valida específicamente error de código duplicado"""
        AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, "code")
        # Validación adicional para mensaje de duplicado
        violations = response_json.get("violations", [])
        code_violations = [v for v in violations if v["propertyPath"] == "code"]
        assert len(code_violations) > 0, "Debe haber una violación para el campo 'code'"

        # Opcional: validar que el mensaje contenga indicios de duplicación
        violation_message = code_violations[0].get("message", "").lower()
        assert any(word in violation_message for word in ["already", "exist", "duplicate", "unique"]), \
            f"El mensaje de error debería indicar duplicación: {violation_message}"

    @staticmethod
    def assert_required_field_error(response_json, field_name):
        """Valida error de campo requerido"""
        AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, field_name)
        violations = response_json.get("violations", [])
        field_violations = [v for v in violations if v["propertyPath"] == field_name]

        if field_violations:
            violation_message = field_violations[0].get("message", "").lower()
            valid_keywords = [
                "blank", "required", "not be blank", "not null",
                "please enter", "must be", "cannot be", "this value"
            ]
            assert any(word in violation_message for word in valid_keywords), \
                f"El mensaje de error debería indicar campo requerido: {violation_message}"

    @staticmethod
    def assert_invalid_amount_error(response_json):
        """Valida error de amount inválido"""
        AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, "amount")
        violations = response_json.get("violations", [])
        amount_violations = [v for v in violations if v["propertyPath"] == "amount"]

        if amount_violations:
            violation_message = amount_violations[0].get("message", "").lower()
            # Mensaje más flexible que acepte "The tax rate amount is invalid"
            valid_messages = ["number", "numeric", "type", "format", "greater", "less", "invalid"]
            assert any(word in violation_message for word in valid_messages), \
                f"El mensaje de error debería indicar problema con el amount: {violation_message}"

    @staticmethod
    def assert_invalid_boolean_error(response_json):
        """Valida error de booleano inválido"""
        AssertionTaxRateErrors.assert_tax_rate_error_response(response_json, "includedInPrice")
        violations = response_json.get("violations", [])
        boolean_violations = [v for v in violations if v["propertyPath"] == "includedInPrice"]

        if boolean_violations:
            violation_message = boolean_violations[0].get("message", "").lower()
            assert any(word in violation_message for word in ["boolean", "true", "false", "type"]), \
                f"El mensaje de error debería indicar problema con el booleano: {violation_message}"

    @staticmethod
    def assert_zone_not_found_error(response_json):
        """Valida error de zona no encontrada (para errores 400)"""
        # Para errores 400 de "Item not found" - estructura diferente
        assert "@context" in response_json, "La respuesta de error debe contener '@context'"
        assert "@type" in response_json, "La respuesta de error debe contener '@type'"

        # Sylius puede usar diferentes estructuras para errores 400 vs 422
        if "detail" in response_json:
            detail = response_json.get("detail", "").lower()
            assert any(word in detail for word in ["not found", "item not found", "zone", "resource"]), \
                f"El mensaje de error debería indicar que la zona no existe: {detail}"
        elif "hydra:description" in response_json:
            description = response_json.get("hydra:description", "").lower()
            assert any(word in description for word in ["not found", "item not found", "zone", "resource"]), \
                f"El mensaje de error debería indicar que la zona no existe: {description}"

    @staticmethod
    def assert_invalid_date_range_error(response_json):
        """Valida error de rango de fechas inválido"""
        AssertionTaxRateErrors.assert_tax_rate_error_response(response_json)
        # Podría ser en startDate o endDate
        violations = response_json.get("violations", [])
        date_violations = [v for v in violations if "date" in v["propertyPath"].lower()]

        if date_violations:
            violation_message = date_violations[0].get("message", "").lower()
            assert any(word in violation_message for word in ["date", "before", "after", "range", "invalid"]), \
                f"El mensaje de error debería indicar problema con las fechas: {violation_message}"

    @staticmethod
    def assert_category_not_found_error(response_json):
        """Valida error de categoría de tax no encontrada (para errores 400)"""
        assert "@context" in response_json, "La respuesta de error debe contener '@context'"
        assert "@type" in response_json, "La respuesta de error debe contener '@type'"

        if "detail" in response_json:
            detail = response_json.get("detail", "").lower()
            assert any(
                word in detail for word in ["not found", "item not found", "category", "tax category", "resource"]), \
                f"El mensaje de error debería indicar que la categoría no existe: {detail}"
        elif "hydra:description" in response_json:
            description = response_json.get("hydra:description", "").lower()
            assert any(word in description for word in
                       ["not found", "item not found", "category", "tax category", "resource"]), \
                f"El mensaje de error debería indicar que la categoría no existe: {description}"