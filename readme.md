# User Microservice

## Features

## API Endpoints

## Project Structure

## Getting Started

## Configuration
### .env
Create a `.env` file locally with the following variables:
```
DATABASE_NAME=forum_app
DATABASE_SOCKET=/tmp/mysql.sock
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=localhost
```

### .flaskenv
Create a `.flaskenv` file locally with the following variables:
```
FLASK_APP=app.py
FLASK_RUN_HOST=localhost
FLASK_RUN_PORT=5002
```

### Database
```bash
$ flask db init
$ flask db migrate -m "message"
$ flask db upgrade
```

## Miscellaneous

