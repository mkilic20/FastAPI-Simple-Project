# FastAPI Simple Project

This is a simple FastAPI project using Docker containers.

## Project Structure

- **client/**: Contains frontend code and static files.
- **db-service/**: Handles database-related services.
- **db/**: Contains database files.
- **testing.py**: Script for running tests.
- **docker-compose.yml**: Configuration file for Docker Compose.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mkilic20/FastAPI-Simple-Project.git
    cd FastAPI-Simple-Project
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

### Usage

Access the application at `http://localhost:8000`.

### Running Tests

Run the tests using the following command:
```bash
python testing.py
