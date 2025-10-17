from src.routes.endpoint_zones import EndpointZone
from src.routes.request import SyliusRequest

class ZoneCall:
    @classmethod
    def view_by_id(cls, headers, zone_id):
        response = SyliusRequest().get(EndpointZone.by_id(zone_id), headers)
        return response

    @classmethod
    def view_by_code(cls, headers, zone_code):
        response = SyliusRequest().get(EndpointZone.by_code(zone_code), headers)
        return response

    @classmethod
    def view_all(cls, headers, **params):
        url = EndpointZone.zone_with_params(**params) if params else EndpointZone.zone()
        response = SyliusRequest().get(url, headers)
        return response

    @classmethod
    def create(cls, headers, payload):
        response = SyliusRequest().post(EndpointZone.zone(), headers, payload)
        return response  # Devuelve el objeto Response completo

    @classmethod
    def update_by_id(cls, headers, payload, zone_id):
        response = SyliusRequest().put(EndpointZone.by_id(zone_id), headers, payload)
        return response

    @classmethod
    def update_by_code(cls, headers, payload, zone_code):
        response = SyliusRequest().put(EndpointZone.by_code(zone_code), headers, payload)
        return response

    @classmethod
    def delete_by_id(cls, headers, zone_id):
        response = SyliusRequest().delete(EndpointZone.by_id(zone_id), headers)
        return response

    @classmethod
    def delete_by_code(cls, headers, zone_code):
        response = SyliusRequest().delete(EndpointZone.by_code(zone_code), headers)
        return response