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
	add_p.add_argument("--name", required=True, help="Entry name")
	add_p.add_argument("--username", required=True, help="Username for the entry")
	add_p.add_argument("--password", required=False, help="Password for the entry (will prompt if missing)")
	list_p = sub.add_parser("list", help="List all entries in the vault")
	list_p.add_argument("--mpw", required=False, help="Master password (optional; avoids interactive prompt)")
	get_p = sub.add_parser("get", help="Get a single entry by name")
	get_p.add_argument("--name", required=True, help="Entry name to retrieve")
	get_p.add_argument("--mpw", required=False, help="Master password (optional)")
	# delete command
	delete_p = sub.add_parser("delete", help="Delete an entry by name")
	delete_p.add_argument("--name", required=True, help="Entry name to delete")
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
		# validation: name must not be empty
		if not args.name or not args.name.strip():
			print("Entry name cannot be empty")
			return
		# avoid duplicates
		if storage.get_entry(vault, args.name) is not None:
			print(f"Entry '{args.name}' already exists")
			return
		storage.add_entry(vault, args.name, args.username, pwd)
		storage.save_vault(args.path, vault, mpw)
		print(f"Added entry '{args.name}' to {args.path}")
	elif args.command == "list":
		mpw = args.mpw or auth.get_master_password()
		vault = storage.load_vault(args.path, mpw)
		names = storage.list_entries(vault)
		for n in names:
			print(n)
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
		storage.delete_entry(vault, args.name)
		storage.save_vault(args.path, vault, mpw)
		print(f"Deleted entry '{args.name}' from {args.path}")
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