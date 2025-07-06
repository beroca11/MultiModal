"""
Search tools for comprehensive research data collection
"""
import requests
import json
from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
import wikipedia
import arxiv
from scholarly import scholarly
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from deep_research_system.config import Config

class SearchResult(BaseModel):
    """Model for search results"""
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float = 0.0
    content: Optional[str] = None

class WebSearchTool(BaseTool):
    """Tool for web search using multiple engines"""
    name = "web_search"
    description = "Search the web for current information on a topic"
    
    class InputSchema(BaseModel):
        query: str = Field(description="Search query")
        max_results: int = Field(default=5, description="Maximum number of results")
        preferred_engine: str = Field(default="auto", description="Preferred search engine: tavily, serper, google, brave, duckduckgo, or auto")
    
    def _run(self, query: str, max_results: int = 5, preferred_engine: str = "auto") -> List[SearchResult]:
        results = []
        
        # Determine search order based on preference and availability
        search_engines = self._get_search_engines(preferred_engine)
        
        for engine in search_engines:
            if len(results) >= max_results:
                break
                
            try:
                if engine == "tavily" and Config.TAVILY_API_KEY:
                    engine_results = self._tavily_search(query, max_results - len(results))
                    results.extend(engine_results)
                elif engine == "serper" and Config.SERPER_API_KEY:
                    engine_results = self._serper_search(query, max_results - len(results))
                    results.extend(engine_results)
                elif engine == "google" and Config.GOOGLE_SEARCH_API_KEY:
                    engine_results = self._google_search(query, max_results - len(results))
                    results.extend(engine_results)
                elif engine == "brave" and Config.BRAVE_API_KEY:
                    engine_results = self._brave_search(query, max_results - len(results))
                    results.extend(engine_results)
                elif engine == "duckduckgo":
                    engine_results = self._duckduckgo_search(query, max_results - len(results))
                    results.extend(engine_results)
            except Exception as e:
                print(f"{engine.capitalize()} search failed: {e}")
                continue
        
        return results[:max_results]
    
    def _get_search_engines(self, preferred: str) -> List[str]:
        """Get ordered list of search engines to try"""
        if preferred != "auto":
            # Use preferred engine first, then fallbacks
            engines = [preferred]
            if preferred != "duckduckgo":
                engines.append("duckduckgo")  # Always include as fallback
            return engines
        
        # Auto mode: try based on availability
        engines = []
        
        # Priority order based on quality and availability
        if Config.TAVILY_API_KEY:
            engines.append("tavily")
        if Config.SERPER_API_KEY:
            engines.append("serper")
        if Config.GOOGLE_SEARCH_API_KEY:
            engines.append("google")
        if Config.BRAVE_API_KEY:
            engines.append("brave")
        
        # Always include DuckDuckGo as fallback
        engines.append("duckduckgo")
        
        return engines
    
    def _tavily_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Tavily API"""
        url = "https://api.tavily.com/search"
        headers = {"api-key": Config.TAVILY_API_KEY}
        params = {
            "query": query,
            "max_results": max_results,
            "search_depth": "advanced"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("results", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("content", ""),
                source="tavily",
                relevance_score=item.get("score", 0.0)
            ))
        
        return results
    
    def _serper_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Serper.dev API"""
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": Config.SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": max_results
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("organic", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source="serper",
                relevance_score=0.8
            ))
        
        return results
    
    def _google_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": Config.GOOGLE_SEARCH_API_KEY,
            "cx": Config.GOOGLE_SEARCH_ENGINE_ID,
            "q": query,
            "num": min(max_results, 10)  # Google CSE max is 10
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("items", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source="google",
                relevance_score=0.9
            ))
        
        return results
    
    def _brave_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using Brave Search API"""
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": Config.BRAVE_API_KEY
        }
        params = {
            "q": query,
            "count": max_results
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get("web", {}).get("results", []):
            results.append(SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("description", ""),
                source="brave",
                relevance_score=0.8
            ))
        
        return results
    
    def _duckduckgo_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search using DuckDuckGo"""
        results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)
            for result in search_results:
                results.append(SearchResult(
                    title=result.get("title", ""),
                    url=result.get("link", ""),
                    snippet=result.get("body", ""),
                    source="duckduckgo"
                ))
        return results

