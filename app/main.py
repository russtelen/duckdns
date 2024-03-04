from api.DuckDNS import DuckDNS
from config import Config

config = Config.from_env()

duck = DuckDNS(token=config.DUCKDNS_TOKEN)
duck.refresh_ip(domain=config.DUCKDNS_DOMAIN)
