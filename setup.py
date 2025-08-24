#!/usr/bin/env python3
"""
SoF Event Extractor - Development Setup Script
Automated setup for development environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description, cwd=None):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            cwd=cwd,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if required system dependencies are available"""
    dependencies = {
        'git': 'git --version',
        'docker': 'docker --version',
        'docker-compose': 'docker-compose --version'
    }
    
    available = {}
    for name, command in dependencies.items():
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
            available[name] = True
            print(f"✅ {name} is available")
        except subprocess.CalledProcessError:
            available[name] = False
            print(f"⚠️ {name} is not available")
    
    return available

def setup_python_environment():
    """Set up Python virtual environment"""
    backend_dir = Path("backend")
    venv_dir = backend_dir / "venv"
    
    # Create virtual environment
    if not venv_dir.exists():
        if not run_command(
            f"python -m venv {venv_dir}", 
            "Creating Python virtual environment",
            cwd="."
        ):
            return False
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation script based on OS
    if platform.system() == "Windows":
        activate_script = venv_dir / "Scripts" / "activate.bat"
        pip_command = f"{venv_dir}\\Scripts\\pip"
    else:
        activate_script = venv_dir / "bin" / "activate"
        pip_command = f"{venv_dir}/bin/pip"
    
    # Install dependencies
    requirements_file = backend_dir / "requirements.txt"
    if requirements_file.exists():
        if not run_command(
            f"{pip_command} install -r {requirements_file}",
            "Installing Python dependencies",
            cwd="."
        ):
            return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = [
        "backend/uploads",
        "backend/exports",
        "backend/logs",
        "frontend/static/css",
        "frontend/static/images"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def create_env_file():
    """Create .env file with default configuration"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    env_content = """# SoF Event Extractor Configuration
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=dev-secret-key-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///sof_extractor.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=10485760

# AI/NLP Configuration
SPACY_MODEL=en_core_web_sm
TRANSFORMERS_CACHE=./models_cache

# Redis Configuration (for production)
REDIS_URL=redis://localhost:6379/0

# Celery Configuration (for production)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Security Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:5500

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log

# Docker Configuration
POSTGRES_DB=sof_extractor
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_setup():
    """Test the setup by running basic tests"""
    print("\n🧪 Testing setup...")
    
    # Test Python imports
    test_script = """
import sys
sys.path.append('backend')
try:
    from flask import Flask
    print("✅ Flask import successful")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

try:
    from flask_sqlalchemy import SQLAlchemy
    print("✅ SQLAlchemy import successful")
except ImportError as e:
    print(f"❌ SQLAlchemy import failed: {e}")
    sys.exit(1)

print("✅ All critical imports successful")
"""
    
    try:
        result = subprocess.run(
            [sys.executable, "-c", test_script],
            capture_output=True,
            text=True,
            cwd="."
        )
        
        if result.returncode == 0:
            print("✅ Setup test passed")
            print(result.stdout)
            return True
        else:
            print("❌ Setup test failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Setup test error: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("""
🎉 Setup completed successfully!

📋 Next Steps:

1. 🚀 Start the application:
   
   # Option 1: Manual start
   cd backend && python app.py
   
   # Option 2: Using VS Code workspace
   code ../sof-extractor.code-workspace
   # Then use Ctrl+Shift+P → "Tasks: Run Task" → "Start Flask Backend"

2. 🌐 Open the frontend:
   
   # In a new terminal
   cd frontend && python -m http.server 8000
   # Then visit: http://localhost:8000

3. 🐳 Or use Docker (if available):
   
   docker-compose up -d
   # Then visit: http://localhost

4. 🧪 Run tests:
   
   python simple_test.py

📚 Documentation:
   - README.md: Complete setup guide
   - PROJECT_OVERVIEW.md: Project structure and features
   - API docs: Available at /api/health when running

🔗 Access Points:
   - Frontend: http://localhost:8000
   - API: http://localhost:5000/api
   - Health Check: http://localhost:5000/api/health

🛠️ Development:
   - Use the VS Code workspace for best experience
   - All tasks and debug configurations are pre-configured
   - Check PROJECT_OVERVIEW.md for detailed information

Happy coding! 🚢✨
""")

def main():
    """Main setup function"""
    print("🚢 SoF Event Extractor - Development Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check system dependencies
    dependencies = check_dependencies()
    
    # Setup steps
    steps = [
        ("Creating directories", setup_directories),
        ("Setting up Python environment", setup_python_environment),
        ("Creating configuration file", create_env_file),
        ("Testing setup", test_setup)
    ]
    
    failed_steps = []
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        if not step_function():
            failed_steps.append(step_name)
    
    # Summary
    print("\n" + "=" * 50)
    if failed_steps:
        print("⚠️ Setup completed with some issues:")
        for step in failed_steps:
            print(f"   ❌ {step}")
        print("\nPlease resolve the issues above and run setup again.")
    else:
        print("✅ Setup completed successfully!")
        print_next_steps()

if __name__ == "__main__":
    main()
