import urllib.parse
import hashlib

BASE_az = 26
ZERO = 'a'
ORD_ZERO = ord(ZERO)


def int2az(n):
    """
    Converts an integer to a number in base 26 with 0='a' ... 25='z'
    """
    az = '' if n > 0 else ZERO
    while n > 0:
        az = chr((n % BASE_az) + ORD_ZERO) + az
        n = n // BASE_az
    return az

def az2int(az):
    """
    Converts a number in base 26 (0='a' ... 25='z') to an integer
    """
    n = 0
    for ch in az:
        n = BASE_az * n + (ord(ch) - ORD_ZERO)
    return n

def str2az(s):
    """
    Converts a string of ascii coded characters to an 'az' coded string
    """
    az = ''
    for ch in s:
        az = az + ('aa'+int2az(ord(ch)))[-2:]
    return az

def bytes2az(b):
    """
    Converts a list of bytes an 'az' coded string
    """
    az = ''
    for ch in b:
        az = az + ('aa'+int2az(ch))[-2:]
    return az

def az2str(az):
    """
    Converts an 'az' coded string to a string of ascii coded characters
    """
    s = ''
    for i in range(0, len(az), 2):
        s = s + chr(az2int(az[i:i+2]))
    return s




