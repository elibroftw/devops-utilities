import argparse
import os
import subprocess
import sys
# from modules.emailing import send_email

from git import Repo

"""
Features
- Auto-deployment
- Auto-increase Digital Ocean storage (TODO)
"""
BASH = 'bash -cil \'exec "$@"\' _'


def reload_server():
    if os.path.exists('gunicorn.pid'):
        print('Restarting gunicorn via HUP')
        subprocess.run('kill -HUP $(cat gunicorn.pid)', shell=True)


def stop_server():
    if os.path.exists('gunicorn.pid'):
        subprocess.run('kill $(cat gunicorn.pid)', shell=True)


def start_server():
    subprocess.Popen(f'{BASH} gunicorn', shell=True)


def pull_remote(restart_server=True):
    repo = Repo('.')
    o = repo.remotes.origin
    o.fetch()
    # works if production branch is not master
    active_branch = repo.active_branch
    if any(repo.iter_commits(f'{active_branch}..origin/{active_branch}')):
        print('Pulling new changes')
        repo.git.reset('--hard', f'origin/{active_branch}')
        repo.git.submodule('sync')
        for submodule in repo.submodules:
            submodule.update(recursive=True, init=True)
        print('HEAD reset')
        print('installing requirements.txt')
        subprocess.run(f'{sys.executable} -m pip install --upgrade -r requirements.txt', shell=True)
        if restart_server:
            reload_server()
        return True
    return False


# def start_monerod(monerod=Path(os.environ['MONERO']) / 'monerod', check_if_running=False):
#     if check_if_running:
#         with suppress(requests.RequestException):
#             port = 38081 if is_dev() else 18081  # 38081 is the stagenet daemon  RPC port
#             return requests.post(f'http://127.0.0.1:{port}/json_rpc',
#                                  json={'jsonrpc': '2.0', 'id': '0', 'method': 'get_version'})
#     print('INFO: Starting Monero Daemon')
#     # TODO: run pruned node instead of full node?
#     #  Also when scaling, maybe run monerod only on one droplet to save on storage space.
#     #  It would require daemon address for production and would save on storage space.
#     # 5MB log size limit
#     monerod_cmd = [monerod, '--config-file', 'other_files/monerod.conf']
#     if platform.system() == 'Windows':
#         from subprocess import CREATE_NEW_PROCESS_GROUP, CREATE_NO_WINDOW
#         creationflags = CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
#     else:
#         creationflags = 0
#     Popen(monerod_cmd, stdin=DEVNULL, stdout=DEVNULL, shell=True, start_new_session=True,
#           creationflags=creationflags)


def update_monerod():
    # also update modules/monero.py
    # TODO: v2.0
    """ Checks for monerod update
    If update found, shutdown monerod via API,
    download new binaries to ~/Downloads,
    force-close monerod and monero-wallet-rpc if they are still running
    replace binaries (recommend storing them in ~/bin/monero)
    start monerod and monero-wallet-rpc using .env values
    XMR_WALLET_PW is set in production only
    """
    # check monerodocs for update method
    # with suppress(requests.RequestException):
    #     return requests.post(f'http://127.0.0.1:18081/json_rpc',
    #                            json={'jsonrpc': '2.0', 'id': '0', 'method': '???'})
    # https://web.getmonero.org/resources/developer-guides/daemon-rpc.html#update
    pass


def other_tasks():
    """
    - TODO: droplet block space auto increase
    """
    pass


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    parser = argparse.ArgumentParser(description='Cronjob for this project')
    parser.add_argument('--monero-node', action='store_true', help='check for monero updates')
    parser.add_argument('--live-server', action='store_true', help='start server after pull')
    parser.add_argument('--restart-server', action='store_true', help='restart server')
    args = parser.parse_args()
    head_reset = pull_remote(restart_server=args.live_server)
    if not head_reset and args.restart_server:
        print('restarting server')
        reload_server()
    if args.monero_node:
        print('checking for monero updates')
        update_monerod()
