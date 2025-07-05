#!/bin/bash

# Deep Research System Installation Script
# This script installs and configures the Deep Research System

set -e  # Exit on any error

echo "🚀 Deep Research System - Installation Script"
echo "=============================================="

# Check if Python 3.8+ is installed
echo "🔍 Checking Python version..."
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version found"
else
    echo "❌ Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p research_outputs data logs

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env file with your API keys"
else
    echo "ℹ️  .env file already exists"
fi

# Test installation
echo "🧪 Testing installation..."
python3 -c "
try:
    import crewai
    import langchain
    import pandas
    import numpy
    import matplotlib
    import plotly
    import requests
    import beautifulsoup4
    import nltk
    from deep_research_system.research_system import DeepResearchSystem
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📖 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python3 quick_start.py"
echo "3. Run: python3 main.py --topic 'your research topic'"
echo "4. Check README.md for full documentation"
echo ""
echo "🔑 Required API Keys:"
echo "- OpenAI API Key (required)"
echo "- Tavily API Key (recommended for better search)"
echo ""
echo "📚 Documentation: README.md" 