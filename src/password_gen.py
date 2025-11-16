"""Password generator utilities.

Provides a simple, secure password generator with length and character-set
options and a tiny entropy estimate helper.
"""
import secrets
import string
from typing import Tuple


def _build_charset(use_lower: bool = True, use_upper: bool = True, use_digits: bool = True, use_symbols: bool = True) -> str:
    parts = []
    if use_lower:
        parts.append(string.ascii_lowercase)
    if use_upper:
        parts.append(string.ascii_uppercase)
    if use_digits:
        parts.append(string.digits)
    if use_symbols:
        # remove ambiguous whitespace-like characters
        parts.append("!@#$%^&*()-_=+[]{};:,.<>/?")
    return "".join(parts)


def generate_password(length: int = 16, use_lower: bool = True, use_upper: bool = True, use_digits: bool = True, use_symbols: bool = True) -> Tuple[str, float]:
    """
    Generate a secure random password and return it with an estimated entropy (bits).

    Args:
        length: desired password length (must be >= 4)
        use_*: which character classes to include

    Returns:
        (password, entropy_bits)
    """
    if length < 4:
        raise ValueError("password length must be >= 4")

    charset = _build_charset(use_lower, use_upper, use_digits, use_symbols)
    if not charset:
        raise ValueError("At least one character class must be enabled")

    # Use secrets.choice for cryptographic randomness
    pw = "".join(secrets.choice(charset) for _ in range(length))

    # entropy estimate: log2(charset_size^length) = length * log2(charset_size)
    import math

    entropy = length * math.log2(len(charset))
    return pw, entropy


if __name__ == "__main__":
    # very small CLI for ad-hoc generation
    p, e = generate_password(16)
    print(p)
    print(f"Estimated entropy: {e:.1f} bits")
