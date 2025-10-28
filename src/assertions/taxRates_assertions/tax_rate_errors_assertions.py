import re

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

    @staticmethod
    def assert_tax_rate_name_not_blank_error(response_json: dict) -> None:
        """Valida el error de nombre vacío en tax rate"""
        assert response_json["status"] == 422, f"Expected status 422, got {response_json['status']}"

        if "violations" in response_json:
            # Buscar la violación relacionada con el nombre
            name_violations = [
                violation for violation in response_json["violations"]
                if violation.get("propertyPath") == "name"
            ]

            assert len(name_violations) > 0, "No violation found for 'name' property"

            # Verificar que el mensaje indica que el nombre no puede estar vacío
            violation_messages = [violation.get("message", "").lower() for violation in name_violations]

            # Buscar en todos los mensajes de violación del campo 'name'
            assert any(
                any(term in message for term in ["please enter", "blank", "empty", "required", "at least"])
                for message in violation_messages
            ), f"Expected name validation message, got: {violation_messages}"

        else:
            # Para respuestas sin array de violations
            error_text = response_json.get("detail", "").lower()
            assert any(term in error_text for term in ["please enter", "name", "blank", "empty"]), \
                f"Expected name validation error in detail, got: {error_text}"

    @staticmethod
    def assert_tax_rate_not_found_error(response_json: dict) -> None:
        """Valida el error de tax rate no encontrado"""
        assert response_json["status"] == 404, f"Expected status 404, got {response_json['status']}"

        # Verificar que contiene mensajes indicando que no se encontró el recurso
        error_text = f"{response_json.get('detail', '')} {response_json.get('hydra:description', '')}".lower()

        assert any(term in error_text for term in [
            "not found",
            "not exist",
            "no found",
            "could not find",
            "does not exist"
        ]), f"Expected 'not found' message, got: {error_text}"

        # Verificar estructura hydra para errores 404
        assert "hydra:title" in response_json, "Missing hydra:title in 404 response"
        assert "hydra:description" in response_json, "Missing hydra:description in 404 response"

    @staticmethod
    def assert_tax_rate_amount_non_negative_error(response_json):
        """
        Verifica que la respuesta contenga un error relacionado con
        que 'amount' no puede ser negativo (o debe ser >= 0).
        """
        # Extraer posibles violaciones/errores en formatos comunes
        violations = []
        if isinstance(response_json, dict):
            violations = response_json.get("violations") or response_json.get("errors") or []
        if not isinstance(violations, list):
            violations = [violations]

        # Normalizar mensajes
        messages = []
        for v in violations:
            if isinstance(v, dict):
                field = (v.get("propertyPath") or v.get("field") or "").lower()
                msg = (v.get("message") or v.get("detail") or v.get("title") or "").strip()
                messages.append((field, msg))
            elif isinstance(v, str):
                messages.append(("", v))

        # Patrón que cubre "no negativo", ">= 0", "greater than or equal to 0", etc.
        pattern = re.compile(
            r"(non[- ]?negative|>=\s*0|greater than or equal to|no puede ser negativo|no negativo|must be greater than or equal to 0)",
            re.I)

        found = False
        for field, msg in messages:
            if "amount" in field or pattern.search(msg):
                found = True
                break

        assert found, f"No se encontró error de 'amount non-negative' en la respuesta: {response_json}"

    @staticmethod
    def assert_tax_rate_includedInPrice_boolean_error(response_json: dict) -> None:
        """Valida el error de includedInPrice con valor no booleano"""
        # Primero debuggear para ver qué está devolviendo la API
        print(f"Status Code in response: {response_json.get('status')}")
        print(f"Response violations: {response_json.get('violations', [])}")
        print(f"Response detail: {response_json.get('detail', '')}")

        # Aceptar tanto 400 como 422
        assert response_json["status"] in [400, 422], f"Expected status 400 or 422, got {response_json['status']}"

        if "violations" in response_json:
            # Buscar violaciones del campo 'includedInPrice'
            included_in_price_violations = [
                violation for violation in response_json["violations"]
                if violation.get("propertyPath") == "includedInPrice"
            ]

            assert len(included_in_price_violations) > 0, "No validation error found for 'includedInPrice' field"

            # Verificar que el mensaje indica el problema de tipo
            violation_messages = [violation.get("message", "").lower() for violation in included_in_price_violations]

            # Términos que podrían aparecer en el mensaje de error
            expected_terms = ["boolean", "true", "false", "type", "bool", "this value", "expected"]
            assert any(
                any(term in message for term in expected_terms)
                for message in violation_messages
            ), f"Expected type validation message, got: {violation_messages}"
        else:
            # Para respuestas sin array de violations
            error_text = response_json.get("detail", "").lower()
            assert any(term in error_text for term in ["includedinprice", "boolean", "type"]), \
                f"Expected includedInPrice validation error, got: {error_text}"

    @staticmethod
    def assert_tax_rate_code_not_blank_error(response_json: dict) -> None:
        """Valida el error de código vacío en tax rate"""
        violations = response_json.get("violations", [])

        found = any(
            (v.get("propertyPath") == "code" and
             any(term in (v.get("message", "").lower())
                 for term in ["blank", "not be blank", "no puede", "vacío"]))
            for v in violations
        )

        # Fallback al detail general
        if not found and "detail" in response_json:
            detail = response_json["detail"].lower()
            found = "code" in detail and any(term in detail for term in ["blank", "not be blank"])

        assert found, f"No se encontró el error 'code not blank'. Violations: {violations}"

    @staticmethod
    def assert_tax_rate_name_too_long_error(response_json: dict) -> None:
        """Valida el error de nombre demasiado largo"""
        assert response_json["status"] == 422, f"Expected status 422, got {response_json['status']}"
        assert "violations" in response_json, "Missing violations in response"

        # Buscar violaciones del campo 'name'
        name_violations = [
            violation for violation in response_json["violations"]
            if violation.get("propertyPath") == "name"
        ]

        assert len(name_violations) > 0, "No validation error found for 'name' field"

        # Verificar que el mensaje indica problema de longitud
        violation_messages = [violation.get("message", "").lower() for violation in name_violations]

        expected_terms = ["long", "length", "max", "255", "limit", "size"]
        assert any(
            any(term in message for term in expected_terms)
            for message in violation_messages
        ), f"Expected length validation message, got: {violation_messages}"

    @staticmethod
    def assert_tax_rate_invalid_characters_error(response_json: dict, field_name: str) -> None:
        """Valida error de caracteres inválidos en un campo específico"""
        assert response_json["status"] == 422, f"Expected status 422, got {response_json['status']}"
        assert "violations" in response_json, "Missing violations in response"

        # Buscar violaciones del campo específico
        field_violations = [
            violation for violation in response_json["violations"]
            if violation.get("propertyPath") == field_name
        ]

        assert len(field_violations) > 0, f"No validation error found for '{field_name}' field"

        # Verificar que el mensaje indica caracteres inválidos
        violation_messages = [violation.get("message", "").lower() for violation in field_violations]

        invalid_terms = ["invalid", "character", "format", "pattern", "symbol", "special"]
        assert any(
            any(term in message for term in invalid_terms)
            for message in violation_messages
        ), f"Expected invalid characters validation for {field_name}, got: {violation_messages}"

    @staticmethod
    def assert_tax_rate_validation_error(response_json: dict, field_name: str) -> None:
        """Valida cualquier error de validación para un campo específico"""
        assert response_json["status"] == 422, f"Expected status 422, got {response_json['status']}"
        assert "violations" in response_json, "Missing violations in response"

        # Buscar violaciones del campo específico
        field_violations = [
            violation for violation in response_json["violations"]
            if violation.get("propertyPath") == field_name
        ]

        assert len(field_violations) > 0, f"No validation error found for '{field_name}' field"

        # El test pasa si hay cualquier violación en el campo especificado
        print(f"Validation error found for {field_name}: {field_violations[0].get('message')}")

    @staticmethod
    def assert_tax_rate_amount_validation_error(response_json: dict) -> None:
        """Valida error de validación en el campo amount"""
        assert response_json["status"] == 422, f"Expected status 422, got {response_json['status']}"
        assert "violations" in response_json, "Missing violations in response"

        # Buscar violaciones del campo 'amount'
        amount_violations = [
            violation for violation in response_json["violations"]
            if violation.get("propertyPath") == "amount"
        ]

        assert len(amount_violations) > 0, "No validation error found for 'amount' field"

        # Verificar que el mensaje indica problema con amount
        violation_messages = [violation.get("message", "").lower() for violation in amount_violations]

        amount_terms = ["amount", "value", "range", "greater", "less", "negative", "positive"]
        assert any(
            any(term in message for term in amount_terms)
            for message in violation_messages
        ), f"Expected amount validation message, got: {violation_messages}"