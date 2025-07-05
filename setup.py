#!/usr/bin/env python3
"""
Setup script for the Deep Research System
Handles installation, configuration, and initial setup.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("ℹ️  .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    try:
        # Copy env.example to .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your API keys")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["research_outputs", "data", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Created necessary directories")

def validate_installation():
    """Validate the installation"""
    print("🔍 Validating installation...")
    
    try:
        # Test imports
        import crewai
        import langchain
        import pandas
        import numpy
        import matplotlib
        import plotly
        import requests
        import beautifulsoup4
        import nltk
        
        # Test AI provider imports
        try:
            import openai
            print("✅ OpenAI package imported successfully")
        except ImportError:
            print("⚠️  OpenAI package not available")
        
        try:
            import anthropic
            print("✅ Anthropic package imported successfully")
        except ImportError:
            print("⚠️  Anthropic package not available")
        
        try:
            import google.generativeai
            print("✅ Google Generative AI package imported successfully")
        except ImportError:
            print("⚠️  Google Generative AI package not available")
        
        print("✅ All required packages imported successfully")
        
        # Test deep research system import
        from deep_research_system.research_system import DeepResearchSystem
        print("✅ Deep Research System imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def setup_api_keys():
    """Interactive API key setup"""
    print("\n🔑 API Key Setup")
    print("="*40)
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found. Please run setup first.")
        return False
    
    # Read current .env content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Check for existing keys
    if "your_openai_api_key_here" not in content and "your_anthropic_api_key_here" not in content and "your_google_api_key_here" not in content:
        print("ℹ️  API keys already configured")
        return True
    
    print("Please provide your API keys (press Enter to skip):")
    print("Note: At least one AI provider API key is required.")
    
    # OpenAI API Key
    openai_key = input("OpenAI API Key: ").strip()
    if openai_key:
        content = content.replace("your_openai_api_key_here", openai_key)
    
    # Anthropic API Key
    anthropic_key = input("Anthropic API Key: ").strip()
    if anthropic_key:
        content = content.replace("your_anthropic_api_key_here", anthropic_key)
    
    # Google API Key
    google_key = input("Google API Key: ").strip()
    if google_key:
        content = content.replace("your_google_api_key_here", google_key)
    
    # Tavily API Key
    tavily_key = input("Tavily API Key (optional): ").strip()
    if tavily_key:
        content = content.replace("your_tavily_api_key_here", tavily_key)
    
    # Preferred AI Provider
    print("\nSelect your preferred AI provider:")
    print("1. OpenAI (GPT-4)")
    print("2. Anthropic (Claude)")
    print("3. Google (Gemini)")
    
    provider_choice = input("Enter choice (1-3, default: 1): ").strip()
    if provider_choice == "2":
        content = content.replace("PREFERRED_AI_PROVIDER=openai", "PREFERRED_AI_PROVIDER=anthropic")
    elif provider_choice == "3":
        content = content.replace("PREFERRED_AI_PROVIDER=openai", "PREFERRED_AI_PROVIDER=google")
    
    # Write updated content
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ API keys configured")
    
    # Validate that at least one AI provider is configured
    if not any([openai_key, anthropic_key, google_key]):
        print("⚠️  Warning: No AI provider API keys were provided.")
        print("   You'll need to add at least one API key to use the system.")
    
    return True

def run_test():
    """Run a simple test to verify the system works"""
    print("\n🧪 Running system test...")
    
    try:
        from deep_research_system.research_system import DeepResearchSystem
        
        # Initialize system
        research_system = DeepResearchSystem()
        print("✅ System initialized successfully")
        
        # Show provider information
        provider_info = research_system.get_provider_info()
        print(f"🤖 Preferred Provider: {provider_info['preferred_provider'].upper()}")
        print(f"📊 Available Providers: {list(provider_info['available_providers'].keys())}")
        
        # Test basic functionality
        print("✅ Basic functionality test passed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Deep Research System Setup")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Validate installation
    if not validate_installation():
        print("❌ Installation validation failed")
        sys.exit(1)
    
    # Setup API keys
    setup_api_keys()
    
    # Run test
    if not run_test():
        print("❌ System test failed")
        sys.exit(1)
    
    print("\n" + "="*40)
    print("✅ Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Edit .env file with your API keys (if not done during setup)")
    print("2. Run: python quick_start.py --providers (to check available providers)")
    print("3. Run: python quick_start.py (to test the system)")
    print("4. Run: python main.py --topic 'your research topic'")
    print("5. Check example_usage.py for more examples")
    print("\n📚 Documentation: README.md")
    print("\n🔑 Required API Keys:")
    print("- At least one AI provider: OpenAI, Anthropic, or Google")
    print("- Optional: Tavily API Key for enhanced search")

if __name__ == "__main__":
    main() 