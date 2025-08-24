# 🚢 SoF Event Extractor - Project Overview

## 📋 Project Structure

```
sof-extractor/
├── 📁 backend/                    # Flask API Backend
│   ├── 🐍 app.py                 # Main Flask application
│   ├── ⚙️ config.py              # Configuration management
│   ├── 📦 requirements.txt       # Python dependencies
│   ├── 📁 models/                # Database models
│   │   └── __init__.py           # Document & Event models
│   ├── 📁 services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── document_processor.py # PDF/DOC/DOCX processing
│   │   ├── event_extractor.py    # AI event extraction
│   │   └── ai_service.py         # Chat & export services
│   └── 📁 utils/                 # Utility functions
│       ├── __init__.py
│       └── helpers.py            # Helper functions
├── 📁 frontend/                  # Web Interface
│   ├── 🌐 index.html            # Main HTML page
│   └── 📁 static/
│       └── 📁 js/
│           └── app.js            # Frontend JavaScript
├── 🐳 docker-compose.yml        # Multi-service Docker setup
├── 🐳 Dockerfile               # Container configuration
├── 🌐 nginx.conf               # Reverse proxy config
├── 📝 README.md                # Documentation
├── 🚫 .gitignore               # Git ignore rules
├── 🧪 simple_test.py           # Basic functionality tests
└── 🧪 test_basic_functionality.py # Comprehensive tests
```

## 🎯 Key Features

### ✅ Backend API (Flask)
- **Document Upload & Processing**: PDF, DOC, DOCX support
- **AI Event Extraction**: NLP-powered maritime event detection
- **Interactive Chat**: AI assistant for document queries
- **Data Export**: CSV/JSON export with customizable options
- **RESTful API**: 10+ endpoints for full functionality

### ✅ Frontend Interface
- **Responsive Design**: Mobile-first with Tailwind CSS
- **Drag & Drop Upload**: Intuitive file upload experience
- **Real-time Processing**: Live status updates and notifications
- **Interactive Timeline**: Event visualization and filtering
- **AI Chat Interface**: Contextual maritime assistance

### ✅ Infrastructure
- **Docker Deployment**: Multi-service containerization
- **Database Integration**: SQLAlchemy with PostgreSQL support
- **Background Processing**: Celery for async operations
- **Reverse Proxy**: Nginx with SSL and security headers
- **Monitoring**: Health checks and logging

## 🚀 Quick Start Commands

### Development Setup
```bash
# Open workspace in VS Code
code sof-extractor.code-workspace

# Setup Python environment
python -m venv backend/venv
source backend/venv/bin/activate  # Windows: backend\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start backend
python backend/app.py

# Start frontend (new terminal)
cd frontend && python -m http.server 8000
```

### Docker Deployment
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔗 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:8000 | Web interface |
| **API** | http://localhost:5000/api | REST API endpoints |
| **Health Check** | http://localhost:5000/api/health | Service status |
| **Docker (Nginx)** | http://localhost | Production setup |

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/upload` | Upload document |
| POST | `/api/process/<id>` | Process document |
| GET | `/api/documents/<id>/events` | Get events |
| POST | `/api/chat` | AI chat |
| GET | `/api/export/<id>/<format>` | Export data |
| GET | `/api/documents/<id>/summary` | Get summary |
| GET | `/api/documents` | List documents |

## 🛠️ Development Tools

### VS Code Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- 🐍 **Setup Python Environment**: Create virtual environment
- 📦 **Install Dependencies**: Install Python packages
- 🚀 **Start Flask Backend**: Run development server
- 🌐 **Start Frontend Server**: Serve static files
- 🐳 **Docker Build**: Build containers
- 🐳 **Docker Up**: Start all services
- 🧪 **Run Tests**: Execute test suite

### Debug Configurations (F5)
- 🚀 **Flask App**: Debug backend with breakpoints
- 🧪 **Run Tests**: Debug test execution

## 🎨 Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **PyPDF2**: PDF processing
- **python-docx**: Word document processing
- **spaCy**: NLP processing
- **Celery**: Background tasks
- **Redis**: Caching and message broker

### Frontend
- **HTML5**: Modern web standards
- **Tailwind CSS**: Utility-first CSS framework
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Mobile-first approach

### Infrastructure
- **Docker**: Containerization
- **PostgreSQL**: Production database
- **Nginx**: Reverse proxy and load balancer
- **SQLite**: Development database

## 🔧 Configuration

### Environment Variables
```bash
# Backend Configuration
FLASK_ENV=development
FLASK_DEBUG=1
DATABASE_URL=sqlite:///sof_extractor.db
SECRET_KEY=your-secret-key
UPLOAD_FOLDER=uploads

# Docker Configuration
POSTGRES_DB=sof_extractor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
REDIS_URL=redis://redis:6379/0
```

## 📈 Performance Features

- **File Deduplication**: Hash-based duplicate detection
- **Background Processing**: Async document processing
- **Caching**: Redis-based response caching
- **Database Optimization**: Indexed queries and relationships
- **Lazy Loading**: Efficient data loading strategies

## 🔒 Security Features

- **Input Validation**: File type and size restrictions
- **CORS Configuration**: Cross-origin request handling
- **SQL Injection Protection**: Parameterized queries
- **File Upload Security**: Secure filename handling
- **Error Handling**: Comprehensive exception management

## 🧪 Testing

### Test Files
- `simple_test.py`: Basic structure validation
- `test_basic_functionality.py`: Comprehensive API testing

### Test Coverage
- ✅ File structure validation
- ✅ API endpoint testing
- ✅ Database model validation
- ✅ Service integration testing
- ✅ Frontend functionality testing

## 📚 Documentation

- **README.md**: Setup and deployment guide
- **API Documentation**: Endpoint specifications
- **Docker Guide**: Container deployment
- **Development Guide**: Local setup instructions

## 🎯 Next Steps

1. **Install Dependencies**: Run setup tasks in VS Code
2. **Start Development**: Use debug configurations
3. **Test Functionality**: Upload sample documents
4. **Deploy Production**: Use Docker Compose
5. **Monitor Performance**: Check logs and metrics

---

**🚢 Ready to extract maritime events with AI-powered precision!**
