from api.Base import BaseAPI
from api.Ipify import Ipify

from models.IpAddress import IPAddress


class DucksDNSError(Exception):
    ...


class DuckDNS(BaseAPI):
    BASE_URL: str = 'https://www.duckdns.org'

    def __init__(self, token: str):
        super().__init__(url=self.BASE_URL)
        self.token = token

    def refresh_ip(self, domain: str, ip: IPAddress = None):
        res = self.get(
            params='/update',
            query={
                'domains': domain,
                'token': self.token,
                'ip': Ipify().get_ip() if not ip else ip
            }
        )
        if res.text.lower() != 'ok':
            raise DucksDNSError(f'Failed to update {domain}: {res.text}. Check that you have the correct domain / token')
        print(res.text)
