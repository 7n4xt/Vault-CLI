import json
import os
import base64
from typing import Any, Dict

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def _b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    """
    Derive a 256-bit key from a password and salt using PBKDF2-HMAC-SHA256.

    Args:
        password (str): The master password.
        salt (bytes): A cryptographic salt.
        iterations (int): Number of PBKDF2 iterations.

    Returns:
        bytes: A 32-byte derived key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))


def encrypt_bytes(plaintext: bytes, password: str, iterations: int = 200_000) -> Dict[str, Any]:
    """
    Encrypt raw bytes using a password. Uses PBKDF2 for key derivation and AES-GCM for encryption.

    Returns a JSON-serializable dict containing base64-encoded salt, nonce and ciphertext.
    """
    salt = os.urandom(16)
    key = derive_key(password, salt, iterations=iterations)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    return {
        "salt": _b64encode(salt),
        "nonce": _b64encode(nonce),
        "ciphertext": _b64encode(ciphertext),
        "iterations": iterations,
        "kdf": "pbkdf2_sha256",
        "cipher": "aes_gcm",
    }


def decrypt_bytes(payload: Dict[str, Any], password: str) -> bytes:
    """
    Decrypt bytes previously encrypted with `encrypt_bytes`.

    Args:
        payload (dict): The dict produced by `encrypt_bytes`.
        password (str): The password used to derive the key.

    Returns:
        bytes: The decrypted plaintext.
    """
    salt = _b64decode(payload["salt"])
    nonce = _b64decode(payload["nonce"])
    ciphertext = _b64decode(payload["ciphertext"])
    iterations = int(payload.get("iterations", 200_000))

    key = derive_key(password, salt, iterations=iterations)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)


def encrypt_json(data: Dict[str, Any], password: str, iterations: int = 200_000) -> str:
    """
    Encrypt a JSON-serializable dictionary and return a compact JSON string containing
    the encrypted payload (base64 fields).
    """
    plaintext = json.dumps(data, separators=(",", ":")).encode("utf-8")
    payload = encrypt_bytes(plaintext, password, iterations=iterations)
    return json.dumps(payload, separators=(",", ":"))


def decrypt_json(encrypted_json: str, password: str) -> Dict[str, Any]:
    """
    Decrypt a JSON string produced by `encrypt_json` and return the original dictionary.
    """
    # Try to parse as encrypted payload first. If it doesn't look like the
    # expected encrypted dict, fall back to assuming it's plaintext JSON.
    try:
        payload = json.loads(encrypted_json)
    except json.JSONDecodeError:
        # not JSON at all
        raise ValueError("Vault file is not valid JSON or encrypted payload")

    # Heuristic: encrypted payload should contain the 'ciphertext' key
    if isinstance(payload, dict) and "ciphertext" in payload:
        try:
            plaintext = decrypt_bytes(payload, password)
            return json.loads(plaintext.decode("utf-8"))
        except Exception as exc:
            # map cryptography InvalidTag to a clearer error
            from cryptography.exceptions import InvalidTag

            if isinstance(exc, InvalidTag):
                raise ValueError("Decryption failed: wrong password or corrupted file") from exc
            raise

    # Not an encrypted payload — assume it's plaintext JSON data and return it
    # Mark it so callers can detect a legacy plaintext vault and migrate
    if isinstance(payload, dict):
        payload["_was_plaintext"] = True
    return payload


def save_encrypted(path: str, data: Dict[str, Any], password: str, iterations: int = 200_000) -> None:
    """
    Atomically save encrypted data to `path` using `password`.

    Raises exceptions on I/O or encryption errors.
    """
    encrypted = encrypt_json(data, password, iterations=iterations)
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(encrypted)
    os.replace(tmp, path)


def load_encrypted(path: str, password: str) -> Dict[str, Any]:
    """
    Load and decrypt data from `path` using `password`.

    Raises exceptions on I/O or decryption errors.
    """
    with open(path, "r", encoding="utf-8") as fh:
        encrypted = fh.read()
    return decrypt_json(encrypted, password)
