# Code Challenge

This project is a Dockerized Django application with a PostgreSQL database. Follow the steps below to set up and run the project.

## Prerequisites

- Docker
- Docker Compose


## Setup

1. Clone the repository:
   
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   
   ```bash
   cd <project-directory>
   ```

3. Create a `.env` file based on the structure of `.env.example`:
   
   ```bash
   cp .env.example .env
   ```

   Update the `.env` file with your desired configurations.


## Running the Project

1. Start the Docker containers:

   ```bash
   docker-compose up -d
   ```

2. Create a superuser (if needed):

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

4. Access the application at `http://localhost:8000`.


## Running Tests

- To run tests, execute the following command:

   ```bash
   docker-compose exec web pytest
   ```

## Stopping the Project

- To stop the Docker containers, run:

   ```bash
   docker-compose down
   ```

## Documentation

- The Swagger documentation is available at `http://localhost:8000/swagger/`.
