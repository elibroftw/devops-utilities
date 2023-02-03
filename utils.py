#!/usr/bin/python3

import platform
import os

def systemd_services_without_root(*services):
    if platform.system() == 'Windows':
        print('ERROR: allow_services_without_root is not currently supported on Windows')
        return 1
    user = os.getlogin()
    new_rules = {}
    for service in services:
        commands = ', '.join((f'/usr/bin/systemctl {unit_cmd} {service}' for unit_cmd in ('start', 'stop', 'restart', 'reload')))
        new_rules[service] = f'{user} ALL=(ALL) NOPASSWD: {commands}\n'
    sudoers_file = f'/etc/sudoers.d/{user}'
    with open(sudoers_file, 'a+', encoding='utf-8') as f:
        existing_rules = set(f.readlines())
        rules_to_add = {}
        for service, new_rule in new_rules.items():
            if new_rule in existing_rules:
                print(f'INFO: rule for {service} already exists in /etc/sudoers')
            else:
                rules_to_add[service] = new_rule
        for service, rule in rules_to_add.items():
            f.write(rule)
            print(f'SUCCESS: {sudoers_file} modified to allow {user} to start/stop/restart/reload {service}')
    return 0


systemd_services_without_root('example')
