import hmac
import hashlib
import binascii

def get_hash_code(msg, key):
    # Convert hex to bin
    # Encode string with utf8
    # Hash msg with SHA256, convert to hex
    key = binascii.unhexlify(key)
    msg = msg.encode()
    return hmac.new(key, msg, hashlib.sha256).hexdigest().upper()

def check_integrity_msg(msg, key, code_rev):
    # Hash msg with key and compare
    if code_rev == get_hash_code(msg, key):
        return True
    else:
        return False
