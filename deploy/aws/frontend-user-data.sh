#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

APP_DIR=/opt/consultorio-app
REPO_URL="https://github.com/Karo-LR/Coonsultorio-para-medicos.git"
BRANCH="main"

apt-get update
apt-get install -y git nginx curl ufw fail2ban

curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

if [ ! -d "$APP_DIR/.git" ]; then
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
else
  git -C "$APP_DIR" fetch origin
  git -C "$APP_DIR" checkout "$BRANCH"
  git -C "$APP_DIR" pull --ff-only origin "$BRANCH"
fi

cd "$APP_DIR/frontend"
cp -n .env.production.example .env.production || true
npm ci
npm run build

rm -rf /var/www/consultorio-frontend
mkdir -p /var/www/consultorio-frontend
cp -r dist/* /var/www/consultorio-frontend/

cat >/etc/nginx/sites-available/consultorio-frontend <<'EOF'
server {
    listen 80 default_server;
    server_name _;

    root /var/www/consultorio-frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
EOF

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/consultorio-frontend /etc/nginx/sites-enabled/consultorio-frontend

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
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw --force enable

systemctl enable nginx fail2ban
systemctl restart nginx
systemctl restart fail2ban
