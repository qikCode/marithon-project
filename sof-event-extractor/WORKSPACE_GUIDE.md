# 🚢 SoF Event Extractor - Workspace Guide

## 🎯 Welcome to Your Development Workspace!

This workspace has been configured with professional development tools and workflows for the **SoF Event Extractor** - a Flask-based maritime document processing system.

## 📁 Project Structure

```
sof-event-extractor/
├── 📱 app.py                          # Main Flask application
├── ⚙️ config.py                       # Configuration settings
├── 🗄️ models.py                       # Database models
├── 📦 requirements.txt                # Python dependencies
├── 📚 README.md                       # Project documentation
├── 📁 uploads/                        # Document upload directory
├── 📁 migrations/                     # Database migrations
├── 📁 services/                       # Business logic services
│   ├── 🤖 ai_service.py              # AI chat and export services
│   ├── 📄 document_processor.py       # Document text extraction
│   └── 🔍 event_extractor.py         # Maritime event extraction
├── 📁 utils/                          # Utility functions
│   └── 🛠️ helpers.py                  # File handling helpers
└── 📁 .vscode/                        # VS Code workspace configuration
    ├── settings.json                  # Editor settings
    ├── launch.json                    # Debug configurations
    └── tasks.json                     # Development tasks
```

## 🚀 Quick Start Guide

### 1. Open the Workspace
```bash
# Open in VS Code
code sof-event-extractor.code-workspace
```

### 2. Setup Development Environment
Use VS Code Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`):
- **"Tasks: Run Task"** → **"🐍 Setup Virtual Environment"**
- **"Tasks: Run Task"** → **"📦 Install Dependencies"**
- **"Tasks: Run Task"** → **"🗄️ Initialize Database"**

### 3. Start Development Server
- **"Tasks: Run Task"** → **"🚀 Start Flask Server"**
- Or press `F5` to start with debugging

### 4. Verify Setup
- **"Tasks: Run Task"** → **"📊 API Health Check"**
- Visit: http://localhost:5000/api/health

## 🛠️ Development Tools

### 🎯 VS Code Tasks (Ctrl+Shift+P → "Tasks: Run Task")

| Task | Description | Usage |
|------|-------------|-------|
| 🐍 **Setup Virtual Environment** | Creates Python virtual environment | First-time setup |
| 📦 **Install Dependencies** | Installs all required packages | After cloning/updating |
| 🚀 **Start Flask Server** | Launches development server | Daily development |
| 🧪 **Run All Tests** | Executes test suite | Before commits |
| 🔍 **Code Quality Check** | Runs flake8 linting | Code review |
| 🎨 **Format Code** | Auto-formats with Black | Before commits |
| 🗄️ **Initialize Database** | Creates database tables | First-time setup |
| 🧹 **Clean Cache** | Removes __pycache__ files | Cleanup |
| 📊 **API Health Check** | Tests server connectivity | Debugging |
| 🔄 **Restart Flask Server** | Restarts development server | When needed |

### 🐛 Debug Configurations (F5 or Debug Panel)

| Configuration | Purpose | When to Use |
|---------------|---------|-------------|
| 🚀 **Flask Development Server** | Debug main application | General debugging |
| 🧪 **Debug Tests** | Debug test execution | Test failures |
| 🔧 **Debug Current File** | Debug active file | Module-specific issues |
| 🗄️ **Debug Database Operations** | Debug model operations | Database issues |
| 🤖 **Debug AI Services** | Debug AI/chat features | AI functionality |
| 📄 **Debug Document Processor** | Debug file processing | Document parsing |

## 🎨 Code Quality & Standards

### Automatic Formatting
- **Black**: Code formatting (88 character line length)
- **isort**: Import sorting
- **Format on Save**: Enabled automatically

### Linting & Quality
- **Flake8**: Style and error checking
- **Pylint**: Advanced code analysis
- **Type Hints**: Encouraged for better code documentation

### Testing
- **pytest**: Test framework
- **Auto-discovery**: Tests found automatically
- **Coverage**: Track test coverage

## 🔧 Configuration Features

### Editor Enhancements
- **File Nesting**: Related files grouped together
- **Python Path**: Automatic PYTHONPATH configuration
- **IntelliSense**: Full autocomplete and suggestions
- **Error Highlighting**: Real-time error detection

### Workspace Organization
- **Excluded Files**: __pycache__, .pyc, venv hidden
- **File Associations**: Proper syntax highlighting
- **Terminal Integration**: Automatic virtual environment activation

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

## 🎯 Development Workflow

### Daily Development
1. **Open Workspace**: `code sof-event-extractor.code-workspace`
2. **Start Server**: Press `F5` or run "🚀 Start Flask Server" task
3. **Make Changes**: Edit code with full IntelliSense support
4. **Test Changes**: Use "📊 API Health Check" or manual testing
5. **Debug Issues**: Set breakpoints and use debug configurations

### Before Committing
1. **Format Code**: Run "🎨 Format Code" task
2. **Check Quality**: Run "🔍 Code Quality Check" task
3. **Run Tests**: Run "🧪 Run All Tests" task
4. **Clean Up**: Run "🧹 Clean Cache" task

### Troubleshooting
1. **Server Issues**: Use "🔄 Restart Flask Server" task
2. **Database Issues**: Run "🗄️ Initialize Database" task
3. **Dependency Issues**: Run "📦 Install Dependencies" task
4. **Environment Issues**: Run "🐍 Setup Virtual Environment" task

## 🚀 Advanced Features

### Background Tasks
- **File Processing**: Asynchronous document processing
- **Event Extraction**: AI-powered maritime event detection
- **Export Generation**: CSV/JSON export with customization

### AI Integration
- **Chat System**: Interactive maritime document queries
- **Event Recognition**: Advanced NLP for maritime operations
- **Confidence Scoring**: Reliability metrics for extracted data

### Database Features
- **SQLAlchemy ORM**: Object-relational mapping
- **Migration Support**: Database schema versioning
- **Relationship Management**: Document-event relationships

## 🎉 Ready to Develop!

Your workspace is now fully configured with:

- ✅ **Professional IDE Setup**: VS Code with maritime-specific configurations
- ✅ **Development Tools**: Tasks, debugging, and quality checks
- ✅ **Code Standards**: Automatic formatting and linting
- ✅ **Testing Framework**: Comprehensive test support
- ✅ **Documentation**: Complete guides and references

### Next Steps:
1. **Explore the Code**: Browse through the services and models
2. **Run the Application**: Start the Flask server and test endpoints
3. **Upload Documents**: Test the maritime document processing
4. **Use AI Chat**: Interact with the maritime AI assistant
5. **Export Data**: Generate CSV/JSON reports

**Happy coding! 🚢⚓**

---

*For additional help, check the README.md or explore the VS Code Command Palette for available tasks and debug configurations.*
