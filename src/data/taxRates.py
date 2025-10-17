from faker import Faker
from uuid import uuid4
import random

fake = Faker()


def generate_tax_rate_data(required_only=False, available_zones=None, available_categories=None):
    # Valores por defecto para zonas y categorías
    default_zone = "/api/v2/admin/zones/US"
    default_category = "/api/v2/admin/tax-categories/clothing"

    # Usar zonas disponibles si se proporcionan
    if available_zones and len(available_zones) > 0:
        zone = random.choice(available_zones)['@id']
    else:
        zone = default_zone

    # Usar categorías disponibles si se proporcionan
    if available_categories and len(available_categories) > 0:
        category = random.choice(available_categories)['@id']
    else:
        category = default_category

    tax_rate_data = {
        "code": f"VAT_{uuid4().hex[:8]}",
        "name": f"{fake.word().capitalize()} Tax Rate {random.randint(1000, 9999)}",
        "amount": round(random.uniform(0.05, 0.25), 2),
        "includedInPrice": fake.boolean(),
        "calculator": "default",
        "zone": zone,
        "category": category
    }

    if not required_only:
        # Podrías añadir campos opcionales aquí si la API los soporta
        # Por ejemplo: "startDate", "endDate", etc.
        pass

    # Validaciones
    assert tax_rate_data["code"] is not None, "El código no puede ser None"
    assert tax_rate_data["name"] is not None, "El nombre no puede ser None"
    assert tax_rate_data["amount"] is not None, "El amount no puede ser None"
    assert tax_rate_data["includedInPrice"] is not None, "El includedInPrice no puede ser None"
    assert tax_rate_data["calculator"] is not None, "El calculator no puede ser None"
    assert tax_rate_data["zone"] is not None, "El zone no puede ser None"
    assert tax_rate_data["category"] is not None, "El category no puede ser None"

    return tax_rate_data


def create_tax_rate_data(code=None, name=None, amount=None, includedInPrice=None,
                         calculator=None, zone=None, category=None):
    """
    Crea un diccionario de Tax Rate con valores personalizados o aleatorios.
    """
    tax_rate_data = {
        "code": code or f"VAT_{uuid4().hex[:8]}",
        "name": name or f"{fake.word().capitalize()} Tax Rate {random.randint(1000, 9999)}",
        "amount": amount if amount is not None else round(random.uniform(0.05, 0.25), 2),
        "includedInPrice": includedInPrice if includedInPrice is not None else fake.boolean(),
        "calculator": calculator or "default",
        "zone": zone or "/api/v2/admin/zones/US",
        "category": category or "/api/v2/admin/tax-categories/clothing"
    }

    # Convierte valores "null" en None
    tax_rate_data = {k: (None if v == "null" else v) for k, v in tax_rate_data.items()}

    # Elimina las claves cuyo valor sea None
    tax_rate_data = {k: v for k, v in tax_rate_data.items() if v is not None}

    return tax_rate_data