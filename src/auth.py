"""Authentication helpers for CLI prompts.

This module centralizes password prompts so the CLI remains thin and testable.
"""
import getpass
from typing import Optional


def get_master_password(prompt: str = "Master password: ") -> str:
    """Prompt the user for the master password and return it as a string."""
    return getpass.getpass(prompt)


def get_entry_password(prompt: str = "Entry password: ") -> str:
    """Prompt the user for a per-entry password and return it."""
    return getpass.getpass(prompt)