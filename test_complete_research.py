#!/usr/bin/env python3
"""
Complete Research Test Script
Tests the full research pipeline with a simple topic
"""

import os
import sys
from deep_research_system.research_system import DeepResearchSystem

def test_complete_research():
    """Test the complete research pipeline"""
    print("🧪 Testing Complete Research Pipeline")
    print("="*50)
    
    try:
        # Initialize the system
        print("🔧 Initializing Deep Research System...")
        research_system = DeepResearchSystem()
        
        # Test with a simple topic
        topic = "python programming basics"
        print(f"🎯 Research Topic: {topic}")
        
        # Conduct research
        results = research_system.conduct_research(
            topic=topic,
            research_depth="basic",
            target_audience="general",
            output_format="markdown",
            save_results=True
        )
        
        # Display results
        print("\n" + "="*50)
        print("✅ RESEARCH COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"Topic: {results['topic']}")
        print(f"AI Provider: {results['ai_provider'].upper()}")
        print(f"AI Model: {results['ai_model']}")
        print(f"Execution Time: {results['execution_time']:.2f} seconds")
        print(f"Research Depth: {results['research_depth']}")
        
        print("\n📋 EXECUTIVE SUMMARY:")
        print("-" * 30)
        print(results['summary'][:300] + "..." if len(results['summary']) > 300 else results['summary'])
        
        print(f"\n🔍 Key Findings ({len(results['key_findings'])} found):")
        for i, finding in enumerate(results['key_findings'], 1):
            print(f"  {i}. {finding}")
        
        print(f"\n💡 Recommendations ({len(results['recommendations'])} found):")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        print(f"\n💾 Results saved to research_outputs/ directory")
        print("🎉 Complete research pipeline test successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during research: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_complete_research()
    sys.exit(0 if success else 1) 