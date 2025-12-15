# GovCare - Full Stack Deployment

This docker-compose configuration orchestrates all GovCare services.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Public Network                       │
│                                                          │
│  ┌──────────────┐      ┌──────────────┐                │
│  │   Frontend   │─────▶│   Backend    │                │
│  │  (Port 8000) │      │ (Port 5000)  │                │
│  └──────────────┘      └──────┬───────┘                │
│                               │                          │
│                               │                          │
│                        ┌──────▼───────┐                 │
│                        │  PostgreSQL  │                 │
│                        │ (Port 5432)  │                 │
│                        └──────────────┘                 │
└────────────────────────────┬────────────────────────────┘
                             │
┌────────────────────────────┼────────────────────────────┐
│                  Internal Network                        │
│                             │                            │
│                      ┌──────▼───────┐                   │
│                      │  ML Service  │                   │
│                      │ (Port 5001)  │                   │
│                      └──────────────┘                   │
└──────────────────────────────────────────────────────────┘
```

## Services

### 1. **PostgreSQL Database**
- Image: `postgres:15-alpine`
- Port: `5432` (public)
- Networks: `internal`, `public`
- Persistent volume: `postgres_data`

### 2. **ML Service** (Internal Only)
- Build: `./backend/ml_service`
- Port: `5001` (internal only, not exposed)
- Network: `internal` only
- Purpose: Sentiment analysis predictions

### 3. **Backend (Main Service)** (Public)
- Build: `./backend/main_service`
- Port: `5000` (public)
- Networks: `internal`, `public`
- Connects to: PostgreSQL, ML Service

### 4. **Frontend** (Public)
- Build: `./frontend`
- Port: `8000` (public)
- Network: `public` only
- Connects to: Backend

## Quick Start

### Start All Services
```bash
docker-compose up -d
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f ml-service
docker-compose logs -f postgres
```

### Stop All Services
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

### Rebuild Services
```bash
docker-compose up -d --build
```

## Access Points

- **Frontend**: http://localhost:8000
- **Backend API**: http://localhost:5000
- **PostgreSQL**: localhost:5432
- **ML Service**: Not accessible externally (internal network only)

## Environment Variables

All environment variables are configured in the docker-compose.yml:

**Backend:**
- `DB_HOST=postgres`
- `DB_NAME=postgres`
- `DB_USER=postgres`
- `DB_PASSWORD=password`
- `ML_API_URL=http://ml-service:5001/predict`

**Frontend:**
- `BACKEND_URL=http://backend:5000`

## Network Configuration

### Internal Network
- Used for: Backend ↔ ML Service communication
- Isolated from external access
- ML Service only accessible from backend

### Public Network
- Used for: Frontend ↔ Backend ↔ PostgreSQL
- Exposed to host machine
- Accessible via published ports

## Health Checks

All services include health checks:
- **PostgreSQL**: Checks database readiness
- **ML Service**: Verifies prediction endpoint
- **Backend**: Checks API availability
- **Frontend**: Verifies web server

## Troubleshooting

### Check Service Status
```bash
docker-compose ps
```

### Restart a Service
```bash
docker-compose restart backend
```

### View Service Logs
```bash
docker-compose logs --tail=100 backend
```

### Access Container Shell
```bash
docker-compose exec backend sh
docker-compose exec postgres psql -U postgres
```

### Database Access
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d postgres

# View tables
\dt

# View feedbacks
SELECT * FROM feedbacks;
```

## Production Considerations

1. **Change Default Passwords**: Update PostgreSQL password in production
2. **Use Secrets**: Store sensitive data in Docker secrets
3. **Enable SSL**: Configure HTTPS for frontend and backend
4. **Resource Limits**: Add memory and CPU limits to services
5. **Backup Strategy**: Implement regular database backups
6. **Monitoring**: Add logging and monitoring solutions

## Development Mode

To run in development with hot-reload:
```bash
# Mount local directories as volumes (add to docker-compose.yml)
volumes:
  - ./frontend:/app
  - ./backend/main_service:/app
```
