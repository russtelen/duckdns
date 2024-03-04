from dataclasses import dataclass


class IpAddressError(Exception):
    ...


@dataclass
class IPAddress:
    ip_str: str

    def __post_init__(self):
        self.octets = [int(octet) for octet in self.ip_str.split('.')]
        self.is_valid()

    def is_valid(self):
        if not len(self.octets) == 4 and all(0 <= octet <= 255 for octet in self.octets):
            raise IpAddressError(f'Invalid IP: {self.ip_str}')

    def __str__(self):
        return ".".join(map(str, self.octets))
