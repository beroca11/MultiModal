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
    
    def _run(self, query: str, max_results: int = 5) -> List[SearchResult]:
        results = []
        
        # Try Tavily first if available
        if Config.TAVILY_API_KEY:
            try:
                tavily_results = self._tavily_search(query, max_results)
                results.extend(tavily_results)
            except Exception as e:
                print(f"Tavily search failed: {e}")
        
        # Fallback to DuckDuckGo
        if len(results) < max_results:
            try:
                ddg_results = self._duckduckgo_search(query, max_results - len(results))
                results.extend(ddg_results)
            except Exception as e:
                print(f"DuckDuckGo search failed: {e}")
        
        return results[:max_results]
    
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