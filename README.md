![made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)

# JustAskIt

JustAskIt is the Django backend for a Q&A web application where users can ask questions, post answers, follow other users, vote on answers, and comment. The API is built with Django REST Framework and is ready for deployment (example: Heroku + Gunicorn). The project includes JWT-based authentication, email password reset via SendGrid, and Postman documentation.

Live demo (example): https://justaskit.herokuapp.com/ (if deployed)

Postman docs: https://documenter.getpostman.com/view/14121536/UVJWqKYy

**Tech stack & key dependencies**
- Python + Django (Django==4.2)
- Django REST Framework
- PostgreSQL (production), SQLite (development)
- Gunicorn, WhiteNoise (static serving)
- python-decouple, dj-database-url, django-heroku, sendgrid

See `requirements.txt` for the full dependency list.

## Features
- Ask and answer questions
- Follow users
- Upvote / downvote answers
- Comment on answers
- JWT authentication and password reset via SendGrid

## Environment variables
Create a `.env` file in the project root (the project uses `python-decouple`). The following variables are expected:

- `SECRET_KEY` — Django secret key
- `ENVIRONMENT` — `development` or `production` (controls database selection)
- `DATABASE_URL` — Production Postgres URL (used when `ENVIRONMENT=production`)
- `ACCESS_SECRET_TOKEN` — secret used for generating JWTs
- `BCRYPT_SALT` — bcrypt salt rounds or value used for hashing
- `SENDGRID_API_KEY` — SendGrid API key (for password reset emails)
- `PASSWORD_RESET_EMAIL_TEMPLATE_ID` — SendGrid template id for reset emails
- `FROM_EMAIL` — sender email for outgoing emails

## Quickstart (development)
1. Clone the repo
2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file with the variables above (at minimum `SECRET_KEY` and `ENVIRONMENT=development`).
4. Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

5. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

## Running tests
Run Django tests with:

```bash
python manage.py test
```

## Production notes
- `Procfile` is included for Heroku deployments. Use `gunicorn justaskit.wsgi` to run the app in production.
- `dj-database-url` and `django-heroku` are enabled in `justaskit/settings.py` to simplify Heroku setup.

## Project structure (important files)
- `manage.py` — Django command-line utility
- `requirements.txt` — pinned dependencies
- `justaskit/settings.py` — Django settings (env-driven)
- `justaskit/urls.py` — root URL config
- `api/` — main API package
  - `api/user`, `api/question`, `api/answer`, `api/comment` — app packages with views/serializers/models
- `templates/` — HTML templates (e.g., index)
- `Procfile` — Heroku process file

## Database models
This section documents the main database models used by the application and the important fields on each model.

- **EndUser**: users of the system
  - `name` (CharField)
  - `email` (CharField, unique)
  - `phone` (CharField)
  - `password` (CharField, hashed)
  - `description` (CharField)
  - `profile_image` (CharField, optional)
  - `created_at`, `updated_at` (DateTimeFields)

- **Location**: user location entries
  - `user` (ForeignKey -> EndUser)
  - `location` (CharField)
  - `start_year`, `end_year` (DateFields)

- **Education**: user education entries
  - `user` (ForeignKey -> EndUser)
  - `school` (CharField)
  - `degree_type` (CharField)
  - `graduation_year` (DateField, optional)

- **Employment**: user employment entries
  - `user` (ForeignKey -> EndUser)
  - `position` (CharField)
  - `company` (CharField)
  - `start_year`, `end_year` (DateFields)

- **Follow**: follower / followee relationship
  - `follower` (ForeignKey -> EndUser)
  - `followee` (ForeignKey -> EndUser)
  - `created_at`, `updated_at` (DateTimeFields)

- **Token**: auth tokens for password reset / sessions
  - `user` (ForeignKey -> EndUser)
  - `token` (CharField)
  - `created_at`, `updated_at` (DateTimeFields)

- **Question**: questions posted by users
  - `question` (CharField)
  - `ask_type` (CharField, choices: public/private)
  - `owner` (ForeignKey -> EndUser)
  - `created_at`, `updated_at` (DateTimeFields)

- **Answer**: answers to questions
  - `answer` (CharField)
  - `question` (ForeignKey -> Question)
  - `owner` (ForeignKey -> EndUser)
  - `created_at`, `updated_at` (DateTimeFields)

- **AnswerVote**: votes on answers
  - `answer` (ForeignKey -> Answer)
  - `voter` (ForeignKey -> EndUser)
  - `vote_type` (CharField, choices: up/down)
  - `created_at`, `updated_at` (DateTimeFields)

- **Comment**: comments on answers (supports threaded comments)
  - `owner` (ForeignKey -> EndUser)
  - `answer` (ForeignKey -> Answer, optional)
  - `comment` (self-referential ForeignKey, optional)
  - `comment_text` (CharField)
  - `created_at`, `updated_at` (DateTimeFields)

- **CommentVote**: votes on comments
  - `comment` (ForeignKey -> Comment)
  - `voter` (ForeignKey -> EndUser)
  - `vote_type` (CharField, choices: up/down)
  - `created_at`, `updated_at` (DateTimeFields)

## Contributing
- Fork, create a feature branch, and open a PR with clear description and tests where applicable.

## License
This project includes a `LICENSE` file in the repository.

If you want, I can also:
- add example `.env` file template
- generate an OpenAPI schema or README API examples
- run the test suite and report failures
