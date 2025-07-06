# Google Search Integration for MultiModalMind

This document describes the Google Search API integration that has been added to the MultiModalMind chat interface.

## 🎯 Overview

The Google Search integration allows users to search the web directly from the chat interface using Google's Custom Search API. The system automatically detects when web search is needed and provides relevant, up-to-date information.

## ✨ Features

### 🔍 Web Search Toggle
- **Toggle Button**: Click the "Web Search" button in the chat interface to enable web search mode
- **Visual Indicator**: The button turns green when web search is active
- **Search Panel**: When toggled, a dedicated search panel appears with additional options

### 🤖 Automatic Search Detection
The AI automatically detects when web search is needed based on keywords like:
- `search`, `latest`, `recent`, `current`
- `news`, `update`, `trend`
- `2024`, `2025` (current years)
- Questions about current events or recent developments

### 🔄 Multi-Engine Fallback
The system uses multiple search engines in order of preference:
1. **Google Custom Search API** (primary)
2. **Serper.dev API** (fallback)
3. **Tavily API** (fallback)
4. **DuckDuckGo** (final fallback)

### 📊 Enhanced Search Results
- **Source Attribution**: Shows which search engine provided each result
- **Relevance Scoring**: Displays relevance percentage for each result
- **Direct Links**: Click external links to visit source pages
- **Rich Snippets**: Shows titles, descriptions, and URLs

## 🚀 How to Use

### 1. Enable Web Search
1. Open the chat interface
2. Click the "Web Search" button (🔍 icon) in the toolbar
3. The button will turn green, indicating web search is active

### 2. Ask Questions
Simply ask questions about current events, recent developments, or any topic that might benefit from up-to-date information:

**Examples:**
- "What are the latest AI developments in 2024?"
- "Search for recent news about quantum computing"
- "What are the current trends in machine learning?"
- "Find information about the latest iPhone release"

### 3. View Results
When web search is performed, you'll see:
- **Search Results Panel**: Shows the top 3 most relevant results
- **Source Information**: Indicates which search engine was used
- **AI Summary**: The AI provides a comprehensive summary based on the search results
- **Direct Links**: Click the external link icon to visit source pages

## ⚙️ Configuration

### Environment Variables
Ensure these are set in your `.env` file:

```bash
# Google Custom Search API
GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# Fallback APIs (optional)
SERPER_API_KEY=your_serper_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Setup Instructions
1. Follow the setup guide in `GOOGLE_SEARCH_SETUP.md`
2. Configure your Google Custom Search API
3. Set the environment variables
4. Start the development server: `npm run dev`

## 🎨 User Interface

### Search Toggle Button
- **Location**: Bottom toolbar in chat interface
- **Icon**: 🔍 (Search icon)
- **Color**: Gray (inactive) → Green (active)
- **Tooltip**: "Web Search"

### Search Panel
When activated, shows:
- **Search Engine Selector**: Choose between Google, Serper.dev, or Tavily
- **Search Input**: Enter specific search queries
- **Search Button**: Manually trigger searches
- **Tips**: Helpful hints about automatic search detection

### Search Results Display
- **Source Badge**: Shows which search engine provided results
- **Result Cards**: Individual cards for each search result
- **Relevance Score**: Percentage indicating result relevance
- **External Links**: Direct links to source pages

## 🔧 Technical Details

### Backend Integration
- **File**: `server/services/search.ts`
- **Primary Engine**: Google Custom Search API
- **Fallback Logic**: Automatic fallback to other engines if primary fails
- **Error Handling**: Graceful degradation with user-friendly error messages

### Frontend Components
- **ToolPanel**: `client/src/components/chat/ToolPanel.tsx`
- **ChatInput**: `client/src/components/chat/ChatInput.tsx`
- **MessageBubble**: `client/src/components/chat/MessageBubble.tsx`

### API Endpoints
- **Search**: `POST /api/search`
- **Message with Search**: `POST /api/conversations/:id/messages`

## 🧪 Testing

Run the integration test to verify everything is working:

```bash
python test_google_integration.py
```

This will check:
- ✅ Environment setup
- ✅ Package dependencies
- ✅ Google Search API integration
- ✅ Frontend components

## 📈 Performance

### Search Engine Performance
| Engine | Speed | Quality | Cost | Reliability |
|--------|-------|---------|------|-------------|
| Google | Fast | Excellent | $5/1000 | Very High |
| Serper.dev | Fast | Good | $50/month | High |
| Tavily | Medium | Good | $10/month | High |
| DuckDuckGo | Slow | Good | Free | Medium |

### Optimization Features
- **Caching**: Results are cached to reduce API calls
- **Smart Fallback**: Only uses fallback engines when needed
- **Rate Limiting**: Respects API rate limits
- **Error Recovery**: Continues with fallback engines on errors

## 🐛 Troubleshooting

### Common Issues

**"No search API configured"**
- Check that `GOOGLE_SEARCH_API_KEY` is set in `.env`
- Verify the API key is valid and has proper permissions

**"Search engine not found"**
- Ensure `GOOGLE_SEARCH_ENGINE_ID` is correctly set
- Verify the search engine is configured to search the entire web

**"No results returned"**
- Try a different search query
- Check if the search engine is working properly
- Verify API quotas haven't been exceeded

**Frontend not showing search results**
- Check browser console for errors
- Verify the server is running properly
- Ensure all frontend components are loaded

### Debug Mode
Enable debug logging to see which search engines are being used:

```typescript
// In server/services/search.ts
console.log('Using search engine:', engine);
console.log('Search results:', results);
```

## 🔮 Future Enhancements

### Planned Features
- **Search History**: Save and reuse previous searches
- **Advanced Filters**: Filter by date, source, or content type
- **Search Analytics**: Track search performance and usage
- **Custom Search Engines**: Allow users to configure their own search engines
- **Search Suggestions**: AI-powered search query suggestions

### Potential Improvements
- **Real-time Search**: Live search results as you type
- **Search Alerts**: Get notified when new results are available
- **Search Export**: Export search results to various formats
- **Search Collaboration**: Share search results with other users

## 📚 Additional Resources

- [Google Custom Search API Documentation](https://developers.google.com/custom-search/v1/overview)
- [Serper.dev API Documentation](https://serper.dev/api-docs)
- [Tavily API Documentation](https://tavily.com/docs)
- [Setup Guide](GOOGLE_SEARCH_SETUP.md)
- [Test Script](test_google_integration.py)

## 🤝 Contributing

To contribute to the Google Search integration:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This integration is part of the MultiModalMind project and follows the same license terms.

---

**Happy Searching! 🔍✨** 