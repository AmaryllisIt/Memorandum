from hashlib import sha256


def encoder(text: str):
    return sha256(text.encode()).hexdigest()

