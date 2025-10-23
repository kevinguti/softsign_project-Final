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
        if "startDate" in data:
            payload["startDate"] = data.get("startDate")
        if "endDate" in data:
            payload["endDate"] = data.get("endDate")

        return payload

    @staticmethod
    def build_minimal_payload(code, name, amount, zone, category):
        """Para cuando solo quieres los campos mínimos requeridos"""
        return {
            "code": code,
            "name": name,
            "amount": amount,
            "includedInPrice": False,
            "calculator": "default",
            "zone": zone,
            "category": category
        }

    @staticmethod
    def build_payload_with_dates(code, name, amount, zone, category, startDate, endDate):
        """Para crear payload con fechas específicas"""
        return {
            "code": code,
            "name": name,
            "amount": amount,
            "includedInPrice": False,
            "calculator": "default",
            "zone": zone,
            "category": category,
            "startDate": startDate,
            "endDate": endDate
        }