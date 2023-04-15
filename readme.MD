# ProxyRequest

## Summary

* Proxy your http request to and from wherever you want
* Safely share your key with other users
    * Quota / User (soon)

## How it works

This application allows you to share your api key between several users.
The application is supposed to be self-hosted.
The person doing the installation fills in his admin IDs using the environment
and creates the accesses for other users with the admin interface (/admin).

### Endpoints

The users have access to :

- an url to get token using username/password /api/login;
- an url to send a request using the shared api key /api/call (protected)
- url to view the history of requests sent /api/logs (protected)
- url to get current quota /api/stats/quota (protected)

### Logs

The proxied requests are logged.
The log contains the headers, the body, the response and other info.

### Quota

Admin can set global quota. How users reach or exceed this value is compute using the log.
Default: every request made by a user counts 1, whether the request is completed or not.

### Authentification

Authentication to this api is done with bearer token.
Token validity can be changed.

The authentication to the final server currently supports only bearer.

### Files

Files can be sent. Using multiform. Concerned keys must start with "files_".
The following parts will be used in the request.
So if you have:
files_file_key_1: ArrayOfFiles
files_file_key_2: ArrayOfFiles
key_3: ArrayOfFiles
the request sent by this app will contain files: `{"file_key_1": <>, "file_key_2": <>}`

FIles are not stored with logs.

## First steps

a) Retrieve

b) Dependencies

```bash
poetry install
```

c) Db migrations

```bash
python manage.py migrate
```

d) Start

```bash
python manage.py runserver
```

## env

```pre
MODE=dev 
DJANGO_SECRET_KEY=SECRET # replace with your secret key
ALLOWED_HOSTS=*

#
USE_SQLITE= # True if "1" else False

# PSQL database (irrelevant if USE_SQLITE)
DB_USER=
DB_NAME=
DB_HOST=
DB_PORT=
DB_PASSWORD=

CORS_ALLOWED_ORIGINS=

# Admin page access

DEFAULT_ADMIN_USERNAME=
DEFAULT_ADMIN_EMAIL=
DEFAULT_ADMIN_PASSWORD=

SHARED_KEY= # replace with your api key

QUOTA_GLOBAL_MAX_REQUEST_COUNT = 
QUOTA_EXCLUDED_STATUS_CODE = 
QUOTA_INCLUDED_STATUS_CODE = 
QUOTA_EXCLUDED_INCOMPLETE_REQUEST = 
QUOTA_MODE =

# Unused yet
EMAIL_USE_TLS=
EMAIL_PORT=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
```

## Docker

docker/proxy_default.conf -> "example.app" should be changed

## todo:

* add some tests (welp)