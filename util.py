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

_encodeDict = {
    '0A': 'B', '1A': 'D', '2A': 'u', '0a': 'R', '1a': 'I', '2a': 'S', '0B': 'w', '1B': 'j', '2B': 'X', 
    '0b': 'y', '1b': '0', '2b': 'B', '0C': 'q', '1C': 'h', '2C': 'K', '0c': 'H', '1c': 'o', '2c': 'E', 
    '0D': 'm', '1D': 'G', '2D': '3', '0d': 'h', '1d': 'c', '2d': 'G', '0E': 'r', '1E': 'p', '2E': 'g', 
    '0e': 'u', '1e': 'N', '2e': 'a', '0F': '4', '1F': 'd', '2F': 'U', '0f': 'k', '1f': '9', '2f': 'y', 
    '0G': 'M', '1G': '4', '2G': 'M', '0g': 'e', '1g': 'F', '2g': 'e', '0H': 'I', '1H': 'Z', '2H': 'Z', 
    '0h': 'Q', '1h': 'W', '2h': 't', '0I': '7', '1I': 'E', '2I': 'F', '0i': 'z', '1i': '7', '2i': 'j', 
    '0J': 'N', '1J': 'k', '2J': 'P', '0j': 'l', '1j': 'S', '2j': 'D', '0K': 'f', '1K': 'z', '2K': 's', 
    '0k': '0', '1k': 's', '2k': 'h', '0L': '5', '1L': 'f', '2L': 'A', '0l': 'G', '1l': 'A', '2l': 'Q', 
    '0M': 'O', '1M': 'O', '2M': 'J', '0m': 's', '1m': 'n', '2m': 'q', '0N': 'T', '1N': 'l', '2N': '7', 
    '0n': 'x', '1n': 'B', '2n': 'L', '0O': '6', '1O': 'x', '2O': 'c', '0o': 't', '1o': '2', '2o': 'n', 
    '0P': 'b', '1P': 'Y', '2P': 'v', '0p': 'J', '1p': 'L', '2p': 'C', '0Q': 'A', '1Q': 'a', '2Q': 'x', 
    '0q': 'g', '1q': 'T', '2q': 'm', '0R': 'Y', '1R': '5', '2R': '0', '0r': '8', '1r': 'X', '2r': '9', 
    '0S': 'F', '1S': 't', '2S': '1', '0s': 'S', '1s': 'V', '2s': 'd', '0T': 'P', '1T': '6', '2T': 'H', 
    '0t': '2', '1t': 'Q', '2t': '8', '0U': 'C', '1U': 'J', '2U': 'p', '0u': 'D', '1u': 'm', '2u': 'W', 
    '0V': 'a', '1V': 'i', '2V': 'l', '0v': 'E', '1v': 'r', '2v': 'N', '0W': 'W', '1W': 'y', '2W': 'I', 
    '0w': '9', '1w': '1', '2w': 'f', '0X': '3', '1X': 'q', '2X': '2', '0x': 'U', '1x': 'R', '2x': 'O', 
    '0Y': 'c', '1Y': 'C', '2Y': '5', '0y': 'K', '1y': 'K', '2y': 'w', '0Z': 'j', '1Z': 'e', '2Z': 'Y', 
    '0z': 'Z', '1z': 'u', '2z': '4', '00': 'd', '10': 'v', '20': 'o', '01': '1', '11': '8', '21': '6', 
    '02': 'o', '12': '3', '22': 'R', '03': 'X', '13': 'g', '23': 'V', '04': 'n', '14': 'M', '24': 'r', 
    '05': 'p', '15': 'b', '25': 'k', '06': 'v', '16': 'H', '26': 'b', '07': 'V', '17': 'U', '27': 'i', 
    '08': 'L', '18': 'w', '28': 'z', '09': 'i', '19': 'P', '29': 'T'
}
_decodeDict = {
    '0B': 'A', '1D': 'A', '2u': 'A', '0R': 'a', '1I': 'a', '2S': 'a', '0w': 'B', '1j': 'B', '2X': 'B', 
    '0y': 'b', '10': 'b', '2B': 'b', '0q': 'C', '1h': 'C', '2K': 'C', '0H': 'c', '1o': 'c', '2E': 'c', 
    '0m': 'D', '1G': 'D', '23': 'D', '0h': 'd', '1c': 'd', '2G': 'd', '0r': 'E', '1p': 'E', '2g': 'E', 
    '0u': 'e', '1N': 'e', '2a': 'e', '04': 'F', '1d': 'F', '2U': 'F', '0k': 'f', '19': 'f', '2y': 'f', 
    '0M': 'G', '14': 'G', '2M': 'G', '0e': 'g', '1F': 'g', '2e': 'g', '0I': 'H', '1Z': 'H', '2Z': 'H', 
    '0Q': 'h', '1W': 'h', '2t': 'h', '07': 'I', '1E': 'I', '2F': 'I', '0z': 'i', '17': 'i', '2j': 'i', 
    '0N': 'J', '1k': 'J', '2P': 'J', '0l': 'j', '1S': 'j', '2D': 'j', '0f': 'K', '1z': 'K', '2s': 'K', 
    '00': 'k', '1s': 'k', '2h': 'k', '05': 'L', '1f': 'L', '2A': 'L', '0G': 'l', '1A': 'l', '2Q': 'l', 
    '0O': 'M', '1O': 'M', '2J': 'M', '0s': 'm', '1n': 'm', '2q': 'm', '0T': 'N', '1l': 'N', '27': 'N', 
    '0x': 'n', '1B': 'n', '2L': 'n', '06': 'O', '1x': 'O', '2c': 'O', '0t': 'o', '12': 'o', '2n': 'o', 
    '0b': 'P', '1Y': 'P', '2v': 'P', '0J': 'p', '1L': 'p', '2C': 'p', '0A': 'Q', '1a': 'Q', '2x': 'Q', 
    '0g': 'q', '1T': 'q', '2m': 'q', '0Y': 'R', '15': 'R', '20': 'R', '08': 'r', '1X': 'r', '29': 'r', 
    '0F': 'S', '1t': 'S', '21': 'S', '0S': 's', '1V': 's', '2d': 's', '0P': 'T', '16': 'T', '2H': 'T', 
    '02': 't', '1Q': 't', '28': 't', '0C': 'U', '1J': 'U', '2p': 'U', '0D': 'u', '1m': 'u', '2W': 'u', 
    '0a': 'V', '1i': 'V', '2l': 'V', '0E': 'v', '1r': 'v', '2N': 'v', '0W': 'W', '1y': 'W', '2I': 'W', 
    '09': 'w', '11': 'w', '2f': 'w', '03': 'X', '1q': 'X', '22': 'X', '0U': 'x', '1R': 'x', '2O': 'x', 
    '0c': 'Y', '1C': 'Y', '25': 'Y', '0K': 'y', '1K': 'y', '2w': 'y', '0j': 'Z', '1e': 'Z', '2Y': 'Z', 
    '0Z': 'z', '1u': 'z', '24': 'z', '0d': '0', '1v': '0', '2o': '0', '01': '1', '18': '1', '26': '1', 
    '0o': '2', '13': '2', '2R': '2', '0X': '3', '1g': '3', '2V': '3', '0n': '4', '1M': '4', '2r': '4', 
    '0p': '5', '1b': '5', '2k': '5', '0v': '6', '1H': '6', '2b': '6', '0V': '7', '1U': '7', '2i': '7', 
    '0L': '8', '1w': '8', '2z': '8', '0i': '9', '1P': '9', '2T': '9'

}

def encode(s):
    retValue = ''
    for i in range(len(s)):
        key = str(i%3)+s[i]
        retValue += _encodeDict.get(key, s[i])
    return retValue

def decode(s):
    retValue = ''
    for i in range(len(s)):
        key = str(i%3)+s[i]
        retValue += _decodeDict.get(key, s[i])
    return retValue



