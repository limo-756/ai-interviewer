import hashlib


def stable_hash(input_str: str) -> str:
    return hashlib.sha256(input_str.encode('utf-8')).hexdigest()
