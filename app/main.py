from api.DuckDNS import DuckDNS
from config import Config

from time import sleep


if __name__ == '__main__':
    while True:
        config = Config.from_env()

        duck = DuckDNS(token=config.DUCKDNS_TOKEN)
        duck.refresh_ip(domain=config.DUCKDNS_DOMAIN)

        sleep(60*5)
