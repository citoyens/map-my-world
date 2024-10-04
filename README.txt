# Map My World API

This project is a REST API for managing locations and categories, and providing exploration recommendations for 'Map My World'.

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/map-my-world-api.git
   cd map-my-world-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in a `.env` file:
   ```
   DATABASE_USERNAME=your_username
   DATABASE_PASSWORD=your_password
   DATABASE_HOST=your_host
   DATABASE_PORT=your_port
   DATABASE_NAME=your_database_name
   ```

## Running the Application

To run the application, use the following command:

```
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Running Tests

To run the tests, use the following command:

```
pytest
```

For more detailed output, use:

```
pytest -v
```

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
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.