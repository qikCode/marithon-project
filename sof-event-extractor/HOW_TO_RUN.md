# 🚀 How to Run SoF Event Extractor - Quick Start Guide

## 🎯 3 Simple Steps to Get Started

### Step 1: Open the Workspace
Choose your operating system:

**Windows:**
```bash
# Double-click this file:
open_workspace.bat
```

**Linux/Mac:**
```bash
# Run this command:
./open_workspace.sh
```

**Manual (Any OS):**
```bash
# Open VS Code with workspace
code sof-event-extractor.code-workspace
```

### Step 2: Setup Environment (First Time Only)
In VS Code, press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac) and run:
1. **"Tasks: Run Task"** → **"🐍 Setup Virtual Environment"**
2. **"Tasks: Run Task"** → **"📦 Install Dependencies"**
3. **"Tasks: Run Task"** → **"🗄️ Initialize Database"**

### Step 3: Start the Application
**Option A: Debug Mode (Recommended)**
- Press `F5` in VS Code
- This starts Flask with debugging enabled

**Option B: Using Tasks**
- Press `Ctrl+Shift+P` → **"Tasks: Run Task"** → **"🚀 Start Flask Application"**

## 🌐 Access the Application

Once running, the Flask server will be available at:
- **Health Check**: http://localhost:5000/api/health
- **API Base**: http://localhost:5000/api/

## 📱 Test the API

### Quick Health Check
```bash
# Windows (PowerShell)
Invoke-RestMethod -Uri "http://localhost:5000/api/health"

# Linux/Mac
curl http://localhost:5000/api/health
```

### Upload a Document
```bash
# Using curl (Linux/Mac)
curl -X POST -F "file=@your-document.pdf" http://localhost:5000/api/upload

# Using PowerShell (Windows)
$form = @{file = Get-Item "your-document.pdf"}
Invoke-RestMethod -Uri "http://localhost:5000/api/upload" -Method Post -Form $form
```

## 🛠️ Common Development Tasks

### In VS Code Command Palette (`Ctrl+Shift+P`):

| Task | Purpose |
|------|---------|
| **🚀 Start Flask Application** | Launch the server |
| **🧪 Run Tests** | Execute test suite |
| **🔍 Check Code Quality** | Run code linting |
| **🎨 Format Code** | Auto-format code |
| **🧹 Clean Cache** | Remove Python cache files |
| **📊 API Health Check** | Test if server is running |

## 🐛 Debugging

1. **Set Breakpoints**: Click left margin in VS Code
2. **Press F5**: Start debugging
3. **Use Debug Console**: Interact with running application
4. **Step Through Code**: Use debug controls

## 📁 Project Structure

```
sof-event-extractor/
├── app.py              # 👈 Main Flask application (START HERE)
├── config.py           # Configuration settings
├── models.py           # Database models
├── requirements.txt    # Dependencies
├── services/           # Business logic
│   ├── ai_service.py
│   ├── document_processor.py
│   └── event_extractor.py
└── utils/              # Helper functions
    └── helpers.py
```

## 🔧 Troubleshooting

### Server Won't Start?
```bash
# Check if Python is installed
python --version

# Check if virtual environment exists
ls venv/  # Linux/Mac
dir venv\  # Windows

# Recreate virtual environment
python -m venv venv
```

### Import Errors?
```bash
# Install dependencies
pip install -r requirements.txt

# Or use VS Code task:
# Ctrl+Shift+P → "Tasks: Run Task" → "📦 Install Dependencies"
```

### Database Issues?
```bash
# Reinitialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Or use VS Code task:
# Ctrl+Shift+P → "Tasks: Run Task" → "🗄️ Initialize Database"
```

### Port Already in Use?
```bash
# Kill existing Flask processes
# Linux/Mac:
pkill -f "python.*app.py"

# Windows:
taskkill /f /im python.exe
```

## 🎉 You're Ready!

Once the server is running:
1. **Upload maritime documents** via `/api/upload`
2. **Process documents** to extract events
3. **Chat with AI** about your documents
4. **Export data** in CSV or JSON format

**Happy maritime document processing! 🚢⚓**

---

*Need more help? Check WORKSPACE_GUIDE.md for detailed instructions.*
