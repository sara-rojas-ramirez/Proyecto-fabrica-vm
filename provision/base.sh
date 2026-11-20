#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

timedatectl set-timezone America/Bogota

apt-get update -y
if [ $# -gt 0 ]; then
  apt-get install -y "$@"
fi

id estudiante &>/dev/null || useradd -m -s /bin/bash estudiante
echo "estudiante:Lab2026*" | chpasswd

systemctl enable --now ssh

echo "$(date) - aprovisionamiento OK" >> /var/log/fabrica.log
