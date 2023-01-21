from modules.database import *
from modules.store import *
from getpass import getpass
import sys
# CLI for non server related things

import argparse
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='additional help', dest='subcommand')

# store
publish_parser = subparsers.add_parser('publish', help='mark product as published')
publish_parser.add_argument('product_id', type=str, help='product id')

# database
add_user_aliases = ['adduser', 'create-user']
add_user_parser = subparsers.add_parser('add-user', aliases=add_user_aliases, help='add a user')
add_user_parser.add_argument('username', help='username', type=str)
add_user_parser.add_argument('--password', help='password', type=str)
add_user_parser.add_argument('--admin', action='store_true', help='user is admin', default=False)

clone_items_parser = subparsers.add_parser('clone-items', help='clone dev products to prod')
clone_items_parser.add_argument('--overwrite', action='store_true', help='overwrite items', default=False)

args = parser.parse_args()
if 'subcommand' in args:
    if args.subcommand == 'publish':
        printify_published(args.product_id)
    elif args.subcommand == 'add-user':
        if not args.password:
            args.password = getpass(f'Enter password for user {args.username}: ')
        if not args.password:
            print('ERROR: password cannot be empty', file=sys.stderr)
            sys.exit(1)
        create_user(args.username, args.password, admin=args.admin)
    elif args.subcommand == 'clone-items':
        clone_items_to_prod(overwrite=args.overwrite)
    else:
        parser.print_help()
else:
    parser.print_help()
