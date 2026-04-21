# FastAPI Calculator API with JWT Authentication

A robust, secure backend calculator application built with FastAPI. This project features user registration, JWT-based authentication, and a fully tested API for mathematical operations. It is containerized using Docker and includes a complete CI/CD pipeline using GitHub Actions, Trivy security scanning, and Playwright end-to-end testing.

## 🚀 Features
* **User Authentication:** Secure registration and login using JSON Web Tokens (JWT) and password hashing (bcrypt).
* **Calculator API:** Perform addition, subtraction, multiplication, and division operations.
* **History Tracking:** All calculations are saved to the database and tied to the authenticated user.
* **Full E2E Testing:** Automated UI/API testing using Playwright and Pytest.
* **CI/CD Pipeline:** Automated testing, Trivy vulnerability scanning, and deployment to Docker Hub via GitHub Actions.
* **Containerized:** Fully reproducible environments using Docker and Docker Compose.

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Database:** PostgreSQL (via SQLAlchemy ORM)
* **Testing:** Pytest, Playwright (E2E), Pytest-cov
* **DevOps:** Docker, Docker Compose, GitHub Actions, Trivy

## 🐳 Running the Application Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Reyesfrancisp/client_side.git](https://github.com/Reyesfrancisp/client_side.git)
   cd client_side
   ```

2. **Build and start the containers:**
   ```bash
   docker-compose up -d --build
   ```

3. **Access the application:**
   * API Documentation (Swagger UI): `http://localhost:8000/docs`
   * Health Check: `http://localhost:8000/health`

## 🧪 Running the Tests

To run the full test suite (including the Playwright E2E tests) inside the Docker container:

```bash
docker-compose exec web pytest tests/e2e/ -v
```

## 🔒 Security

This repository utilizes an automated DevSecOps pipeline. Upon every push to the `main` branch, GitHub Actions builds the Docker image and scans it for vulnerabilities using **Trivy**. Known unpatchable vulnerabilities (e.g., specific `pyasn1` conflicts required by legacy auth libraries) are managed via a `.trivyignore` policy file.