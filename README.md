FastAPI User Auth with Postgres and Docker

This project is a simple example of FastAPI authentication with a PostgreSQL database using Docker.
🧰 Tech Stack

    Python 3.12

    FastAPI

    SQLAlchemy

    Alembic

    asyncpg

    Docker

    Docker Compose

🚀 Installation
1. Clone the repository:

git clone https://github.com/your_username/your_repository.git
cd your_repository

2. Create a .env file in the root directory with the following content:

NAME_OF_USER=your_postgres_username
PASSWORD_OF_USER=your_postgres_password
DATABASE_NAME=your_database_name

3. Build and run the project with Docker:

docker-compose up --build

4. In a new terminal, open the container’s shell:

docker exec -it fastapi_app sh

    Note: Make sure the service name (fastapi_app) matches the one in your docker-compose.yml.

5. Inside the container, apply database migrations:

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

✅ Done!

Visit the automatic docs at:

🔗 http://127.0.0.1:8000/docs
📝 Notes

    Make sure PostgreSQL is ready before running Alembic commands.

    This setup uses async SQLAlchemy with asyncpg driver.
