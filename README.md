# graphene-django-extras-example

`graphene-django-extras` 에 대한 예제 프로젝트입니다.

## Installation

Make migrate files:

```bash
python manage.py makemigrations ingredients
```

- [`makemigrations`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#makemigrations): Make migrate file.
- `ingredients`: Local app.

Migrate:

```bash
python manage.py migrate
```

- [`migrate`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#migrate)

Create super user:

```bash
python manage.py createsuperuser

# Username (leave blank to use 'user'): masteradmin
# Email address: 
# Password: 
# Password (again): 
# Superuser created successfully.
```

- [`createsuperuser`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#createsuperuser)

Load data:

```bash
python manage.py loaddata ingredients
```

- [`loaddata`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#loaddata)

Run server:

```bash
python manage.py runserver --settings project.debug 0.0.0.0:8000
```

- [`runserver`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#runserver)
- [`--settings`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#cmdoption-settings): 사용할 설정 모듈을 지정합니다.
- `project.debug`: `project/debug.py` 을 의미합니다.

## Usage

### Django Admin Web Page

Django Admin 이용하기.

URL: `http://0.0.0.0:8000/admin`

### GraphiQL API Web Page

GraphQL API 질의를 할 수 있는 Web Page 이용하기.

URL: `http://0.0.0.0:8000/graphql`
