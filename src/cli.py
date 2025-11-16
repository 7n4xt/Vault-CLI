"""CLI: small command-line interface for the Vault-CLI project.

Compact CLI: handlers are small and focused (init/add/list/get/delete/generate).
"""
import argparse
import sys
from typing import Tuple, Optional

from src import storage, auth, password_gen


def _resolve_path(arg_path: Optional[str]) -> str:
    """Return vault path; prompt user if not provided."""
    if arg_path:
        return arg_path
    return input("Vault path (default vault.enc): ").strip() or "vault.enc"


def _load_vault_with_migration(path: str, mpw: str) -> Tuple[dict, str]:
    """Load a vault; if missing, offer to initialize; if plaintext detected, offer to migrate.

    Returns (vault_dict, master_password_used) or exits when the user aborts.
    """
    try:
        vault = storage.load_vault(path, mpw)
    except FileNotFoundError:
        ans = input(f"Vault {path!r} not found. Initialize new vault? (Y/n): ").strip().lower()
        if ans in ("", "y", "yes"):
            if not mpw:
                mpw = auth.get_master_password()
            vault = {"metadata": {"created_at": "2025-11-16"}, "entries": []}
            storage.save_vault(path, vault, mpw)
            print(f"Initialized encrypted vault at {path}")
        else:
            print("Aborted")
            sys.exit(0)

    if isinstance(vault, dict) and vault.pop("_was_plaintext", False):
        print("Detected plaintext vault file. You can set a master password to encrypt it.")
        newpw = auth.get_master_password("Set master password to encrypt vault: ")
        if newpw:
            storage.save_vault(path, vault, newpw)
            print("Vault encrypted and saved.")
            mpw = newpw
    return vault, mpw


def handle_init(args: argparse.Namespace) -> None:
    path = _resolve_path(args.path)
    mpw = auth.get_master_password()
    vault = {"metadata": {"created_at": "2025-11-15"}, "entries": []}
    storage.save_vault(path, vault, mpw)
    print(f"Initialized encrypted vault at {path}")


def handle_add(args: argparse.Namespace) -> None:
    path = _resolve_path(args.path)
    mpw = auth.get_master_password()
    vault, mpw = _load_vault_with_migration(path, mpw)

    # interactive prompts for missing fields
    name = args.name or input("Entry name: ").strip()
    if not name:
        print("Entry name cannot be empty")
        return
    username = args.username or input("Username: ").strip()

    # password choice: accept provided, suggest one, or prompt
    if args.password:
        pwd = args.password
    else:
        suggested, ent = password_gen.generate_password(16)
        print(f"Suggested password (entropy {ent:.1f} bits): {suggested}")
        use_s = input("Use suggested password? (Y/n): ").strip().lower()
        if use_s in ("", "y", "yes"):
            pwd = suggested
        else:
            pwd = auth.get_entry_password()

    if storage.get_entry(vault, name) is not None:
        print(f"Entry '{name}' already exists")
        return

    storage.add_entry(vault, name, username, pwd)
    storage.save_vault(path, vault, mpw)
    print(f"Added entry '{name}' to {path}")


def handle_list(args: argparse.Namespace) -> None:
    path = _resolve_path(args.path)
    mpw = args.mpw or auth.get_master_password()
    vault, _ = _load_vault_with_migration(path, mpw)
    names = storage.list_entries(vault)
    for n in names:
        entry = storage.get_entry(vault, n)
        if entry:
            print(f"- {n}: {entry.get('username')}\t({len(entry.get('password',''))} chars)")
        else:
            print(f"- {n}")


def handle_get(args: argparse.Namespace) -> None:
    path = _resolve_path(args.path)
    mpw = args.mpw or auth.get_master_password()
    vault, _ = _load_vault_with_migration(path, mpw)
    entry = storage.get_entry(vault, args.name)
    if entry is None:
        print(f"Entry '{args.name}' not found")
    else:
        print(entry)


def handle_delete(args: argparse.Namespace) -> None:
    path = _resolve_path(args.path)
    mpw = args.mpw or auth.get_master_password()
    vault, mpw = _load_vault_with_migration(path, mpw)

    name = args.name
    if not name:
        names = storage.list_entries(vault)
        if not names:
            print("No entries to delete")
            return
        for i, n in enumerate(names, start=1):
            print(f"{i}. {n}")
        choice = input("Choose entry number or name to delete: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(names):
                name = names[idx]
            else:
                print("Invalid selection")
                return
        else:
            name = choice

    confirm = input(f"Delete '{name}'? (y/N): ").strip().lower()
    if confirm not in ("y", "yes"):
        print("Aborted")
        return

    storage.delete_entry(vault, name)
    storage.save_vault(path, vault, mpw)
    print(f"Deleted entry '{name}' from {path}")


def handle_generate(args: argparse.Namespace) -> None:
    pw, entropy = password_gen.generate_password(
        length=args.length,
        use_symbols=not args.no_symbols,
        use_upper=not args.no_upper,
        use_digits=not args.no_digits,
    )
    print(pw)
    print(f"Estimated entropy: {entropy:.1f} bits")


def main() -> None:
    parser = argparse.ArgumentParser(description="Vault-CLI command line")
    parser.add_argument("--path", default=None, help="Vault file path")
    sub = parser.add_subparsers(dest="command")

    # register commands
    sub.add_parser("init", help="Initialize a new encrypted vault")
    add_p = sub.add_parser("add", help="Add a new entry to the vault")
    add_p.add_argument("--name", required=False, help="Entry name (will prompt if missing)")
    add_p.add_argument("--username", required=False, help="Username for the entry (will prompt if missing)")
    add_p.add_argument("--password", required=False, help="Password for the entry (will prompt if missing)")

    list_p = sub.add_parser("list", help="List all entries in the vault")
    list_p.add_argument("--mpw", required=False, help="Master password (optional; avoids interactive prompt)")

    get_p = sub.add_parser("get", help="Get a single entry by name")
    get_p.add_argument("--name", required=True, help="Entry name to retrieve")
    get_p.add_argument("--mpw", required=False, help="Master password (optional)")

    delete_p = sub.add_parser("delete", help="Delete an entry by name")
    delete_p.add_argument("--name", required=False, help="Entry name to delete (will prompt if missing)")
    delete_p.add_argument("--mpw", required=False, help="Master password (optional)")

    gen_p = sub.add_parser("generate", help="Generate a secure password")
    gen_p.add_argument("--length", type=int, default=16, help="Password length")
    gen_p.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    gen_p.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    gen_p.add_argument("--no-digits", action="store_true", help="Exclude digits")

    help_p = sub.add_parser("help", help="Show detailed help and examples")

    args = parser.parse_args()

    handlers = {
        "init": handle_init,
        "add": handle_add,
        "list": handle_list,
        "get": handle_get,
        "delete": handle_delete,
        "generate": handle_generate,
        "help": lambda a: (parser.print_help(), print('\nExamples:\n  python3 -m src.cli init --path vault.enc\n  python3 -m src.cli add --name github --username you --password secret\n  python3 -m src.cli generate --length 20')),
    }

    if args.command in handlers:
        handlers[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()