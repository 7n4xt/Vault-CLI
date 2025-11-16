"""CLI: small command-line interface for the Vault-CLI project.

This file contains a compact, commit-sized implementation for the first
interface task: an `init` subcommand to create an encrypted vault file.
"""
import argparse
from src import storage, auth
from src import password_gen


def cmd_init(args: argparse.Namespace) -> None:
	"""Create an empty encrypted vault at the given path using a master password."""
	path = args.path
	# prompt for path if user passed no --path
	if not path:
		path = input("Vault path to create: ").strip() or "vault.enc"
	# set master password interactively
	pw = auth.get_master_password()
	vault = {"metadata": {"created_at": "2025-11-15"}, "entries": []}
	storage.save_vault(path, vault, pw)
	print(f"Initialized encrypted vault at {path}")


def main() -> None:
	parser = argparse.ArgumentParser(description="Vault-CLI command line")
	parser.add_argument("--path", default="vault.enc", help="Vault file path")
	sub = parser.add_subparsers(dest="command")
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
	# delete command
	delete_p = sub.add_parser("delete", help="Delete an entry by name")
	delete_p.add_argument("--name", required=False, help="Entry name to delete (will prompt if missing)")
	delete_p.add_argument("--mpw", required=False, help="Master password (optional)")
	# generate command
	gen_p = sub.add_parser("generate", help="Generate a secure password")
	# help command prints full help plus quick examples
	help_p = sub.add_parser("help", help="Show detailed help and examples")
	gen_p.add_argument("--length", type=int, default=16, help="Password length")
	gen_p.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
	gen_p.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
	gen_p.add_argument("--no-digits", action="store_true", help="Exclude digits")

	args = parser.parse_args()
	if args.command == "init":
		cmd_init(args)
	elif args.command == "add":
		# prompt for master password and for entry password if not supplied
		mpw = auth.get_master_password()
		pwd = args.password or auth.get_entry_password()
		vault = storage.load_vault(args.path, mpw)
		# migrate plaintext vaults to encrypted on first save if detected
		if isinstance(vault, dict) and vault.pop("_was_plaintext", False):
			print("Detected plaintext vault file. You can set a master password to encrypt it.")
			newpw = auth.get_master_password("Set master password to encrypt vault: ")
			if newpw:
				storage.save_vault(args.path, vault, newpw)
				print("Vault encrypted and saved.")
		# interactive prompts for missing fields
		name = args.name
		if not name or not name.strip():
			name = input("Entry name: ").strip()
			if not name:
				print("Entry name cannot be empty")
				return
		username = args.username or input("Username: ").strip()
		# password: offer generated suggestion if not provided
		if not args.password:
			suggested, ent = password_gen.generate_password(16)
			print(f"Suggested password (entropy {ent:.1f} bits): {suggested}")
			use_s = input("Use suggested password? (Y/n): ").strip().lower()
			if use_s in ("", "y", "yes"):
				pwd = suggested
			else:
				pwd = auth.get_entry_password()
		else:
			pwd = args.password or auth.get_entry_password()
		# avoid duplicates
		if storage.get_entry(vault, name) is not None:
			print(f"Entry '{name}' already exists")
			return
		storage.add_entry(vault, name, username, pwd)
		storage.save_vault(args.path, vault, mpw)
		print(f"Added entry '{name}' to {args.path}")
	elif args.command == "list":
		mpw = args.mpw or auth.get_master_password()
		vault = storage.load_vault(args.path, mpw)
		names = storage.list_entries(vault)
		for n in names:
			entry = storage.get_entry(vault, n)
			if entry:
				print(f"- {n}: {entry.get('username')}\t({len(entry.get('password',''))} chars)")
			else:
				print(f"- {n}")
	elif args.command == "get":
		mpw = args.mpw or auth.get_master_password()
		vault = storage.load_vault(args.path, mpw)
		entry = storage.get_entry(vault, args.name)
		if entry is None:
			print(f"Entry '{args.name}' not found")
		else:
			print(entry)
	elif args.command == "delete":
		mpw = args.mpw or auth.get_master_password()
		vault = storage.load_vault(args.path, mpw)
		# if name not provided, list entries and prompt user to choose
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
		storage.save_vault(args.path, vault, mpw)
		print(f"Deleted entry '{name}' from {args.path}")
	elif args.command == "generate":
		pw, entropy = password_gen.generate_password(
			length=args.length,
			use_symbols=not args.no_symbols,
			use_upper=not args.no_upper,
			use_digits=not args.no_digits,
		)
		print(pw)
		print(f"Estimated entropy: {entropy:.1f} bits")
	elif args.command == "help":
		parser.print_help()
		print(
			'''
Examples:
  python3 -m src.cli init --path vault.enc
  python3 -m src.cli add --name github --username you --password secret
  python3 -m src.cli generate --length 20
			'''
		)
	else:
		parser.print_help()


if __name__ == "__main__":
	main()