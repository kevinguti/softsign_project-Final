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


    @staticmethod
    def build_update_payload(data):
        """Para actualización - solo campos editables en formato JSON-LD"""
        payload = {}

        # Solo incluir campos que están presentes en los datos
        editable_fields = ["name", "amount", "includedInPrice", "calculator", "startDate", "endDate"]
        for field in editable_fields:
            if field in data and data[field] is not None:
                payload[field] = data[field]

        return payload

    @staticmethod
    def build_name_update_payload(new_name):
        """Para actualizar solo el nombre"""
        return {
            "name": new_name
        }

    @staticmethod
    def build_amount_update_payload(new_amount):
        """Para actualizar solo el amount (en formato string para JSON-LD)"""
        return {
            "amount": str(new_amount)  # Convertir a string para JSON-LD
        }

    @staticmethod
    def build_included_in_price_update_payload(new_value):
        """Para actualizar solo includedInPrice"""
        return {
            "includedInPrice": new_value
        }

    @staticmethod
    def build_dates_update_payload(start_date, end_date):
        """Para actualizar solo las fechas"""
        return {
            "startDate": start_date,
            "endDate": end_date
        }
