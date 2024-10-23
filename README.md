# kiwi_interview FastAPI Application
Private project for the purpose of solving the task from the interview. This is a minimal FastAPI application running inside a Docker container. The application provides basic endpoint with task functionality and can be easily run using Docker and Docker Compose.

## Features
- **FastAPI** for creating endpoint
- **Uvicorn** as the ASGI server
- **pytes** for code testing
- Dockerized for easy deployment and testing

## Requirements
Make sure you have the following installed on your system:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Structure
.  
├── Dockerfile  
├── docker-compose.yml  
├── main.py  
├── test_main.py  
├── requirements.txt  
└── README.md

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Build the Docker image
Run the following command to build the Docker image:

```bash
docker-compose build
```

### 3. Run the container
After the image is built, you can run the application using Docker Compose:

```bash
docker-compose up
```

The application will be available at http://localhost:8000.

### 4. Access API Endpoints by Openapi
Once the application is running, you can access the endpoints by openapi
- `GET /docs` - returns an Openapi documentation where you can find all available endpoints

### Stop the container

To stop the running container, use:

```bash
docker-compose down
```

## Running Tests
You can run the tests for the FastAPI application using Docker Compose.
Use the following command to run the tests inside the Docker container:

```bash
docker-compose run test
```