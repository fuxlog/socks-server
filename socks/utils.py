import re
import struct
import ipaddress
from .constants import AddressType


def validate_password(password: str) -> bool:    
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,254}$"
    if re.match(pattern, password) is None:
        return False
    
    return True


def validate_username(username: str) -> bool:
    pattern = r"^[a-zA-Z0-9_]{4,254}$"
    if re.match(pattern, username) is None:
        return False
    
    return True


def str_address(address: bytes, address_type):
    if address_type == AddressType.IPV4:
        result = '.'.join(map(str, struct.unpack('BBBB', address)))
        return result
    
    if address_type == AddressType.IPV6:
        result = ':'.join('{:04x}'.format(b) for b in struct.unpack('!HHHHHHHH', address))
        return result
    
    if address_type == AddressType.DOMAINNAME:
        address_len = address[0]
        result = address[1:1+address_len].decode()
        return result

    return None

def int_port(port: bytes):
    result = struct.unpack('!H', port)[0]
    return result


def bytes_address(address: str, address_type: int) -> bytes:
    if address_type == AddressType.DOMAINNAME:
        result = len(address).to_bytes(1, "big") + address.encode()
        return result
    
    elif address_type == AddressType.IPV4:
        return ipaddress.IPv4Address(address).packed
    elif address_type == AddressType.IPV6:
        return ipaddress.IPv6Address(address).packed