#!/usr/bin/env bash

# Pre-settings
export ANSIBLE_CONFIG=deploy/ansible.cfg
export ANSIBLE_HOST_KEY_CHECKING=False
export ANSIBLE_RECORD_HOST_KEYS=False

# Render hosts file
cat >/tmp/hosts<<EOF
[servers]
app_server ansible_host=${SERVER_ADDRESS} ansible_user=${SERVER_USERNAME}
EOF

# Execute deploy
ansible-playbook -i /tmp/hosts --user=${SERVER_USERNAME} ./deploy/deploy.yaml

# Done