class AcademicSearchTool(BaseTool):
    """Tool for academic research using multiple sources"""
    name = "academic_search"
    description = "Search academic papers and research publications"
    
    class InputSchema(BaseModel):
        query: str = Field(description="Academic search query")
        max_results: int = Field(default=5, description="Maximum number of results")
        source: str = Field(default="all", description="Source: arxiv, scholarly, wikipedia, or all")
    
    def _run(self, query: str, max_results: int = 5, source: str = "all") -> List[SearchResult]:
        results = []
        
        if source in ["arxiv", "all"]:
            try:
                arxiv_results = self._arxiv_search(query, max_results // 2)
                results.extend(arxiv_results)
            except Exception as e:
                print(f"ArXiv search failed: {e}")
        
        if source in ["scholarly", "all"]:
            try:
                scholarly_results = self._scholarly_search(query, max_results // 2)
                results.extend(scholarly_results)
            except Exception as e:
                print(f"Scholarly search failed: {e}")
        
        if source in ["wikipedia", "all"]:
            try:
                wiki_results = self._wikipedia_search(query, max_results // 3)
                results.extend(wiki_results)
            except Exception as e:
                print(f"Wikipedia search failed: {e}")
        
        return results[:max_results]
    
    def _arxiv_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search arXiv for papers"""
        results = []
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        for result in search.results():
            results.append(SearchResult(
                title=result.title,
                url=result.entry_id,
                snippet=result.summary,
                source="arxiv",
                relevance_score=0.8
            ))
        
        return results
    
    def _scholarly_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search Google Scholar"""
        results = []
        search_query = scholarly.search_pubs(query)
        
        for i, pub in enumerate(search_query):
            if i >= max_results:
                break
            results.append(SearchResult(
                title=pub.get("bib", {}).get("title", ""),
                url=pub.get("pub_url", ""),
                snippet=pub.get("bib", {}).get("abstract", ""),
                source="scholarly",
                relevance_score=0.7
            ))
        
        return results
    
    def _wikipedia_search(self, query: str, max_results: int) -> List[SearchResult]:
        """Search Wikipedia"""
        results = []
        try:
            # Search for pages
            search_results = wikipedia.search(query, results=max_results)
            
            for title in search_results:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    results.append(SearchResult(
                        title=page.title,
                        url=page.url,
                        snippet=page.summary[:500] + "..." if len(page.summary) > 500 else page.summary,
                        source="wikipedia",
                        relevance_score=0.6
                    ))
                except:
                    continue
        except Exception as e:
            print(f"Wikipedia search error: {e}")
        
        return results

class ContentExtractionTool(BaseTool):
    """Tool for extracting content from URLs"""
    name = "content_extraction"
    description = "Extract and summarize content from web pages"
    
    class InputSchema(BaseModel):
        url: str = Field(description="URL to extract content from")
        max_length: int = Field(default=2000, description="Maximum content length")
    
    def _run(self, url: str, max_length: int = 2000) -> Dict[str, Any]:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Truncate if too long
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return {
                "url": url,
                "title": soup.title.string if soup.title else "",
                "content": text,
                "word_count": len(text.split()),
                "extraction_success": True
            }
            
        except Exception as e:
            return {
                "url": url,
                "content": f"Failed to extract content: {str(e)}",
                "extraction_success": False
            }

# Tool instances
web_search_tool = WebSearchTool()
academic_search_tool = AcademicSearchTool()
content_extraction_tool = ContentExtractionTool()

# Export all tools
__all__ = [
    "WebSearchTool",
    "AcademicSearchTool", 
    "ContentExtractionTool",
    "SearchResult",
    "web_search_tool",
    "academic_search_tool",
    "content_extraction_tool"
] 