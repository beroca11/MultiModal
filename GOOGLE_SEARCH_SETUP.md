# Google Custom Search API Setup Guide

This guide will help you set up Google Custom Search API as an alternative to Travily for web search functionality in your MultiModalMind project.

## Overview

Google Custom Search API provides access to Google's search results through a customizable search engine. It's a reliable alternative to Travily with good rate limits and high-quality results.

## Prerequisites

- Google Cloud Platform account
- Billing enabled on your Google Cloud project
- Basic familiarity with Google Cloud Console

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter a project name (e.g., "multimodalmind-search")
4. Click "Create"

### 2. Enable the Custom Search API

1. In your Google Cloud project, go to the [API Library](https://console.cloud.google.com/apis/library)
2. Search for "Custom Search API"
3. Click on "Custom Search API"
4. Click "Enable"

### 3. Create API Credentials

1. Go to [Credentials](https://console.cloud.google.com/apis/credentials)
2. Click "Create Credentials" → "API Key"
3. Copy the generated API key
4. (Optional) Click "Restrict Key" to limit usage to Custom Search API only

### 4. Create a Custom Search Engine

1. Go to [Google Programmable Search Engine](https://programmablesearchengine.google.com/about/)
2. Click "Create a search engine"
3. Enter any website URL (e.g., `https://example.com`)
4. Give your search engine a name (e.g., "MultiModalMind Search")
5. Click "Create"
6. Click "Customize" on your new search engine
7. Go to "Search the entire web" section
8. Turn ON "Search the entire web"
9. Click "Save"
10. Copy the Search Engine ID (cx parameter)

### 5. Configure Your Environment

Add the following to your `.env` file:

```bash
# Google Custom Search API
GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
```

### 6. Test the Integration

Run the following command to test your Google Search API setup:

```bash
python -c "
from deep_research_system.tools.search_tools import web_search_tool
results = web_search_tool._run('artificial intelligence trends 2024', max_results=3, preferred_engine='google')
for result in results:
    print(f'Title: {result.title}')
    print(f'URL: {result.url}')
    print(f'Source: {result.source}')
    print('---')
"
```

## Usage Examples

### Basic Search

```python
from deep_research_system.tools.search_tools import web_search_tool

# Search using Google Custom Search API
results = web_search_tool._run(
    query="machine learning applications",
    max_results=5,
    preferred_engine="google"
)

for result in results:
    print(f"Title: {result.title}")
    print(f"URL: {result.url}")
    print(f"Snippet: {result.snippet}")
    print("---")
```

### Auto-Fallback Search

```python
# The system will automatically try Google first, then fall back to other engines
results = web_search_tool._run(
    query="latest AI developments",
    max_results=5,
    preferred_engine="auto"  # Will try Google if available, then others
)
```

### Research System Integration

```python
from deep_research_system.research_system import DeepResearchSystem

# Initialize with Google Search preference
research_system = DeepResearchSystem()

# Conduct research (will use Google Search when available)
results = research_system.conduct_research(
    topic="quantum computing advances",
    research_depth="comprehensive",
    target_audience="technical"
)
```

## API Limits and Pricing

### Free Tier
- 100 searches per day
- No cost for the first 100 searches

### Paid Tier
- $5 per 1,000 searches
- Additional searches beyond the free tier

### Rate Limits
- 10,000 searches per day per project
- 100 searches per 100 seconds per user

## Troubleshooting

### Common Issues

1. **"API key not valid" error**
   - Ensure you've enabled the Custom Search API
   - Check that your API key is correct
   - Verify billing is enabled on your project

2. **"Search engine not found" error**
   - Verify your Search Engine ID is correct
   - Ensure "Search the entire web" is enabled
   - Check that your search engine is active

3. **"Quota exceeded" error**
   - Check your daily quota usage in Google Cloud Console
   - Consider upgrading to paid tier if needed
   - The system will automatically fall back to other search engines

4. **No results returned**
   - Try a different search query
   - Check if your search engine is configured correctly
   - Verify the search engine is set to search the entire web

### Debug Mode

Enable debug logging to see which search engines are being used:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from deep_research_system.tools.search_tools import web_search_tool
results = web_search_tool._run("test query", preferred_engine="google")
```

## Comparison with Other Search APIs

| Feature | Google CSE | Travily | Serper.dev | DuckDuckGo |
|---------|------------|---------|------------|------------|
| **Cost** | $5/1000 searches | $10/month | $50/month | Free |
| **Free Tier** | 100/day | Limited | Limited | Unlimited |
| **Quality** | Excellent | Good | Good | Good |
| **Rate Limits** | 10K/day | High | High | Low |
| **Setup Complexity** | Medium | Easy | Easy | Easy |
| **Reliability** | Very High | High | High | Medium |

## Best Practices

1. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables
   - Restrict API keys to specific services

2. **Cost Optimization**
   - Monitor your usage in Google Cloud Console
   - Use appropriate search result limits
   - Implement caching for repeated queries

3. **Error Handling**
   - Always implement fallback search engines
   - Handle rate limit errors gracefully
   - Log search failures for debugging

4. **Search Quality**
   - Use specific, targeted search queries
   - Leverage the relevance scoring
   - Combine with other search sources for comprehensive results

## Integration with Your Project

The Google Custom Search API is now fully integrated into your MultiModalMind project. The system will:

1. **Automatically detect** if Google Search API is configured
2. **Prioritize Google results** when available
3. **Fall back gracefully** to other search engines if needed
4. **Provide consistent results** across all search engines

## Next Steps

1. Test your setup with the provided examples
2. Monitor your API usage in Google Cloud Console
3. Consider setting up billing alerts
4. Explore advanced features like site-specific searches
5. Integrate with your existing research workflows

## Support

If you encounter issues:

1. Check the [Google Custom Search API documentation](https://developers.google.com/custom-search/v1/overview)
2. Review your Google Cloud Console for quota and billing information
3. Test with the provided debugging examples
4. Check the system logs for detailed error messages

The Google Custom Search API provides a robust, reliable alternative to Travily with excellent search quality and reasonable pricing for most use cases. 