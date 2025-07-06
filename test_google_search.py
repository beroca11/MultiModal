#!/usr/bin/env python3
"""
Test script for Google Custom Search API integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_search_api():
    """Test the Google Search API integration"""
    print("🔍 Testing Google Custom Search API Integration")
    print("=" * 50)
    
    # Check if API keys are configured
    google_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
    google_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    if not google_api_key:
        print("❌ GOOGLE_SEARCH_API_KEY not found in environment variables")
        print("   Please add it to your .env file")
        return False
    
    if not google_engine_id:
        print("❌ GOOGLE_SEARCH_ENGINE_ID not found in environment variables")
        print("   Please add it to your .env file")
        return False
    
    print("✅ API keys found in environment")
    
    try:
        # Import the search tool
        from deep_research_system.tools.search_tools import web_search_tool
        
        print("✅ Search tool imported successfully")
        
        # Test search
        print("\n🔎 Testing search functionality...")
        test_query = "artificial intelligence trends 2024"
        
        results = web_search_tool._run(
            query=test_query,
            max_results=3,
            preferred_engine="google"
        )
        
        if not results:
            print("❌ No results returned from Google Search API")
            return False
        
        print(f"✅ Search successful! Found {len(results)} results")
        
        # Display results
        print("\n📋 Search Results:")
        print("-" * 30)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.title}")
            print(f"   URL: {result.url}")
            print(f"   Source: {result.source}")
            print(f"   Relevance: {result.relevance_score}")
            print(f"   Snippet: {result.snippet[:100]}...")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're in the correct directory and dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return False

def test_fallback_search():
    """Test fallback to other search engines"""
    print("\n🔄 Testing Fallback Search")
    print("=" * 30)
    
    try:
        from deep_research_system.tools.search_tools import web_search_tool
        
        # Test auto mode (should try Google first, then fallback)
        results = web_search_tool._run(
            query="machine learning applications",
            max_results=2,
            preferred_engine="auto"
        )
        
        if results:
            print(f"✅ Fallback search successful! Found {len(results)} results")
            print(f"   Sources used: {[r.source for r in results]}")
            return True
        else:
            print("❌ No results from fallback search")
            return False
            
    except Exception as e:
        print(f"❌ Error during fallback search: {e}")
        return False

def test_search_engines_availability():
    """Test which search engines are available"""
    print("\n🔧 Testing Search Engine Availability")
    print("=" * 40)
    
    from deep_research_system.config import Config
    
    engines = {
        "Tavily": bool(Config.TAVILY_API_KEY),
        "Serper.dev": bool(Config.SERPER_API_KEY),
        "Google Custom Search": bool(Config.GOOGLE_SEARCH_API_KEY),
        "Brave Search": bool(Config.BRAVE_API_KEY),
        "DuckDuckGo": True  # Always available
    }
    
    print("Available search engines:")
    for engine, available in engines.items():
        status = "✅" if available else "❌"
        print(f"   {status} {engine}")
    
    available_count = sum(engines.values())
    print(f"\nTotal available engines: {available_count}")
    
    return available_count > 0

def main():
    """Run all tests"""
    print("🚀 MultiModalMind - Google Search API Test Suite")
    print("=" * 60)
    
    # Test 1: Google Search API
    google_test = test_google_search_api()
    
    # Test 2: Fallback search
    fallback_test = test_fallback_search()
    
    # Test 3: Engine availability
    availability_test = test_search_engines_availability()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Google Search API: {'✅ PASS' if google_test else '❌ FAIL'}")
    print(f"Fallback Search: {'✅ PASS' if fallback_test else '❌ FAIL'}")
    print(f"Engine Availability: {'✅ PASS' if availability_test else '❌ FAIL'}")
    
    if google_test and fallback_test and availability_test:
        print("\n🎉 All tests passed! Google Search API is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Use 'preferred_engine=\"google\"' for Google-only searches")
        print("   2. Use 'preferred_engine=\"auto\"' for automatic fallback")
        print("   3. Monitor your API usage in Google Cloud Console")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        print("\n🔧 Troubleshooting:")
        print("   1. Verify your API keys in .env file")
        print("   2. Check Google Cloud Console for API status")
        print("   3. Ensure billing is enabled on your Google Cloud project")
        print("   4. Verify your Custom Search Engine is configured correctly")

if __name__ == "__main__":
    main() 