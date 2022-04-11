# graphene-django-example

`graphene-django-extras` 에 대한 예제 프로젝트입니다.

## Installation

Python standard library 의 가상 환경 모듈인 [`venv`](https://docs.python.org/ko/3/library/venv.html) 를 이용하여 가상환경을 생성합니다:

```bash
python -m venv --upgrade-deps .venv
```

- `--upgrade-deps`: 핵심 종속성 업그레이드하기.

가상 환경 활성화하기:

```bash
source .venv/bin/activate
```

[`pip`](https://pip.pypa.io/en/stable/) 를 이용하여 필수 패키지 설치합니다:

```bash
python -m pip install -r requirements.txt
```

Django [`makemigrations`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#makemigrations) 명령어를 사용하여 _local app_ 들의 migrate 파일을 생성합니다:

```bash
python manage.py makemigrations ingredients
```

- `ingredients`: Local app.

Django [`migrate`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#migrate) 명령어를 사용하여 table 을 생성합니다:

```bash
python manage.py migrate
```

Django [`createsuperuser`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#createsuperuser) 명령어을 사용하여 _superuser_ 를 생성합니다:

```bash
python manage.py createsuperuser

# Username (leave blank to use 'user'): masteradmin
# Email address: 
# Password: 
# Password (again): 
# Superuser created successfully.
```

Django [`loaddata`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#loaddata) 명령어를 사용하여 _local app_ 들의 `fixtures` 디렉터리에 있는 `*.json` 파일을 불러온 후 데이터를 삽입합니다:

```bash
python manage.py loaddata ingredients
```

## Usage

### Runserver

Django [`runserver`](https://docs.djangoproject.com/en/4.0/ref/django-admin/#runserver) 명령어를 사용하여 서버를 시작합니다.

#### Runserver for Production

시작 전 `project/settings.py` 에서 아래 설정 값을 확인하십시오:

- `DEBUG`: 반드시 Production 은 `False` 입니다.
- `ALLOWED_HOSTS`: 접근 가능한 IP 가 포함되어 있는지 확인하십시오.

배포 가능한 설정으로 서버를 시작합니다:

```bash
python manage.py runserver 0.0.0.0:8000
```

#### Runserver for Development

_debug_ 가능한 설정으로 서버를 시작합니다:

```bash
python manage.py runserver --settings project.debug 0.0.0.0:8000
```

- `project.debug`: `project/settings.py` 에 debug 가능한 설정이 병합된 `project/debug.py` 입니다.

### Introspection Schema

작성된 모든 schema 를 `schema.graphql` 파일로 생성합니다:

```bash
python manage.py graphql_schema --out schema.graphql
```

Refer to [Introspection Schema](https://docs.graphene-python.org/projects/django/en/latest/introspection/#introspection-schema).

### Django Admin Web Page

Go to [Django Admin Page](http://0.0.0.0:8000/admin).

### GraphiQL API Web Page

Go to [GraphQL API Page](http://0.0.0.0:8000/graphql).
