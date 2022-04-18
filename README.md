## FastAPI Boilerplate [PostgreSQL]

### Features
* Database support with PostgreSQL
* Async query with SQLAlchemy ORM
* Migration management with alembic
* A better directory structure
* Tests setup with pytest
* Testing with a real database along with setup and tear down approch
* Celery worker support (celery beat can be configured easily.)
* Repository based ORM writing for better abstraction

### How to run [Docker & Docker Compose]
* Copy the `.env.example` and create `.env` file.
* `$ docker-compose up --build -d`
* Create databases by logging into the container of db. Use the following commands
```
$ docker-compose exec backend sh

# su - postgres
$ psql
# CREATE DATABASE "fastapi_boilerplate";
# CREATE DATABASE "fastapi_boilerplate_test_db";
# \password
Enter new password for user postgres: *****
```
* Again re run the `$ docker-compose up --build -d`
* To run the tests run the following command,
```sh
$ docker-compose exec backend sh
# You will be logged in to the container shell. Then,
$ pytest
```

### How to run [Without Docker]
* Copy the `.env.example` and create `.env` file.
* Create a virtualenv and activate it.
* Install requirements `pip install -r requirements.txt`
* Create database from psql shell.
* Run the Server `$ uvicorn main:app --reload --port 7001`
* Run celery `$ python -m celery -A core.celery worker -l INFO`
* Run the tests `$ pytest`

### Contributing Guide
* Found something? Create an issue on this repository.
* Fork this repo.
* Work on it. Push it on your forked.
* Make a PR with Upstream(this repo)  

**Contributors are most welcome**