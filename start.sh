#!/bin/bash

echo "🚢 SoF Event Extractor - Quick Start (Linux/Mac)"
echo "================================================"

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to start backend
start_backend() {
    echo ""
    echo "🔄 Starting Flask Backend..."
    
    if check_port 5000; then
        echo "⚠️  Port 5000 is already in use. Backend might already be running."
    else
        cd backend
        python app.py &
        BACKEND_PID=$!
        cd ..
        echo "✅ Backend started (PID: $BACKEND_PID)"
    fi
}

# Function to start frontend
start_frontend() {
    echo ""
    echo "🌐 Starting Frontend Server..."
    
    if check_port 8000; then
        echo "⚠️  Port 8000 is already in use. Frontend might already be running."
    else
        cd frontend
        python -m http.server 8000 &
        FRONTEND_PID=$!
        cd ..
        echo "✅ Frontend started (PID: $FRONTEND_PID)"
    fi
}

# Function to open browser
open_browser() {
    echo ""
    echo "🌐 Opening frontend in browser..."
    
    # Detect OS and open browser accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open http://localhost:8000
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v xdg-open > /dev/null; then
            xdg-open http://localhost:8000
        elif command -v gnome-open > /dev/null; then
            gnome-open http://localhost:8000
        else
            echo "Please open http://localhost:8000 in your browser"
        fi
    else
        echo "Please open http://localhost:8000 in your browser"
    fi
}

# Main execution
echo ""
echo "🔍 Checking system requirements..."

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "✅ Python found: $PYTHON_CMD"

# Start services
start_backend

echo ""
echo "⏳ Waiting for backend to start..."
sleep 3

start_frontend

echo ""
echo "⏳ Waiting for frontend to start..."
sleep 2

echo ""
echo "🎉 SoF Event Extractor is running!"
echo ""
echo "📋 Access Points:"
echo "   Frontend: http://localhost:8000"
echo "   API:      http://localhost:5000/api"
echo "   Health:   http://localhost:5000/api/health"

open_browser

echo ""
echo "✅ Setup complete! Services are running in the background."
echo ""
echo "🛑 To stop the services, run:"
echo "   pkill -f 'python.*app.py'"
echo "   pkill -f 'python.*http.server'"
echo ""
echo "📝 Or use Ctrl+C to stop this script and then kill background processes"

# Keep script running
echo "Press Ctrl+C to exit..."
trap 'echo ""; echo "🛑 Stopping services..."; pkill -f "python.*app.py"; pkill -f "python.*http.server"; echo "✅ Services stopped. Goodbye!"; exit 0' INT

# Wait indefinitely
while true; do
    sleep 1
done
