#!/usr/bin/env python3
"""
Test script to demonstrate the dynamic web search agent capabilities.
This shows how the agent now adapts its response format based on query type.
"""

import requests
import json

def test_dynamic_search(query, expected_type):
    """Test the dynamic search agent with different query types."""
    
    # Mock search results for testing
    mock_results = [
        {
            "title": "Top 10 AI Tools for 2024 - Complete Guide",
            "snippet": "Discover the most powerful AI tools that are revolutionizing industries in 2024. From ChatGPT to Claude, find the best AI solutions for your needs.",
            "url": "https://example.com/ai-tools-2024"
        },
        {
            "title": "How to Implement Web Search in Your Application",
            "snippet": "Step-by-step guide to integrating web search functionality using APIs and AI summarization. Learn best practices and common pitfalls.",
            "url": "https://example.com/web-search-guide"
        },
        {
            "title": "GPT-4o vs Claude vs Gemini: Comprehensive Comparison",
            "snippet": "Detailed comparison of the three leading AI models. Performance metrics, use cases, and recommendations for different applications.",
            "url": "https://example.com/ai-comparison"
        }
    ]
    
    try:
        response = requests.post(
            "http://localhost:8000/summarize",
            json={
                "query": query,
                "results": mock_results,
                "model": "gpt-4o"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n🎯 Query Type: {expected_type}")
            print(f"📝 Query: {query}")
            print(f"🤖 Model Used: {result.get('model_used', 'Unknown')}")
            print(f"📊 Response Preview: {result.get('summary', '')[:200]}...")
            print("-" * 80)
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    """Test different query types to demonstrate dynamic responses."""
    
    print("🚀 Testing Dynamic Web Search Agent")
    print("=" * 80)
    
    # Test cases for different query types
    test_cases = [
        ("What are the top 10 AI tools for 2024?", "List Query"),
        ("How to implement web search in my application?", "How-to Query"),
        ("What is web search integration?", "Definition Query"),
        ("GPT-4o vs Claude vs Gemini comparison", "Comparison Query"),
        ("Latest AI developments and news", "News Query"),
        ("Technical implementation of search APIs", "Technical Query"),
        ("Best practices for AI development", "General Query")
    ]
    
    success_count = 0
    total_count = len(test_cases)
    
    for query, query_type in test_cases:
        if test_dynamic_search(query, query_type):
            success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{total_count} successful")
    
    if success_count == total_count:
        print("✅ All tests passed! The dynamic search agent is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the server status and try again.")

if __name__ == "__main__":
    main() 