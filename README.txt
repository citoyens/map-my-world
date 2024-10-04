# Map My World API

This project is a REST API for managing locations and categories, and providing exploration recommendations for 'Map My World'.

## Prerequisites

- Docker and Docker Compose
- (Optional for local development) Python 3.8+, pip, virtualenv, and PostgreSQL

## Setup with Docker

1. Clone the repository:
   ```
   git clone https://github.com/citoyens/map-my-world
   cd map-my-world
   ```

2. Create a `.env.test` file in the root directory with the following content:
   ```
   DATABASE_URL=postgresql://test_user:test_password@db:5432/test_db
   ```

3. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

This will start the PostgreSQL database and the application, and run the tests automatically.

## Local Setup (without Docker)

1. Follow steps 1-4 from the "Setup" section in the original README.

## Running the Application

### With Docker

The application runs automatically when you use `docker-compose up`. To run it separately:

```
docker-compose up db -d
docker-compose run --rm app uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Without Docker

```
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Running Tests

### With Docker

Tests run automatically when you use `docker-compose up`. To run them separately:

```
docker-compose down -v
docker-compose run --rm app pytest
```

### Without Docker

```
pytest
```

For more detailed output, use `pytest -v`.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Project Structure

```
map_my_world/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       ├── locations.py
│       ├── categories.py
│       ├── reviews.py
│       └── recommendations.py
├── tests/
│   ├── __init__.py
│   └── test_crud.py
├── .env
├── .env.test
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.