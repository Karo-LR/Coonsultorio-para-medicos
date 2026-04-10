# Despliegue en AWS Academy

Esta carpeta deja el proyecto listo para una arquitectura con:

- Frontend en una EC2 Ubuntu
- Backend en una EC2 Ubuntu
- Base de datos en red privada
- ALB al frente
- AWS WAF asociado al ALB
- UFW + Fail2Ban en las instancias

## Hallazgos y correcciones en el código

### 1. `DB_HOST` estaba hardcodeado

Antes el backend usaba una IP privada por defecto (`10.0.4.31`) en `settings.py`.

Problema:

- Acopla el proyecto a una sola red
- Puede conectar al host equivocado
- Rompe la configuración por entorno

Corrección:

- Ahora el default volvió a `localhost`
- Para AWS debes usar `backend/.env.aws.example`

### 2. El frontend estaba amarrado a `localhost`

Antes el frontend consumía `http://localhost:8000/api/` como valor por defecto.

Problema:

- En producción, el navegador del usuario intentaría consumir su propia máquina local
- Te obliga a pelear con CORS innecesariamente

Corrección:

- En producción ahora usa `window.location.origin + /api/`
- Esto permite servir frontend y backend detrás del mismo ALB con routing por path

### 3. Faltaba configuración para HTTPS detrás de ALB

Corrección:

- Se agregó soporte para `CSRF_TRUSTED_ORIGINS`
- Si `ENABLE_SSL_REDIRECT=True`, Django respeta `X-Forwarded-Proto`

## Arquitectura recomendada

### Red

- VPC: `10.0.0.0/16`
- Subredes públicas:
  - `10.0.1.0/24` ALB-A
  - `10.0.2.0/24` ALB-B
- Subredes privadas:
  - `10.0.3.0/24` Frontend/Backend
  - `10.0.4.0/24` Base de datos

Si tu profesor pide 2 privadas para EC2 y EC2, puedes usar:

- `10.0.3.0/24` Frontend privada
- `10.0.4.0/24` Backend privada
- Y una subred privada adicional para RDS si tu práctica lo permite

## Seguridad recomendada

### Security Groups

#### `sg-alb`

- Inbound `80` desde `0.0.0.0/0`
- Inbound `443` desde `0.0.0.0/0`
- Outbound a `sg-frontend` y `sg-backend`

#### `sg-frontend`

- Inbound `80` solo desde `sg-alb`
- Inbound `22` solo desde tu IP o deshabilitado si no usarás SSH

#### `sg-backend`

- Inbound `80` solo desde `sg-alb`
- Inbound `22` solo desde tu IP o deshabilitado si no usarás SSH
- Outbound `5432` hacia `sg-db`

#### `sg-db`

- Inbound `5432` solo desde `sg-backend`
- Sin acceso público

## ALB

Usa un solo ALB con reglas:

- `/api/*` -> Target group backend
- `/admin/*` -> Target group backend
- `/*` -> Target group frontend

Esto simplifica:

- DNS
- Certificados
- CORS
- Integración con WAF

## AWS WAF

Asocia el Web ACL al ALB y empieza probando reglas administradas en modo de conteo antes de bloquear tráfico real.

Reglas recomendadas:

- `AWSManagedRulesCommonRuleSet`
- `AWSManagedRulesKnownBadInputsRuleSet`
- `AWSManagedRulesSQLiRuleSet`
- `AWSManagedRulesLinuxRuleSet`

## User Data

Archivos listos:

- `deploy/aws/backend-user-data.sh`
- `deploy/aws/frontend-user-data.sh`

Antes de usarlos cambia:

- `REPO_URL`
- `BRANCH`
- dominios en `.env`
- credenciales de base de datos

## Variables para backend en AWS

Usa `backend/.env.aws.example` como plantilla.

## Variables para frontend en AWS

Usa `frontend/.env.production.example`:

```env
VUE_APP_API_URL=/api/
```

## Flujo recomendado de implementación

1. Crear VPC, subredes, IGW y NAT Gateway.
2. Crear Security Groups por capa.
3. Crear la base de datos privada.
4. Lanzar EC2 frontend y backend en subredes privadas con User Data.
5. Crear ALB en subredes públicas.
6. Asociar target groups al ALB.
7. Configurar WAF sobre el ALB.
8. Configurar Route 53 o DNS del proveedor hacia el ALB.

## Validaciones finales

- Frontend accesible solo por ALB
- Backend no expuesto directamente a internet
- Base de datos accesible solo desde backend
- UFW activo en frontend y backend
- Fail2Ban activo
- HTTPS en ALB
- WAF asociado al ALB
