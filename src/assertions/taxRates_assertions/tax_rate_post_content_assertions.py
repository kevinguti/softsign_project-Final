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

    @staticmethod
    def assert_tax_rate_response(payload, response_json):
        """Valida que la respuesta coincida con el payload enviado"""
        assert response_json["code"] == payload["code"], "El code en la respuesta no coincide"
        assert response_json["name"] == payload["name"], "El name en la respuesta no coincide"
        assert float(response_json["amount"]) == float(payload["amount"]), "El amount en la respuesta no coincide"
        assert response_json["includedInPrice"] == payload[
            "includedInPrice"], "El includedInPrice en la respuesta no coincide"
        assert response_json["calculator"] == payload["calculator"], "El calculator en la respuesta no coincide"