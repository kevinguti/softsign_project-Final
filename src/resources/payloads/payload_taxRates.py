import json

class PayloadTaxRate:

    @staticmethod
    def build_payload_tax_rate(data):
        payload = {
            "code": data.get("code"),
            "name": data.get("name"),
            "amount": data.get("amount"),
            "includedInPrice": data.get("includedInPrice"),
            "calculator": data.get("calculator"),
            "zone": data.get("zone"),
            "category": data.get("category")
        }
        return payload