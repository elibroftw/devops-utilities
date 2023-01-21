#!/bin/bash

allow_services_without_root() {
    # usage `allow_services_without_root monerod monero-wallet-rpc-prod monero-wallet-rpc-dev lenerva.com dev.lenerva.com`
    for service in "$@"; do
        # allow user to start/stop/restart/reload the service
        sudoer_rule="$USER ALL=(ALL) NOPASSWD: /usr/bin/systemctl start $service, /usr/bin/systemctl stop $service, /usr/bin/systemctl restart $service, /usr/bin/systemctl reload $service"

        # Check if the rule already exists in the sudoers file
        if ! grep -q "$sudoer_rule" /etc/sudoers; then
            # Append the rule to the sudoers file
            echo "$sudoer_rule" | sudo tee -a /etc/sudoers > /dev/null
            echo "SUCCESS: sudoers file modified to allow $USER to start/stop/restart/reload $service"
        else
            echo "INFO: rule for $service already exists in the sudoers file"
        fi
    done
}
