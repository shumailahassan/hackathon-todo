# Quick Start Guide: Web Application Conversion

## Overview
This guide provides a quick start for setting up and running the multi-user web application with persistent storage.

## Prerequisites
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Docker and Docker Compose (for containerized deployment)

## Development Setup

### 1. Clone and Initialize
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Configuration
Copy the example environment files and configure your settings:

```bash
# Backend
cp .env.example backend/.env
# Update backend/.env with your database and authentication settings

# Frontend
cp .env.example frontend/.env
# Update frontend/.env with your API endpoint and authentication settings
```

### 5. Database Setup
```bash
cd backend
# Run database migrations
alembic upgrade head
```

## Running Locally

### Development Mode
Start the backend:
```bash
cd backend
python -m uvicorn main:app --reload
```

Start the frontend:
```bash
cd frontend
npm run dev
```

### With Docker
```bash
docker-compose up --build
```

## Key Endpoints

### API Base URL
- Development: `http://localhost:8000/v1`
- Production: `<your-domain>/v1`

### Authentication Endpoints
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user

### Data Endpoints
- `GET /data` - Get user's data records
- `POST /data` - Create new data record
- `GET /data/{id}` - Get specific data record
- `PUT /data/{id}` - Update data record
- `DELETE /data/{id}` - Delete data record

## Authentication Flow
1. User registers with email/password
2. Server creates user account and returns JWT tokens
3. Client stores access token and uses it for authenticated requests
4. When access token expires, use refresh token to get new access token

## Data Isolation
- Each user's data is isolated by user ID
- All data access endpoints filter results by the authenticated user's ID
- Users cannot access other users' data

## Testing
Run backend tests:
```bash
cd backend
python -m pytest
```

Run frontend tests:
```bash
cd frontend
npm run test
```

## Deployment
1. Build the frontend: `npm run build` in frontend directory
2. Ensure environment variables are configured for production
3. Deploy using Docker or your preferred platform

## Troubleshooting
- **Database Connection Issues**: Verify database URL in environment files
- **Authentication Failures**: Check JWT secret and token expiration settings
- **Frontend API Errors**: Verify backend API URL in frontend environment files