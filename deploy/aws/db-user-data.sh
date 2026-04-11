#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

DB_NAME="consultorio_db"
DB_USER="postgres"
DB_PASSWORD="cambia-esta-password"
DB_ALLOWED_CIDR="10.0.3.0/24"
PG_VERSION="16"

apt-get update
apt-get install -y postgresql postgresql-contrib ufw fail2ban

PG_CONF="/etc/postgresql/${PG_VERSION}/main/postgresql.conf"
PG_HBA="/etc/postgresql/${PG_VERSION}/main/pg_hba.conf"

sed -i "s/^#listen_addresses =.*/listen_addresses = '*'/" "$PG_CONF"
sed -i "s/^listen_addresses =.*/listen_addresses = '*'/" "$PG_CONF"

if ! grep -q "^host[[:space:]]\+all[[:space:]]\+all[[:space:]]\+${DB_ALLOWED_CIDR}[[:space:]]\+md5" "$PG_HBA"; then
  echo "host all all ${DB_ALLOWED_CIDR} md5" >> "$PG_HBA"
fi

systemctl enable postgresql
systemctl restart postgresql

sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname = '${DB_USER}'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname = '${DB_NAME}'" | grep -q 1 || \
  sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

sudo -u postgres psql -c "ALTER USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"

cat >/etc/fail2ban/jail.d/sshd.local <<'EOF'
[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = systemd
maxretry = 5
bantime = 1h
findtime = 10m
EOF

ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow from 10.0.3.0/24 to any port 5432 proto tcp
ufw allow 22/tcp
ufw --force enable

systemctl enable fail2ban
systemctl restart fail2ban
