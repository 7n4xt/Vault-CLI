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