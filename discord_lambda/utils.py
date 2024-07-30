from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
import os
import json
PUBLIC_KEY = str(os.environ.get('PUBLIC_KEY'))

def is_signed(event: dict) -> bool:
    body = event.get('body', '')
    signature = event.get('headers', {}).get('x-signature-ed25519')
    timestamp = event.get('headers', {}).get('x-signature-timestamp')

    public_key_bytes = bytes.fromhex(PUBLIC_KEY)
    verify_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)

    message = timestamp + body  # Use the raw body for verification

    try:
        verify_key.verify(signature=bytes.fromhex(signature), data=message.encode())
    except InvalidSignature:
        return False

    return True
