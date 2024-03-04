from api.DuckDNS import DuckDNS
from config import Config

from time import sleep


if __name__ == '__main__':
    config = Config.from_env()
    duck = DuckDNS(token=config.DUCKDNS_TOKEN)

    if config.RUN_TYPE == 'schedule':
        print('Running refresh scheduled.')
        while True:
            duck.refresh_ip(domain=config.DUCKDNS_SUBDOMAIN)
            sleep(60*5)

    elif config.RUN_TYPE ==  'once':
        print('Running refresh once.')
        duck.refresh_ip(domain=config.DUCKDNS_SUBDOMAIN)
        print('Done.')
