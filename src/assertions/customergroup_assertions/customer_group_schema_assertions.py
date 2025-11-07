import pytest

from src.assertions.schema_assertions import AssertionSchemas

class AssertionCustomerGroup:
    MODULE = "customer_group"

    @staticmethod
    def assert_customer_group_list_schema(response_json):
        """Valida la estructura de una LISTA/COLLECTION de customer groups"""
        # Primero valida que sea una colección
        assert response_json.get("@type") == "hydra:Collection", "Response should be a hydra:Collection"
        assert "hydra:member" in response_json, "Collection should have hydra:member"
        assert isinstance(response_json["hydra:member"], list), "hydra:member should be a list"

        # Luego valida CADA ITEM de la colección con tu schema individual
        for customer_group in response_json["hydra:member"]:
            AssertionSchemas().validate_json_schema(
                customer_group,  # ← Aplicar schema a cada objeto individual
                "customer_group_get_output_schema.json",
                AssertionCustomerGroup.MODULE
            )

    @staticmethod
    def assert_customer_group_collection_schema(response_json):
        """Alias para mantener consistencia - mismo método que list_schema"""
        return AssertionCustomerGroup.assert_customer_group_list_schema(response_json)

    @staticmethod
    def assert_customer_group_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "customer_group_post_input_schema.json", AssertionCustomerGroup.MODULE)

    @staticmethod
    def assert_customer_group_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "customer_group_post_output_schema.json", AssertionCustomerGroup.MODULE)

    @staticmethod
    def assert_customer_group_code_schema(response):
        return AssertionSchemas().validate_json_schema(response, "customer_group_get_output_schema.json", AssertionCustomerGroup.MODULE)

    @staticmethod
    def assert_customer_group_edit_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "customer_group_put_input_schema.json", AssertionCustomerGroup.MODULE)

    @staticmethod
    def assert_customer_group_edit_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "customer_group_put_output_schema.json", AssertionCustomerGroup.MODULE)