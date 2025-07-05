#!/usr/bin/env python3
"""
Example Usage of the Deep Research System
Demonstrates how to use the system programmatically for various research scenarios.
"""

import os
import json
from deep_research_system.research_system import DeepResearchSystem

def example_basic_research():
    """Example of basic research on a simple topic"""
    print("🔍 Example 1: Basic Research")
    print("="*50)
    
    # Initialize the system
    research_system = DeepResearchSystem()
    
    # Conduct basic research
    results = research_system.conduct_research(
        topic="renewable energy trends",
        research_depth="basic",
        target_audience="general",
        output_format="markdown"
    )
    
    print(f"✅ Research completed in {results['execution_time']:.2f} seconds")
    print(f"📄 Summary: {results['summary'][:200]}...")
    
    return results

def example_comprehensive_research():
    """Example of comprehensive research on a complex topic"""
    print("\n🔬 Example 2: Comprehensive Research")
    print("="*50)
    
    # Initialize the system
    research_system = DeepResearchSystem()
    
    # Conduct comprehensive research
    results = research_system.conduct_research(
        topic="artificial intelligence in healthcare",
        research_depth="comprehensive",
        target_audience="business",
        output_format="html"
    )
    
    print(f"✅ Research completed in {results['execution_time']:.2f} seconds")
    print(f"📄 Summary: {results['summary'][:200]}...")
    
    return results

def example_expert_research():
    """Example of expert-level research with custom API keys"""
    print("\n🎓 Example 3: Expert Research")
    print("="*50)
    
    # Example API keys (replace with your actual keys)
    api_keys = {
        "OPENAI_API_KEY": "your_openai_key_here",
        "TAVILY_API_KEY": "your_tavily_key_here"
    }
    
    # Initialize the system with custom API keys
    research_system = DeepResearchSystem(api_keys=api_keys)
    
    # Conduct expert research
    results = research_system.conduct_research(
        topic="quantum computing applications in cryptography",
        research_depth="expert",
        target_audience="academic",
        output_format="json"
    )
    
    print(f"✅ Research completed in {results['execution_time']:.2f} seconds")
    print(f"📄 Summary: {results['summary'][:200]}...")
    
    return results

def example_batch_research():
    """Example of conducting multiple research projects"""
    print("\n📚 Example 4: Batch Research")
    print("="*50)
    
    # Initialize the system
    research_system = DeepResearchSystem()
    
    # List of topics to research
    topics = [
        "blockchain technology trends",
        "machine learning in finance",
        "sustainable urban development"
    ]
    
    all_results = []
    
    for i, topic in enumerate(topics, 1):
        print(f"\n🔍 Researching topic {i}/{len(topics)}: {topic}")
        
        try:
            results = research_system.conduct_research(
                topic=topic,
                research_depth="comprehensive",
                target_audience="general",
                output_format="markdown",
                save_results=True
            )
            all_results.append(results)
            print(f"✅ Completed: {topic}")
        except Exception as e:
            print(f"❌ Failed: {topic} - {str(e)}")
    
    # Export all results
    research_system.export_research_history("batch_research_history.json")
    print(f"\n📚 Batch research completed. {len(all_results)} successful research projects.")
    
    return all_results

def example_custom_research():
    """Example of custom research with specific parameters"""
    print("\n⚙️ Example 5: Custom Research")
    print("="*50)
    
    # Initialize the system
    research_system = DeepResearchSystem()
    
    # Custom research parameters
    custom_params = {
        "topic": "cybersecurity threats in 2024",
        "research_depth": "comprehensive",
        "target_audience": "technical",
        "output_format": "html",
        "save_results": True
    }
    
    print(f"🎯 Research Topic: {custom_params['topic']}")
    print(f"📊 Research Depth: {custom_params['research_depth']}")
    print(f"👥 Target Audience: {custom_params['target_audience']}")
    
    # Conduct research
    results = research_system.conduct_research(**custom_params)
    
    print(f"✅ Research completed in {results['execution_time']:.2f} seconds")
    print(f"📄 Summary: {results['summary'][:200]}...")
    
    # Display key findings
    print(f"\n🔍 Key Findings ({len(results['key_findings'])} found):")
    for i, finding in enumerate(results['key_findings'], 1):
        print(f"  {i}. {finding}")
    
    return results

def example_research_analysis():
    """Example of analyzing research history and patterns"""
    print("\n📊 Example 6: Research Analysis")
    print("="*50)
    
    # Initialize the system
    research_system = DeepResearchSystem()
    
    # Conduct a few research projects first
    topics = ["AI ethics", "climate change solutions", "digital transformation"]
    
    for topic in topics:
        print(f"🔍 Researching: {topic}")
        research_system.conduct_research(
            topic=topic,
            research_depth="basic",
            save_results=False
        )
    
    # Analyze research history
    history = research_system.get_research_history()
    
    print(f"\n📚 Research History Analysis:")
    print(f"  Total Research Projects: {len(history)}")
    
    if history:
        # Calculate average execution time
        avg_time = sum(h['results']['execution_time'] for h in history) / len(history)
        print(f"  Average Execution Time: {avg_time:.2f} seconds")
        
        # Show topics researched
        print(f"  Topics Researched:")
        for i, entry in enumerate(history, 1):
            print(f"    {i}. {entry['topic']} ({entry['results']['research_depth']})")
    
    return history

def main():
    """Run all examples"""
    print("🚀 Deep Research System - Example Usage")
    print("="*60)
    print("This script demonstrates various ways to use the Deep Research System.")
    print("Note: Some examples require valid API keys to work properly.")
    print("="*60)
    
    try:
        # Run examples
        example_basic_research()
        example_comprehensive_research()
        # example_expert_research()  # Uncomment if you have API keys
        example_batch_research()
        example_custom_research()
        example_research_analysis()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("📁 Check the 'research_outputs' directory for saved results.")
        print("📚 Research history exported to 'research_history.json'")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        print("💡 Make sure you have set up your API keys properly.")

if __name__ == "__main__":
    main() 