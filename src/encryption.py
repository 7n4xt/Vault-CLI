import json

def init_vault(path, master_password):
    """
    Initialize a secure vault at the specified path using the provided master password.
    
    Args:
        path (str): The file path where the vault will be created.
        master_password (str): The master password to secure the vault.
    
    Returns:
        bool: True if the vault was successfully initialized, False otherwise.
    """
    try:

        master_password_data = {
            "password": master_password,
            "length": len(master_password),
            "path": path
        }

        with open(path, 'w', encoding='utf-8') as vault_file:
            json.dump(master_password_data, vault_file, indent=4)
        
        return True
    except Exception as e:
        print(f"Error initializing vault: {e}")
        return False
    
def load_vault(path):
    """
    Load the vault data from the specified path.
    
    Args:
        path (str): The file path where the vault is located.
    
    Returns:
        dict: The vault data if successfully loaded, None otherwise.
    """
    try:
        with open(path, 'r', encoding='utf-8') as vault_file:
            vault_data = json.load(vault_file)
        print("Vault loaded successfully.")
        return vault_data
    except Exception as e:
        print(f"Error loading vault: {e}")
        return None
    