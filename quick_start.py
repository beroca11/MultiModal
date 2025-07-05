#!/usr/bin/env python3
"""
Quick Start Script for Deep Research System
Run this to test the system with a simple research topic.
"""

import os
import sys
from deep_research_system.research_system import DeepResearchSystem

def quick_research():
    """Run a quick research test"""
    print("🚀 Deep Research System - Quick Start")
    print("="*50)
    
    # Check if any AI provider API key is set
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if not any([openai_key, anthropic_key, google_key]):
        print("❌ No AI provider API key found!")
        print("Please set at least one of the following API keys:")
        print("1. OpenAI API Key: export OPENAI_API_KEY='your_key'")
        print("2. Anthropic API Key: export ANTHROPIC_API_KEY='your_key'")
        print("3. Google API Key: export GOOGLE_API_KEY='your_key'")
        print("\nOr edit .env file and add your API keys")
        return False
    
    try:
        # Initialize the system
        print("🔧 Initializing Deep Research System...")
        research_system = DeepResearchSystem()
        
        # Show provider information
        provider_info = research_system.get_provider_info()
        print(f"🤖 Using AI Provider: {provider_info['preferred_provider'].upper()}")
        print(f"📊 Model: {provider_info['current_model']}")
        
        # Conduct a quick research
        print("🔍 Conducting quick research on 'AI trends 2024'...")
        results = research_system.conduct_research(
            topic="AI trends 2024",
            research_depth="basic",
            target_audience="general",
            output_format="markdown",
            save_results=True
        )
        
        # Display results
        print("\n" + "="*50)
        print("✅ QUICK RESEARCH COMPLETED!")
        print("="*50)
        print(f"Topic: {results['topic']}")
        print(f"AI Provider: {results['ai_provider'].upper()}")
        print(f"AI Model: {results['ai_model']}")
        print(f"Execution Time: {results['execution_time']:.2f} seconds")
        print(f"Research Depth: {results['research_depth']}")
        
        print("\n📋 EXECUTIVE SUMMARY:")
        print("-" * 30)
        print(results['summary'][:500] + "..." if len(results['summary']) > 500 else results['summary'])
        
        print(f"\n💾 Results saved to research_outputs/ directory")
        print("🎉 System is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("1. Check your API keys are valid")
        print("2. Ensure you have internet connection")
        print("3. Check the README.md for more help")
        return False

def show_providers():
    """Show available AI providers"""
    print("🤖 Available AI Providers:")
    print("="*30)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    providers = {
        "OpenAI": openai_key,
        "Anthropic (Claude)": anthropic_key,
        "Google (Gemini)": google_key
    }
    
    for provider, key in providers.items():
        status = "✅ Available" if key else "❌ Not Available"
        print(f"  {provider}: {status}")
    
    if not any([openai_key, anthropic_key, google_key]):
        print("\n❌ No AI providers configured!")
        print("Please set at least one API key in your .env file or environment variables.")
    else:
        print(f"\n✅ At least one AI provider is available!")
        print("You can run: python quick_start.py to test the system.")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("Quick Start Script for Deep Research System")
            print("\nUsage:")
            print("  python quick_start.py          # Run quick research test")
            print("  python quick_start.py --help   # Show this help")
            print("  python quick_start.py --providers  # Show available AI providers")
            return
        elif sys.argv[1] == "--providers":
            show_providers()
            return
    
    success = quick_research()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Try: python main.py --topic 'your research topic'")
        print("2. Try: python main.py --show-providers")
        print("3. Run: python example_usage.py for more examples")
        print("4. Check README.md for full documentation")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main() 