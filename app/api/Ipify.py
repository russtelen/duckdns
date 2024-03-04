from api.Base import BaseAPI
from models.IpAddress import IPAddress


class IpifyError(Exception):
    ...


class Ipify(BaseAPI):
    BASE_URL: str = 'https://api.ipify.org'

    def __init__(self):
        super().__init__(url=self.BASE_URL)

    def get_ip(self) -> IPAddress:
        res = self.get(
            query={
                'format': 'json'
            }
        )
        return IPAddress(res.json().get('ip', '0.0.0.0'))
