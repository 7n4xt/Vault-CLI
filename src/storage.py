def add_entry(vault_data, name, username, password):
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

def get_entry(vault_data, name):
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

def delete_entry(vault_data, name):
    """
    Delete an entry from the vault data by name.
    
    Args:
        vault_data (dict): The current vault data.
        name (str): The name of the entry to delete.
    """
    if "entries" in vault_data:
        vault_data["entries"] = [entry for entry in vault_data["entries"] if entry["name"] != name]
    return vault_data

def list_entries(vault_data):
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
        raise KeyError("vault_data must contain an 'entries' key.")
    
    if not hasattr(entries, "keys"):
        raise TypeError("vault_data['entries'] must be dict-like.")
    
    return list(entries.keys())