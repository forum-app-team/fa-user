# User Microservice

## Notes
The model `app/models/User.py` includes commented-out relationship stubs for posts, replies, histories, and messages. I leave them out for out since I have not thoroughly examine the keys from those services 

**If you think the namings are correct for any model from the service you work on, feel free to uncomment the corresponding lines.**

## Features


## Configuration
### Environment Files
+ `.env`
Create a `.env` file locally with the following variables:
```
DATABASE_NAME=forum_app
DATABASE_SOCKET=/tmp/mysql.sock
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=localhost
DATABASE_MANAGED_TABLES=users

RABBITMQ_URL=amqp://guest:guest@localhost:5672/

RABBITMQ_EXCHANGE=user_exchange
RABBITMQ_EXCHANGE_TYPE=direct
RABBITMQ_ROUTING_KEY=user.created

RABBITMQ_FAILURE_EXCHANGE=failure_exchange
RABBITMQ_FAILURE_EXCHANGE_TYPE=direct
RABBITMQ_FAILURE_ROUTING_KEY=user.failed

JWT_ACCESS_SECRET=
```

or simply run `$ cp .env.example .env`

+ `.flaskenv`
Create a `.flaskenv` file locally with the following variables:
```
FLASK_APP=app.py
FLASK_RUN_HOST=localhost
FLASK_RUN_PORT=5002
```

### DB Setup & Migration
+ Initial Setup (Not needed if repo is pulled from remote)
```bash
$ flask db init
$ flask db migrate -m "message"
$ flask db upgrade
```

+ After pulling this repository:
```bash
$ flask db upgrade
```

+ Undo the most recent migration:
```bash
$ flask db downgrade
```

+ Undo all migrations:
```bash
$ flask db downgrade base
```

## Run the Microservice
+ The main application:
```bash
$ flask run
```

+ The worker that consumes message from AUTH service:
```bash
$ flask worker
```

## API Endpoints
### Endpoints and Explanation
| Endpoint             | Method | Auth Required | Description                                  | Request Body Params (JSON)                   |
| -------------------- | ------ | ------------- | -------------------------------------------- | -------------------------------------------- |
| `/profile/me`        | GET    | YES           | Get the authenticated user’s profile         | N/A                                          |
| `/profile/<user_id>` | GET    | YES           | Get a specific user’s profile (or `"me"`)    | N/A                                          |
| `/profile/<user_id>` | PATCH  | YES           | Update the authenticated user’s profile only | `first_name`, `last_name`, `profile_img_url` |



### Success & Error Responses
| Endpoint             | Method | Success (200) Example                                                     | Possible Errors                                                                                           |
| -------------------- | ------ | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `/profile/me`        | GET    | `{ "message": "Successfully acquired user profile", "profile": { ... } }` | `401 Unauthorized`, `404 Not Found`                                                                       |
| `/profile/<user_id>` | GET    | `{ "message": "Successfully acquired user profile", "profile": { ... } }` | `401 Unauthorized`, `404 Not Found`                                                                       |
| `/profile/<user_id>` | PATCH  | `{ "message": "Successfully updated user profile", "profile": { ... } }`  | `400 Bad Request` (no changes), `403 Forbidden` (cannot edit others), `404 Not Found`, `401 Unauthorized` |


## Database
### Models
+ User Model:

| Column              | Type          | Constraints                              | Description                                                        |
| ------------------- | ------------- | ---------------------------------------- | ------------------------------------------------------------------ |
| `id`                | `String(36)`  | **PK**, auto-generated UUID              | Internal primary key for the `users` table                         |
| `user_id`           | `CHAR(36)`    | **FK → identities.id**, unique, not null | Links this user to their **Identity** record from the auth service |
| `first_name`        | `String(50)`  | not null                                 | User’s first name                                                  |
| `last_name`         | `String(50)`  | not null                                 | User’s last name                                                   |
| `date_joined`       | `DateTime`    | server default = `NOW()`                 | Timestamp when the user was created                                |
| `profile_image_url` | `String(256)` | nullable                                 | URL of the user’s profile image (if provided)                      |




## Project Structure
```
fa-user
├── app/
│   ├── __init__.py
│   ├── middleware/
│   │   ├── jwt_middleware.py
│   │   └── validate_input_middleware.py
│   ├── models/
│   │   ├── relationships.py
│   │   └── User.py
│   └── profile/
│       ├── __init__.py
│       ├── consumer.py
│       ├── producer.py
│       ├── routes.py
│       ├── utils.py
│       └── views.py
├── app.py
├── config.py
├── migrations/
├── .env
├── .flaskenv
├── requirements.txt
└── readme.md
```

## Getting Started
+ Prerequisites:
    - Python (Built on 3.13)
    - MySQL Database, with credentials stored in `.env`
+ Clone this repository
+ Create and activate your virtual environment
+ `$ pip install -r requirements.txt`
+ [Optional] Verify installation: `$ pip list`



## Miscellaneous

