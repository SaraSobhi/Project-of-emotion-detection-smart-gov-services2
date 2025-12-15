# GovCare Project

Full-stack feedback management system with sentiment analysis.

## Quick Start with Docker

```bash
# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:8000
# Backend API: http://localhost:5000
```

## Services

- **Frontend** (Port 8000) - GovCare web interface
- **Backend** (Port 5000) - Main API service
- **ML Service** (Internal) - Sentiment analysis
- **PostgreSQL** (Port 5432) - Database

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment guide
- [frontend/README.md](frontend/README.md) - Frontend documentation

## Development

### Run Individual Services

**Frontend (Demo Mode):**
```bash
cd frontend
pip install -r requirements_minimal.txt
python app_demo.py
```

**Backend:**
```bash
cd backend/main_service
pip install -r requirements.txt
python app.py
```

**ML Service:**
```bash
cd backend/ml_service
pip install -r requirements.txt
python predict.py
```

## Architecture

```
Frontend (8000) → Backend (5000) → ML Service (5001)
                       ↓
                  PostgreSQL (5432)
```

## Demo Credentials

- Username: `admin`
- Password: `admin123`
