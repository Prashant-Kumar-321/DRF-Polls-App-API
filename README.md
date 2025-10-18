# Polls API (pollsAppApi)
This is a Polls Application APIs
Simple Django + DRF project that implements polls, choices and votes.

## Requirements
- Python 3.10+ (or your environment's interpreter)
- Django (as used in this workspace)
- djangorestframework

## Setup (development)
1. Create and activate virtualenv, then install dependencies (example):

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Apply migrations:
```sh
python manage.py migrate
```
3. (Optional) Create a superuser:
```sh
python manage.py createsuperuser
```
4. Run dev server:
```sh
python manage.py runserver
```

## API Endpoints
All API routes are under ```/api/``` (see pollsAppApi/urls.py).

### Main endpoints (declared in polls/urls.py):
**Polls:**

    GET: /api/polls/ — list polls

    POST: /api/polls/ — create poll

    GET: /api/polls/<pk>/ — retrieve poll

    PUT: /api/polls/<pk>/ — update poll

    DELETE /api/polls/<pk>/ — delete poll

**Choices:**

    GET /api/polls/<poll_pk>/choices/ — list choices (polls.views.ChoicesList)

    POST /api/polls/<poll_pk>/choices/ — create a choice

    GET /api/polls/<poll_pk>/choices/<choice_pk>/ — retrieve choice (polls.views.
    ChoiceDetail)

    PUT /api/polls/<poll_pk>/choices/<choice_pk>/ — update choice

    DELETE /api/polls/<poll_pk>/choices/<choice_pk>/ — delete choice

**Voting:**

    POST /api/polls/<poll_pk>/choices/<choice_pk>/vote/ — create or replace a vote 
