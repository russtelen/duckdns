from datetime import datetime

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

    def refresh_ip(self, domain: str, ip: IPAddress = None, logs: bool = True):
        res = self.get(
            params='/update',
            query={
                'domains': domain,
                'token': self.token,
                'ip': Ipify().get_ip() if not ip else ip,
                'verbose': True
            }
        )
        if 'ok' not in res.text.lower():
            raise DucksDNSError(f'Failed to update {domain}: {res.text}. Check that you have the correct domain / token')
        if logs:
            print(f'{"-"*80}')
            print(res.text)
            print(f"Your IP was updated at {datetime.utcnow()} UTC")
            print(f'{"-"*80}')
