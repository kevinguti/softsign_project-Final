class AssertionTaxRateErrors:

    @staticmethod
    def assert_tax_rate_error_response(response_json, expected_error_field=None):
        """Valida la estructura de respuesta de error para tax rates"""
        assert "@context" in response_json, "La respuesta de error debe contener '@context'"
        assert "@type" in response_json, "La respuesta de error debe contener '@type'"
        assert "hydra:title" in response_json, "La respuesta de error debe contener 'hydra:title'"
        assert "hydra:description" in response_json, "La respuesta de error debe contener 'hydra:description'"

        if expected_error_field:
            assert "violations" in response_json, "La respuesta de error debe contener 'violations'"
            violations = response_json["violations"]
            assert any(violation["propertyPath"] == expected_error_field for violation in violations), \
                f"Debe haber una violación para el campo: {expected_error_field}"