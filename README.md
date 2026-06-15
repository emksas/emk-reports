# EMK Reports - Income microservice

Microservice built with Django REST Framework to query, create, update, and
delete incomes stored in a PostgreSQL database.

## Technologies

- Python 3.12+
- Django 6
- Django REST Framework
- PostgreSQL
- python-dotenv

## Main structure

```text
.
├── apps/
│   └── incomes/
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── Dockerfile
├── manage.py
├── requirements.txt
└── .env.example
```

## Environment variables

Create a `.env` file in the project root using `.env.example` as a base:

```env
ALLOWED_HOSTS=localhost,127.0.0.1,django
DB_CONNECTION=pgsql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=emk
DB_USERNAME=user
DB_PASSWORD=password
```

Django reads these variables from `config/settings.py` to connect to
PostgreSQL.

`ALLOWED_HOSTS` is a comma-separated list of hosts accepted by Django. When the
service runs inside Docker and other containers call it as `django:8084`, the
host `django` must be included.

## Local installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create the `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with the real PostgreSQL connection values.

4. Check the project configuration:

```bash
python manage.py check
```

5. Run the development server:

```bash
python manage.py runserver 0.0.0.0:8084
```

The service will be available at:

```text
http://localhost:8084/api/incomes/
```

## Running with Docker

Build the image:

```bash
docker build -t emk-reports .
```

Run the container using the `.env` file:

```bash
docker run --env-file .env -p 8084:8084 emk-reports
```

The service will be available at:

```text
http://localhost:8084/api/incomes/
```

## Data model

The `Income` model represents the existing `ingreso` table. This table is not
managed by Django because the model has `managed = False`.

Fields exposed by the API:

| Field | Type | Database column | Required |
| --- | --- | --- | --- |
| `id` | integer | `id` | automatic |
| `value` | decimal | `valor` | yes |
| `source` | string | `fuente` | no |
| `category` | string | `categoria` | no |
| `payment_method` | string | `metodo_de_pago` | no |
| `date` | datetime | `fecha` | yes |
| `reference` | string | `referencia` | no |
| `financial_planning_id` | integer | `planificacion_financiera_id` | no |
| `accounting_account_id` | integer | `cuentacontable_id` | no |
| `user_id` | integer | `user_id` | yes |

## Endpoints

All routes are under the `/api/` prefix.

| Action | Method | Route |
| --- | --- | --- |
| List incomes | `GET` | `/api/incomes/` |
| List incomes without API prefix | `GET` | `/incomes/` |
| Filter by user | `GET` | `/api/incomes/?user_id=<id>` |
| Filter by accounting account | `GET` | `/api/incomes/?account_id=<id>` |
| Filter by user and account | `GET` | `/api/incomes/?user_id=<id>&account_id=<id>` |
| Retrieve by id | `GET` | `/api/incomes/<id>/` |
| Create income | `POST` | `/api/incomes/` |
| Update by id | `PUT` | `/api/incomes/<id>/` |
| Partially update by id | `PATCH` | `/api/incomes/<id>/` |
| Delete by id | `DELETE` | `/api/incomes/<id>/` |
| Update by user and account | `PUT` | `/api/incomes/update-by-user-account/` |
| Delete by user and account | `DELETE` | `/api/incomes/delete-by-user-account/?user_id=<id>&account_id=<id>` |

The API accepts both trailing-slash and no-trailing-slash URLs. For example,
`/api/incomes/` and `/api/incomes` are both valid.

## Usage examples

Create an income:

```bash
curl -X POST http://localhost:8084/api/incomes/ \
  -H "Content-Type: application/json" \
  -d '{
    "value": "150000.00",
    "source": "Salary",
    "category": "Work",
    "payment_method": "Bank transfer",
    "date": "2026-06-14T10:00:00Z",
    "reference": "Monthly payment",
    "financial_planning_id": 1,
    "accounting_account_id": 2,
    "user_id": 5
  }'
```

List incomes for a user:

```bash
curl "http://localhost:8084/api/incomes/?user_id=5"
```

Update an income by user and account:

```bash
curl -X PUT http://localhost:8084/api/incomes/update-by-user-account/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 5,
    "account_id": 2,
    "value": "175000.00",
    "source": "Salary",
    "category": "Work",
    "payment_method": "Bank transfer",
    "date": "2026-06-14T10:00:00Z",
    "reference": "Adjusted payment",
    "financial_planning_id": 1,
    "accounting_account_id": 2
  }'
```

Delete by user and account:

```bash
curl -X DELETE "http://localhost:8084/api/incomes/delete-by-user-account/?user_id=5&account_id=2"
```

## Important responses

When listing incomes returns no results, the service responds with an empty
list:

```json
[]
```

and HTTP status `200`.

When no income exists for the user-and-account actions, the service responds
with:

```json
{
  "error": "No encontrado"
}
```

and HTTP status `404`.

## Development notes

- The `ingreso` table must already exist in PostgreSQL.
- Because `Income.managed = False`, Django does not create or modify this table
  through migrations.
- The `/admin/` endpoint exists because of the base Django configuration.
- In development, use `python manage.py runserver`; in Docker, the container
  runs the server on port `8084`.
