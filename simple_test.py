#!/usr/bin/env python3
"""
Simple structure and syntax test for SoF Event Extractor
Tests basic code structure without external dependencies
"""

import os
import sys
import ast
import re

def test_file_structure():
    """Test if all required files exist"""
    print("🔍 Testing project structure...")
    
    required_files = [
        'backend/app.py',
        'backend/config.py',
        'backend/models/__init__.py',
        'backend/services/__init__.py',
        'backend/services/document_processor.py',
        'backend/services/event_extractor.py',
        'backend/services/ai_service.py',
        'backend/utils/__init__.py',
        'backend/utils/helpers.py',
        'backend/requirements.txt',
        'frontend/index.html',
        'frontend/static/js/app.js',
        'docker-compose.yml',
        'Dockerfile',
        'nginx.conf',
        '.env.example',
        '.gitignore',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print(f"✅ All {len(required_files)} required files exist")
        return True

def test_python_syntax():
    """Test Python files for syntax errors"""
    print("\n🔍 Testing Python syntax...")
    
    python_files = [
        'backend/app.py',
        'backend/config.py',
        'backend/models/__init__.py',
        'backend/services/__init__.py',
        'backend/services/document_processor.py',
        'backend/services/event_extractor.py',
        'backend/services/ai_service.py',
        'backend/utils/__init__.py',
        'backend/utils/helpers.py'
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST to check syntax
            ast.parse(content)
            print(f"✅ {file_path} - syntax OK")
            
        except SyntaxError as e:
            syntax_errors.append(f"{file_path}: {e}")
            print(f"❌ {file_path} - syntax error: {e}")
        except Exception as e:
            syntax_errors.append(f"{file_path}: {e}")
            print(f"❌ {file_path} - error: {e}")
    
    if syntax_errors:
        return False
    else:
        print("✅ All Python files have valid syntax")
        return True

def test_api_endpoints():
    """Test if API endpoints are defined in app.py"""
    print("\n🔍 Testing API endpoint definitions...")
    
    try:
        with open('backend/app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required endpoints
        required_endpoints = [
            r'@app\.route\([\'\"]/api/health[\'\"]\)',
            r'@app\.route\([\'\"]/api/upload[\'\"]\)',
            r'@app\.route\([\'\"]/api/process/<[^>]+>[\'\"]\)',
            r'@app\.route\([\'\"]/api/chat[\'\"]\)',
            r'@app\.route\([\'\"]/api/export/<[^>]+>/<[^>]+>[\'\"]\)'
        ]
        
        found_endpoints = []
        for endpoint_pattern in required_endpoints:
            if re.search(endpoint_pattern, content):
                found_endpoints.append(endpoint_pattern)
                print(f"✅ Found endpoint: {endpoint_pattern}")
            else:
                print(f"❌ Missing endpoint: {endpoint_pattern}")
        
        if len(found_endpoints) == len(required_endpoints):
            print("✅ All required API endpoints defined")
            return True
        else:
            print(f"❌ Missing {len(required_endpoints) - len(found_endpoints)} endpoints")
            return False
            
    except Exception as e:
        print(f"❌ Error checking API endpoints: {e}")
        return False

def test_frontend_structure():
    """Test frontend HTML and JavaScript structure"""
    print("\n🔍 Testing frontend structure...")
    
    try:
        # Check HTML file
        with open('frontend/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for required HTML elements
        required_elements = [
            r'<div[^>]*id=[\'"]uploadZone[\'"]',
            r'<div[^>]*id=[\'"]resultsSection[\'"]',
            r'<div[^>]*id=[\'"]chatTab[\'"]',
            r'<input[^>]*id=[\'"]fileInput[\'"]',
            r'<button[^>]*id=[\'"]sendChatBtn[\'"]'
        ]
        
        html_elements_found = 0
        for element_pattern in required_elements:
            if re.search(element_pattern, html_content):
                html_elements_found += 1
        
        print(f"✅ Found {html_elements_found}/{len(required_elements)} required HTML elements")
        
        # Check JavaScript file
        with open('frontend/static/js/app.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Check for required JavaScript functions
        required_functions = [
            r'function\s+handleFileSelect',
            r'function\s+sendMessage',
            r'function\s+uploadDocument',
            r'function\s+populateEventsTable'
        ]
        
        js_functions_found = 0
        for func_pattern in required_functions:
            if re.search(func_pattern, js_content):
                js_functions_found += 1
        
        print(f"✅ Found {js_functions_found}/{len(required_functions)} required JavaScript functions")
        
        if html_elements_found >= 4 and js_functions_found >= 3:
            print("✅ Frontend structure looks good")
            return True
        else:
            print("❌ Frontend structure incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Error checking frontend structure: {e}")
        return False

def test_docker_configuration():
    """Test Docker configuration files"""
    print("\n🔍 Testing Docker configuration...")
    
    try:
        # Check docker-compose.yml
        with open('docker-compose.yml', 'r', encoding='utf-8') as f:
            compose_content = f.read()
        
        required_services = ['backend', 'db', 'redis', 'nginx']
        services_found = 0
        
        for service in required_services:
            if f'{service}:' in compose_content:
                services_found += 1
        
        print(f"✅ Found {services_found}/{len(required_services)} required Docker services")
        
        # Check Dockerfile
        with open('Dockerfile', 'r', encoding='utf-8') as f:
            dockerfile_content = f.read()
        
        dockerfile_commands = ['FROM', 'WORKDIR', 'COPY', 'RUN', 'EXPOSE']
        commands_found = 0
        
        for command in dockerfile_commands:
            if command in dockerfile_content:
                commands_found += 1
        
        print(f"✅ Found {commands_found}/{len(dockerfile_commands)} required Dockerfile commands")
        
        if services_found >= 3 and commands_found >= 4:
            print("✅ Docker configuration looks good")
            return True
        else:
            print("❌ Docker configuration incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Error checking Docker configuration: {e}")
        return False

def test_configuration_files():
    """Test configuration and documentation files"""
    print("\n🔍 Testing configuration files...")
    
    try:
        # Check .env.example
        with open('.env.example', 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        required_env_vars = ['FLASK_ENV', 'DATABASE_URL', 'REDIS_URL', 'SECRET_KEY']
        env_vars_found = 0
        
        for var in required_env_vars:
            if var in env_content:
                env_vars_found += 1
        
        print(f"✅ Found {env_vars_found}/{len(required_env_vars)} required environment variables")
        
        # Check README.md
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        readme_sections = ['# SoF Event Extractor', '## Features', '## Installation', '## API Documentation']
        sections_found = 0
        
        for section in readme_sections:
            if section in readme_content:
                sections_found += 1
        
        print(f"✅ Found {sections_found}/{len(readme_sections)} required README sections")
        
        if env_vars_found >= 3 and sections_found >= 3:
            print("✅ Configuration files look good")
            return True
        else:
            print("❌ Configuration files incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Error checking configuration files: {e}")
        return False

def main():
    """Run all structure and syntax tests"""
    print("🚢 SoF Event Extractor - Structure & Syntax Test")
    print("=" * 55)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Syntax", test_python_syntax),
        ("API Endpoints", test_api_endpoints),
        ("Frontend Structure", test_frontend_structure),
        ("Docker Configuration", test_docker_configuration),
        ("Configuration Files", test_configuration_files),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED\n")
            else:
                print(f"❌ {test_name} FAILED\n")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}\n")
    
    print("=" * 55)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All structure and syntax tests PASSED!")
        print("📋 The project structure is complete and ready for deployment!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
