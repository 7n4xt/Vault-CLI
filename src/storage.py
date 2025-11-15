from typing import Dict, Any
from . import encryption


def add_entry(vault_data: Dict[str, Any], name: str, username: str, password: str) -> Dict[str, Any]:
    """
    Add a new entry to the vault data.
    
    Args:
        vault_data (dict): The current vault data.
        name (str): The name of the entry.
        username (str): The username for the entry.
        password (str): The password for the entry.
    
    Returns:
        dict: Updated vault data with the new entry added.
    """
    if "entries" not in vault_data:
        vault_data["entries"] = []
    
    new_entry = {
        "name": name,
        "username": username,
        "password": password
    }
    
    vault_data["entries"].append(new_entry)
    return vault_data

def get_entry(vault_data: Dict[str, Any], name: str):
    """
    Retrieve an entry from the vault data by name.
    
    Args:
        vault_data (dict): The current vault data.
        name (str): The name of the entry to retrieve.
    """
    if "entries" in vault_data:
        for entry in vault_data["entries"]:
            if entry["name"] == name:
                return entry
    return None

def delete_entry(vault_data: Dict[str, Any], name: str) -> Dict[str, Any]:
    """
    Delete an entry from the vault data by name.
    
    Args:
        vault_data (dict): The current vault data.
        name (str): The name of the entry to delete.
    """
    if "entries" in vault_data:
        vault_data["entries"] = [entry for entry in vault_data["entries"] if entry["name"] != name]
    return vault_data

def list_entries(vault_data: Dict[str, Any]) -> list:
    """
    List all entry names in the vault data.
    
    Args:
        vault_data (dict): The current vault data, expected to have an "entries" key.
    
    Returns:
        list: A list of entry names (strings or other hashable keys).
    
    Raises:
        KeyError: If "entries" is missing from vault_data.
        TypeError: If vault_data["entries"] is not dict-like.
    """
    if not isinstance(vault_data, dict):
        raise TypeError("vault_data must be a dictionary.")
    
    entries = vault_data.get("entries")
    if entries is None:
        return []

    # entries expected to be a list of dicts with a 'name' key
    if not isinstance(entries, list):
        raise TypeError("vault_data['entries'] must be a list of entry dicts.")

    return [e.get("name") for e in entries if isinstance(e, dict) and "name" in e]


def save_vault(path: str, vault_data: Dict[str, Any], master_password: str) -> None:
    """
    Save vault data encrypted to disk at `path` using `master_password`.
    """
    encryption.save_encrypted(path, vault_data, master_password)


def load_vault(path: str, master_password: str) -> Dict[str, Any]:
    """
    Load and decrypt vault data from `path` using `master_password`.
    """
    return encryption.load_encrypted(path, master_password)