#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

# Firewall: instalar y definir reglas
apt-get install -y ufw
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow from 192.168.56.0/24 to any port 22 proto tcp
ufw allow from 192.168.56.0/24 to any port 80 proto tcp
ufw allow 22/tcp
ufw --force enable

# SSH: sin acceso directo de root
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
systemctl restart ssh

# Usuario estudiante: sin sudo
deluser estudiante sudo 2>/dev/null || true

echo "$(date) - seguridad OK" >> /var/log/fabrica.log
