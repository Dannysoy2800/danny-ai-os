"""Security helpers for authentication secrets.

Set PAI_AUTH_ENCRYPTION_KEY to a Fernet key supplied by a secret manager.
Never generate or persist a production key automatically in application code.
"""
from __future__ import annotations

import os

from cryptography.fernet import Fernet, InvalidToken


def _fernet() -> Fernet:
    key = os.getenv("PAI_AUTH_ENCRYPTION_KEY")
    if not key:
        raise RuntimeError(
            "PAI_AUTH_ENCRYPTION_KEY is required before storing or reading TOTP secrets."
        )
    try:
        return Fernet(key.encode("ascii"))
    except (ValueError, UnicodeEncodeError) as exc:
        raise RuntimeError("PAI_AUTH_ENCRYPTION_KEY must be a valid Fernet key.") from exc


def encrypt_totp_secret(secret: str) -> str:
    """Encrypt a TOTP seed before it is persisted in TwoFactorMethod."""
    if not secret:
        raise ValueError("TOTP secret must not be empty.")
    return _fernet().encrypt(secret.encode("utf-8")).decode("ascii")


def decrypt_totp_secret(ciphertext: str) -> str:
    """Decrypt a stored TOTP seed; invalid ciphertext raises ValueError."""
    try:
        return _fernet().decrypt(ciphertext.encode("ascii")).decode("utf-8")
    except (InvalidToken, UnicodeEncodeError) as exc:
        raise ValueError("TOTP secret could not be decrypted.") from exc
