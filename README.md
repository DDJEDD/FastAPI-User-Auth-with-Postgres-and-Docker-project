# FastAPI User Authentication with PostgreSQL and Docker

This project demonstrates a simple user authentication system built with FastAPI, PostgreSQL, and Docker.

## 🧰 Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- asyncpg
- Docker
- Docker Compose

## 🚀 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/DDJEDD/FastAPI-User-Auth-with-Postgres-and-Docker-project
   cd FastAPI-User-Auth-with-Postgres-and-Docker-project
   ```
2.** Create a .env file in the root directory with the following content**:
```bash
NAME_OF_USER=your_postgres_username
PASSWORD_OF_USER=your_postgres_password
DATABASE_NAME=your_database_name
SECRET_KEY=your_secret_key_for_JWT
```
3.**Build and run the project with Docker**:
```bash
docker-compose up --build
```
4.**In a new terminal, open the container’s shell**:
```bash
docker exec -it fastapi_app sh
```
Note: Ensure the service name (fastapi_app) matches the one defined in your docker-compose.yml.
5.**Inside the container, apply database migrations**:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
## ✅ Done!

Visit the automatic API documentation at:
🔗 http://127.0.0.1:8000/docs

## 📝 Notes

Ensure PostgreSQL is fully initialized before running Alembic commands.
This setup uses async SQLAlchemy with the asyncpg driver for PostgreSQL.
