import pytest

from src.assertions.schema_assertions import AssertionSchemas

class AssertionTaxRate:
    MODULE = "tax_rate"

    @staticmethod
    def assert_tax_rate_list_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxRates_list_schema.json", AssertionTaxRate.MODULE)

    @staticmethod
    def assert_tax_rate_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "taxRates_add_input_schema.json", AssertionTaxRate.MODULE)

    @staticmethod
    def assert_tax_rate_output_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "taxRates_add_output_schema.json", AssertionTaxRate.MODULE)

    @staticmethod
    def assert_tax_rate_id_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxRates_id_schema.json", AssertionTaxRate.MODULE)

    @staticmethod
    def assert_tax_rate_code_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxRates_code_schema.json", AssertionTaxRate.MODULE)

    @staticmethod
    def assert_tax_rate_edit_input_schema(payload):
        return AssertionSchemas().validate_json_schema(payload, "taxRates_edit_input_schema.json", AssertionTaxRate.MODULE)

    @staticmethod
    def assert_tax_rate_edit_output_schema(response):
        return AssertionSchemas().validate_json_schema(response, "taxRates_edit_output_schema.json", AssertionTaxRate.MODULE)