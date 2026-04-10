#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

APP_USER=ubuntu
APP_DIR=/opt/consultorio-app
REPO_URL="https://github.com/tu-usuario/tu-repo.git"
BRANCH="main"
PYTHON_BIN=python3
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

apt-get update
apt-get install -y git nginx python3 python3-venv python3-pip postgresql-client ufw fail2ban

if [ ! -d "$APP_DIR/.git" ]; then
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
else
  git -C "$APP_DIR" fetch origin
  git -C "$APP_DIR" checkout "$BRANCH"
  git -C "$APP_DIR" pull --ff-only origin "$BRANCH"
fi

cd "$APP_DIR/backend"
$PYTHON_BIN -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

cp -n .env.aws.example .env || true

./venv/bin/python manage.py migrate
./venv/bin/python manage.py collectstatic --noinput

cat >/etc/systemd/system/consultorio-backend.service <<'EOF'
[Unit]
Description=Consultorio Django Backend
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/opt/consultorio-app/backend
EnvironmentFile=/opt/consultorio-app/backend/.env
ExecStart=/opt/consultorio-app/backend/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 3 --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

cat >/etc/nginx/sites-available/consultorio-backend <<'EOF'
server {
    listen 80 default_server;
    server_name _;

    client_max_body_size 20M;

    location /static/ {
        alias /opt/consultorio-app/backend/staticfiles/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120;
    }
}
EOF

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/consultorio-backend /etc/nginx/sites-enabled/consultorio-backend

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

systemctl daemon-reload
systemctl enable consultorio-backend nginx fail2ban
systemctl restart consultorio-backend
systemctl restart nginx
systemctl restart fail2ban

chown -R "$APP_USER":www-data "$APP_DIR"
