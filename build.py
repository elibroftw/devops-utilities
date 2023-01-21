# generate config files based on inputs
from string import Template
from pathlib import Path
import os
import getpass
import secrets
import argparse
import glob

services = glob.glob('services/*.*')

parser = argparse.ArgumentParser()
parser.add_argument('--monero', action='store_true', help='build monero services')
parser.add_argument('--proton', action='store_true', help='build protonmail bridge service')
args = parser.parse_args()

user = getpass.getuser()
print('User:', user)

project_name = input('Enter project name: ')
project_folder = Path.home() / 'projects' / project_name
print('Project dir (working dir):', project_folder)
domains = f'www.{project_name} {project_name}' if project_name.count('.') == 1 else project_name
print(f'domains: {domains}')
domains_override = input('Override or confirm domains: ')
if len(domains_override) > 0:
    domains = domains_override
wallet_path = input('Enter path to wallet: ') if args.monero else ''
wallet_password = getpass.getpass('Enter wallet password: ') if args.monero else ''
rpc_password = secrets.token_urlsafe(10)
if args.monero:
    print('Generated monero wallet RPC password:', rpc_password)

variables = {
    'USER': user,
    'PROJECT': project_name,
    'WD': project_folder,
    'PROJECT_DIR': project_folder,
    'PATH': os.environ['PATH'],
    'WALLET_FILE': wallet_path,
    'WALLET_PW': wallet_password,
    'RPC_PASSWORD': rpc_password,
    'DOMAINS': domains
}

os.makedirs('build/services')

for service_template in services:
    with open(service_template, encoding='utf-8') as src_file:
        with open(f'build/services/{Path(service_template).name}', 'w', encoding='utf-8') as dest_file:
            dest_file.write(Template(src_file.read()).substitute(variables))
