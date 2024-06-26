# BOOK STORE WITH PYTHON FLASK

## Introduction
- TBD
## Want to explore?
### Clone the source code
    > git clone https://github.com/sieunhantanbao/book-store.git
    > cd book-store
### Run the app from the source code
Note: Make sure you have installed the [Python](https://www.python.org/downloads/)
#### Install [`virtualenv`](https://flask.palletsprojects.com/en/3.0.x/installation/#virtual-environments)
    > py -3 -m venv .venv
    > .venv\Scripts\activate
    
#### Install the packages
    > pip install -r requirements.txt

#### Rename the .sample.env to .env and update the configuration
    APP_SECRET_KEY='myrandomuntellsecret'
    REDIS_HOST=127.0.0.1
    REDIS_PORT=6379
    UPLOAD_FOLDER='static/files_uploaded'
    ALLOWED_EXTENSIONS={'pdf','png','jpg','jpeg','gif'}
    DB_ENGINE=postgresql
    DB_HOST=127.0.0.1
    DB_USERNAME=postgresql
    DB_PASSWORD=postgresql
    DB_PORT=5432
    DB_NAME=book_store.db
    DEFAULT_ADMIN_PASSWORD=12345678
    JWT_SECRET=
    JWT_ALGORITHM=HS256

#### Run the data migration
    > alembic upgrade head

#### Run the app
    > python main.py

#### Viewing the app
Open the following url on your browser [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

### Run the app with Docker Compose
Make sure you have installed the [Docker Compose](https://docs.docker.com/compose/install/)

#### Rename the .sample.env to .env and update the configuration
    APP_SECRET_KEY='myrandomuntellsecret'
    UPLOAD_FOLDER='static/files_uploaded'
    ALLOWED_EXTENSIONS={'pdf','png','jpg','jpeg','gif'}
    DB_ENGINE=postgresql
    DB_USERNAME=postgresql
    DB_PASSWORD=postgresql
    DB_NAME=book_store.db
    DEFAULT_ADMIN_PASSWORD=12345678
    JWT_SECRET=
    JWT_ALGORITHM=HS256
#### Run the app
    > docker-compose up

### Viewing the app
Open the following url on your browser [http://127.0.0.1:5001/](http://127.0.0.1:5001/)

