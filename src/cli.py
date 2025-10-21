import argparse

parser = argparse.ArgumentParser(description="A simple CLI tool.")
parser.add_argument('--setup', '-s', help="Run setup tasks.")
parser.add_argument('--add', '-a', help="Add new password to Vault")
parser.add_argument('--get', '-g', help='Get an existent password')
parser.add_argument('--list', '-l', help='List all passwords')
parser.add_argument('--delete', '-d', help='Delete a password')
parser.add_argument('--generate', help='Generats a nw password randamly')