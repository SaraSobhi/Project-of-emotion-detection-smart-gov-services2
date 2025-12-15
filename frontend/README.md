# Frontend Application

## Quick Start (No Backend Required)

### Option 1: Minimal Installation (Demo Mode)
```bash
cd frontend
pip install -r requirements_minimal.txt
python app_demo.py
```

Then open: http://localhost:8000

**Demo Credentials:**
- Username: `admin`
- Password: `admin123`

### Option 2: Full Installation (with Excel Export)
```bash
cd frontend
pip install Flask pandas openpyxl
python app_demo.py
```

## Demo Credentials
- **Username**: `admin`
- **Password**: `admin123`

## Features Available in Demo
- ✅ Public feedback submission (creates random sentiment)
- ✅ Login/Signup pages (demo mode)
- ✅ Admin dashboard with 8 sample feedbacks
- ✅ Date and sentiment filtering
- ✅ Interactive pie charts (sentiment/negation)
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Excel export (if pandas installed)

## Sample Data
The demo includes 8 pre-loaded feedbacks with various sentiments:
- 4 Positive feedbacks
- 2 Negative feedbacks  
- 2 Neutral feedbacks

## Full Application (with Backend)
To run the full application with the backend API:
```bash
# Terminal 1 - Backend
cd backend/main_service
pip install -r requirements.txt
python app.py

# Terminal 2 - Frontend
cd frontend
pip install -r requirements.txt
python app.py
```

## Docker Deployment (Production)

The Dockerfile is configured for the **main application** (app.py) which requires the backend API.

### Build Image
```bash
cd frontend
docker build -t govcare-frontend .
```

### Run Container
You need to specify the backend URL when running:
```bash
docker run -d \
  -p 8000:8000 \
  -e BACKEND_URL=http://your-backend-host:5000 \
  --name govcare-frontend \
  govcare-frontend
```

### Example with Docker Network
If running backend in Docker too:
```bash
# Create network
docker network create govcare-network

# Run backend (example)
docker run -d --name govcare-backend --network govcare-network backend-image

# Run frontend
docker run -d \
  -p 8000:8000 \
  -e BACKEND_URL=http://govcare-backend:5000 \
  --network govcare-network \
  --name govcare-frontend \
  govcare-frontend
```

## Notes
- The demo app runs on port 8000
- Demo mode: All data is in-memory and resets when you restart
- Production mode: Requires backend API connection
- Export to XLSX requires pandas
- Docker image uses full dependencies for production deployment
