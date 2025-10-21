import argparse
import auth

parser = argparse.ArgumentParser(description="A simple CLI tool.")
parser.add_argument('--setup', '-s',action=auth.ask_user_master_password, help="Run setup tasks.")
parser.add_argument('--add', '-a',type=str, help="Add new password to Vault")
parser.add_argument('--get', '-g',type=str, help='Get an existent password')
parser.add_argument('--list', '-l', help='List all passwords')
parser.add_argument('--delete', '-d',type=str, help='Delete a password')
parser.add_argument('--generate', help='Generats a nw password randamly')

args = parser.parse_args()