#!/bin/bash

echo "🚢 SoF Event Extractor - Opening Workspace"
echo "========================================"

# Check if VS Code is installed
if ! command -v code &> /dev/null; then
    echo "❌ VS Code is not installed or not in PATH"
    echo "Please install VS Code from: https://code.visualstudio.com/"
    echo "Or install via package manager:"
    echo "  • Ubuntu/Debian: sudo apt install code"
    echo "  • macOS: brew install --cask visual-studio-code"
    echo "  • Arch Linux: sudo pacman -S code"
    exit 1
fi

echo "✅ VS Code found"
echo "🔄 Opening workspace..."

# Open the workspace file
code sof-event-extractor.code-workspace

echo "✅ Workspace opened in VS Code!"
echo ""
echo "📋 Quick Start:"
echo "  • Press F5 to start Flask server with debugging"
echo "  • Use Ctrl+Shift+P (Cmd+Shift+P on Mac) for Command Palette"
echo "  • Check WORKSPACE_GUIDE.md for detailed instructions"
echo ""
echo "🎯 Happy coding! 🚢⚓"

# Keep terminal open for a moment
sleep 2
