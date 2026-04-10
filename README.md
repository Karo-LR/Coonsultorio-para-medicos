# Consultorio Para Medicos - Local

Este proyecto quedo preparado para ejecutarse en entorno local, sin dependencias obligatorias de servicios en la nube.

## Cambios principales

- Backend configurado para base de datos local en `localhost` mediante variables `DB_*`.
- Eliminadas referencias por defecto a despliegues remotos.
- Frontend configurado para consumir `http://localhost:8000/api/`.
- Eliminada la integracion con Google reCAPTCHA del frontend.
- Correo configurado por defecto con backend de consola de Django para evitar SMTP externo.

## Dependencias necesarias

### Backend

- Python 3.12+
- PostgreSQL local
- Paquetes de `backend/requirements.txt`

Opcional:

- MySQL local si cambias `DB_ENGINE=mysql` y agregas un driver compatible como `mysqlclient`.

### Frontend

- Node.js 18+
- npm 9+

## Variables de entorno backend

Archivo: `backend/.env`

Valores locales por defecto:

```env
SECRET_KEY=dev-secret-key-local
DEBUG=True
ENABLE_SSL_REDIRECT=False
DB_ENGINE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=consultorio_db
DB_USER=postgres
DB_PASSWORD=postgres
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080,http://127.0.0.1:8080
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8080
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=no-reply@consultorio.local
```

## Base de datos local

### PostgreSQL

1. Crea la base:
   `CREATE DATABASE consultorio_db;`
2. Verifica que el usuario y password de `backend/.env` existan en tu instancia local.

### MySQL

1. Cambia `DB_ENGINE=mysql`
2. Cambia `DB_PORT=3306`
3. Ajusta `DB_NAME`, `DB_USER` y `DB_PASSWORD`
4. Instala un driver MySQL para Django, por ejemplo `mysqlclient`

## Como correr el backend

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createadmin
python manage.py runserver localhost:8000
```

## Como correr el frontend

```powershell
cd frontend
npm install
npm run serve
```

El frontend quedara disponible en `http://localhost:8080`.

## Funcionamiento offline

- La autenticacion JWT funciona localmente en el backend.
- El registro y login ya no dependen de Google reCAPTCHA.
- Los correos de activacion o recuperacion se imprimen en la consola del backend.
- La aplicacion no necesita AWS, S3, RDS ni endpoints externos para operar localmente.
