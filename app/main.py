from dataclasses import dataclass
from time import sleep
from typing import ClassVar

from api.DuckDNS import DuckDNS
from config import Config

from art import tprint


@dataclass
class Application:
    DEFAULT_POLLING_TIME_IN_SECONDS: ClassVar[int] = 60 * 5

    config: Config = None
    duck_client: DuckDNS = None

    def __post_init__(self):
        tprint('DuckDNS', font='calgphy2')

        if not self.config:
            self.config = Config.from_env()

        if not self.duck_client:
            self.duck_client = DuckDNS(token=self.config.DUCKDNS_TOKEN)

    def run(self):
        if self.config.RUN_TYPE == 'schedule':
            print('Running refresh scheduled.')
            print(f'Polling interval: {self.DEFAULT_POLLING_TIME_IN_SECONDS / 60} min')
            while True:
                self.duck_client.refresh_ip(domain=self.config.DUCKDNS_SUBDOMAIN)
                sleep(self.DEFAULT_POLLING_TIME_IN_SECONDS)

        elif self.config.RUN_TYPE ==  'once':
            print('Running refresh once.')
            self.duck_client.refresh_ip(domain=self.config.DUCKDNS_SUBDOMAIN)


if __name__ == '__main__':
    Application().run()
