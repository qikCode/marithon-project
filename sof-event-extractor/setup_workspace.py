#!/usr/bin/env python3
"""
SoF Event Extractor - Workspace Setup Script
Automated setup for development environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("🚢" + "=" * 60)
    print("   SoF Event Extractor - Workspace Setup")
    print("   Maritime Document Processing System")
    print("=" * 62)
    print()

def run_command(command, description, cwd=None, shell=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, list):
            result = subprocess.run(
                command,
                check=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                shell=shell
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                cwd=cwd,
                capture_output=True,
                text=True
            )
        print(f"✅ {description} completed successfully")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_system_dependencies():
    """Check if required system dependencies are available"""
    dependencies = {
        'git': 'git --version',
        'pip': 'pip --version',
        'curl': 'curl --version' if platform.system() != 'Windows' else 'powershell -Command "Get-Command curl"'
    }

    available = {}
    for name, command in dependencies.items():
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
            available[name] = True
            print(f"✅ {name} is available")
        except subprocess.CalledProcessError:
            available[name] = False
            print(f"⚠️  {name} is not available (optional)")

    return available

def setup_virtual_environment():
    """Set up Python virtual environment"""
    venv_dir = Path("venv")

    if venv_dir.exists():
        print("✅ Virtual environment already exists")
        return True

    success, output = run_command(
        "python -m venv venv",
        "Creating Python virtual environment"
    )
    return success

def install_dependencies():
    """Install Python dependencies"""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("⚠️  requirements.txt not found, skipping dependency installation")
        return True

    # Determine pip command based on OS
    if platform.system() == "Windows":
        pip_command = "venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_command = "venv/bin/pip install -r requirements.txt"

    success, output = run_command(
        pip_command,
        "Installing Python dependencies"
    )
    return success

def initialize_database():
    """Initialize the database"""
    init_script = '''
from app import app, db
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
'''

    # Determine python command based on OS
    if platform.system() == "Windows":
        python_command = f'venv\\Scripts\\python -c "{init_script}"'
    else:
        python_command = f'venv/bin/python -c "{init_script}"'

    success, output = run_command(
        python_command,
        "Initializing database"
    )

    if success:
        print("   " + output.strip())

    return success

def create_directories():
    """Create necessary directories"""
    directories = [
        "uploads",
        "logs",
        "exports",
        "tests"
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

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log
"""

    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_flask_app():
    """Test if Flask app can be imported and run"""
    test_script = '''
import sys
sys.path.insert(0, ".")
try:
    from app import app
    print("✅ Flask app imported successfully")
    with app.app_context():
        print("✅ Flask app context created successfully")
except Exception as e:
    print(f"❌ Flask app test failed: {e}")
    sys.exit(1)
'''

    # Determine python command based on OS
    if platform.system() == "Windows":
        python_command = f'venv\\Scripts\\python -c "{test_script}"'
    else:
        python_command = f'venv/bin/python -c "{test_script}"'

    success, output = run_command(
        python_command,
        "Testing Flask application"
    )

    if success:
        print("   " + output.strip())

    return success

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Workspace setup completed successfully!")
    print("\n📋 Next Steps:")
    print("\n1. 🚀 Open VS Code Workspace:")
    print("   code sof-event-extractor.code-workspace")
    print("\n2. 🎯 Start Development:")
    print("   • Press F5 to start Flask server with debugging")
    print("   • Or use Ctrl+Shift+P → 'Tasks: Run Task' → '🚀 Start Flask Server'")
    print("\n3. 🌐 Access the Application:")
    print("   • API Health Check: http://localhost:5000/api/health")
    print("   • Upload endpoint: http://localhost:5000/api/upload")
    print("\n4. 🛠️ Development Tools:")
    print("   • Use VS Code tasks for common operations")
    print("   • Debug configurations available in Run panel")
    print("   • Code formatting and linting enabled")
    print("\n5. 📚 Documentation:")
    print("   • README.md: Project overview and API docs")
    print("   • WORKSPACE_GUIDE.md: Detailed workspace guide")
    print("\n🚢 Ready to process maritime documents with AI! ⚓")

def main():
    """Main setup function"""
    print_header()

    # Check system requirements
    if not check_python_version():
        sys.exit(1)

    print("\n🔍 Checking system dependencies...")
    dependencies = check_system_dependencies()

    # Setup steps
    steps = [
        ("Creating directories", create_directories),
        ("Setting up virtual environment", setup_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Creating configuration file", create_env_file),
        ("Initializing database", initialize_database),
        ("Testing Flask application", test_flask_app)
    ]

    print("\n🔧 Setting up workspace...")
    failed_steps = []

    for step_name, step_function in steps:
        if not step_function():
            failed_steps.append(step_name)

    # Summary
    print("\n" + "=" * 62)
    if failed_steps:
        print("⚠️  Setup completed with some issues:")
        for step in failed_steps:
            print(f"   ❌ {step}")
        print("\n💡 You may need to:")
        print("   • Install missing dependencies manually")
        print("   • Check Python version and virtual environment")
        print("   • Review error messages above")
    else:
        print_next_steps()

if __name__ == "__main__":
    main()
