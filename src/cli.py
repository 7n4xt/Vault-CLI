"""CLI: small command-line interface for the Vault-CLI project.

This file contains a compact, commit-sized implementation for the first
interface task: an `init` subcommand to create an encrypted vault file.
"""
import argparse
import getpass
from src import storage


def cmd_init(args: argparse.Namespace) -> None:
	"""Create an empty encrypted vault at the given path using a master password."""
	path = args.path
	pw = getpass.getpass("Master password: ")
	vault = {"metadata": {"created_at": "2025-11-15"}, "entries": []}
	storage.save_vault(path, vault, pw)
	print(f"Initialized encrypted vault at {path}")


def main() -> None:
	parser = argparse.ArgumentParser(description="Vault-CLI command line")
	parser.add_argument("--path", default="vault.enc", help="Vault file path")
	sub = parser.add_subparsers(dest="command")
	sub.add_parser("init", help="Initialize a new encrypted vault")

	args = parser.parse_args()
	if args.command == "init":
		cmd_init(args)
	else:
		parser.print_help()


if __name__ == "__main__":
	main()