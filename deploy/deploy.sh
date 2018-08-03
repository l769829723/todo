#!/usr/bin/env bash

# Render hosts file
cat >hosts<<EOF
app_server ansible_host=${SERVER_ADDRESS} ansible_ssh_pass=${SERVER_PASSWORD} ansible_user=${SERVER_USERNAME}
EOF

# Execute deploy
# ansible-playbook deploy.yaml
ansible localhost -m ping

# Done