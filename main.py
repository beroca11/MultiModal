#!/usr/bin/env python3
"""
Deep Research System - Main Entry Point
A comprehensive research automation system using Crew AI with multiple specialized agents.
"""

import os
import sys
import argparse
from typing import Dict, Any
from deep_research_system.research_system import DeepResearchSystem

def main():
    """Main entry point for the Deep Research System"""
    parser = argparse.ArgumentParser(
        description="Deep Research System using Crew AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --topic "artificial intelligence trends 2024"
  python main.py --topic "climate change impact" --depth expert --audience academic
  python main.py --topic "blockchain technology" --format html --no-save
  python main.py --topic "AI in healthcare" --provider anthropic
        """
    )
    
    parser.add_argument(
        "--topic", 
        required=False,  # Changed from True to False
        help="Research topic to investigate"
    )
    
    parser.add_argument(
        "--depth",
        choices=["basic", "comprehensive", "expert"],
        default="comprehensive",
        help="Research depth level (default: comprehensive)"
    )
    
    parser.add_argument(
        "--audience",
        choices=["general", "academic", "business", "technical"],
        default="general",
        help="Target audience for the report (default: general)"
    )
    
    parser.add_argument(
        "--format",
        choices=["markdown", "html", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "google"],
        help="AI provider to use (default: from PREFERRED_AI_PROVIDER env var)"
    )
    
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save results to file"
    )
    
    parser.add_argument(
        "--api-keys",
        help="Path to JSON file containing API keys"
    )
    
    parser.add_argument(
        "--show-providers",
        action="store_true",
        help="Show available AI providers and exit"
    )
    
    args = parser.parse_args()
    
    # Check if topic is required but not provided
    if not args.show_providers and not args.topic:
        parser.error("--topic is required unless --show-providers is specified")
    
    try:
        # Load API keys if provided
        api_keys = None
        if args.api_keys:
            import json
            with open(args.api_keys, 'r') as f:
                api_keys = json.load(f)
        
        # Set preferred provider if specified
        if args.provider:
            os.environ["PREFERRED_AI_PROVIDER"] = args.provider
        
        # Initialize the research system
        print("🔧 Initializing Deep Research System...")
        research_system = DeepResearchSystem(api_keys=api_keys)
        
        # Show available providers if requested
        if args.show_providers:
            provider_info = research_system.get_provider_info()
            print("\n🤖 Available AI Providers:")
            print("="*40)
            for provider, is_available in provider_info["available_providers"].items():
                status = "✅ Available" if is_available else "❌ Not Available"
                print(f"  {provider.upper()}: {status}")
            print(f"\nPreferred Provider: {provider_info['preferred_provider'].upper()}")
            print(f"Current Model: {provider_info['current_model']}")
            return 0
        
        # Conduct research
        results = research_system.conduct_research(
            topic=args.topic,
            research_depth=args.depth,
            target_audience=args.audience,
            output_format=args.format,
            save_results=not args.no_save
        )
        
        # Display results summary
        print("\n" + "="*60)
        print("📊 RESEARCH COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Topic: {results['topic']}")
        print(f"Research Depth: {results['research_depth']}")
        print(f"Target Audience: {results['target_audience']}")
        print(f"AI Provider: {results['ai_provider'].upper()}")
        print(f"AI Model: {results['ai_model']}")
        print(f"Execution Time: {results['execution_time']:.2f} seconds")
        print(f"Timestamp: {results['timestamp']}")
        
        if not args.no_save:
            print(f"\n💾 Results saved to research_outputs/ directory")
        
        print("\n" + "="*60)
        print("📋 EXECUTIVE SUMMARY")
        print("="*60)
        print(results['summary'])
        
        print("\n" + "="*60)
        print("🔍 KEY FINDINGS")
        print("="*60)
        for i, finding in enumerate(results['key_findings'], 1):
            print(f"{i}. {finding}")
        
        print("\n" + "="*60)
        print("💡 RECOMMENDATIONS")
        print("="*60)
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"{i}. {rec}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ Research interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 