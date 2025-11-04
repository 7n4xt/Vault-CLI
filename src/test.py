from storage import list_entries


vault_data = {
    "metadata": {"created_at": "2025-10-18"},
    "entries": {
        "github": {"username": "malek", "password": "secret123"},
        "gmail": {"username": "malek.dev", "password": "p@ssw0rd!"},
    },
}

print(list_entries(vault_data))