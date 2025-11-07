class AssertionTaxRateCreate:

    @staticmethod
    def assert_tax_rate_payload(payload):
        """Valida que el payload de creación tenga los campos requeridos"""
        assert "code" in payload, "El payload debe contener 'code'"
        assert "name" in payload, "El payload debe contener 'name'"
        assert "amount" in payload, "El payload debe contener 'amount'"
        assert "includedInPrice" in payload, "El payload debe contener 'includedInPrice'"
        assert "calculator" in payload, "El payload debe contener 'calculator'"
        assert "zone" in payload, "El payload debe contener 'zone'"
        assert "category" in payload, "El payload debe contener 'category'"

        # Validaciones específicas de formato
        assert isinstance(payload["amount"], (int, float)), "El amount debe ser numérico"
        assert 0 <= payload["amount"] <= 1, "El amount debe estar entre 0 y 1"
        assert isinstance(payload["includedInPrice"], bool), "El includedInPrice debe ser booleano"
        assert payload["calculator"] == "default", "El calculator debe ser 'default'"

        if "startDate" in payload:
            assert isinstance(payload["startDate"], str), "El startDate debe ser string"
        if "endDate" in payload:
            assert isinstance(payload["endDate"], str), "El endDate debe ser string"

    @staticmethod
    def assert_tax_rate_response(payload, response_json):
        """Valida que la respuesta coincida con el payload enviado"""
        assert response_json["code"] == payload["code"], "El code en la respuesta no coincide"
        assert response_json["name"] == payload["name"], "El name en la respuesta no coincide"
        assert float(response_json["amount"]) == float(payload["amount"]), "El amount en la respuesta no coincide"
        assert response_json["includedInPrice"] == payload[
            "includedInPrice"], "El includedInPrice en la respuesta no coincide"
        assert response_json["calculator"] == payload["calculator"], "El calculator en la respuesta no coincide"

        # Validaciones de fechas en la respuesta
        if "startDate" in payload:
            assert "startDate" in response_json, "La respuesta debe incluir startDate"
            # Puedes agregar más validaciones de formato de fecha si quieres
        if "endDate" in payload:
            assert "endDate" in response_json, "La respuesta debe incluir endDate"

    @staticmethod
    def assert_tax_rate_dates(payload, response_json):
        """Valida específicamente las fechas en la respuesta"""
        if "startDate" in payload:
            assert "startDate" in response_json, "La respuesta debe incluir startDate"
            assert response_json["startDate"] is not None, "startDate no debe ser null"
            # Opcional: validar formato de fecha
            # assert "T" in response_json["startDate"] or len(response_json["startDate"]) > 10, "Formato de fecha inválido"

        if "endDate" in payload:
            assert "endDate" in response_json, "La respuesta debe incluir endDate"
            assert response_json["endDate"] is not None, "endDate no debe ser null"


    @staticmethod
    def assert_tax_rate_update_response(original_data, update_payload, response_json):
        """Valida que la actualización se aplicó correctamente"""
        # Campos que se actualizaron
        for field in update_payload:
            if field in ["amount"]:
                assert float(response_json[field]) == float(
                    update_payload[field]), f"El {field} no se actualizó correctamente"
            else:
                assert response_json[field] == update_payload[field], f"El {field} no se actualizó correctamente"

        # Campos que NO deberían cambiar
        assert response_json["code"] == original_data["code"], "El código no debería cambiar"
        assert response_json["id"] == original_data["id"], "El ID no debería cambiar"
        assert response_json["zone"] == original_data["zone"], "La zona no debería cambiar"
        assert response_json["category"] == original_data["category"], "La categoría no debería cambiar"