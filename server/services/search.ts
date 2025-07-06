export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
  displayUrl: string;
  source?: string;
  relevanceScore?: number;
}

export interface SearchResponse {
  results: SearchResult[];
  query: string;
  totalResults: number;
}

export async function performWebSearch(query: string): Promise<SearchResponse> {
  // Try Google Custom Search API first
  if (process.env.GOOGLE_SEARCH_API_KEY && process.env.GOOGLE_SEARCH_ENGINE_ID) {
    try {
      return await performGoogleSearch(query);
    } catch (error) {
      console.warn("Google Search failed, trying fallback:", error);
    }
  }

  // Try Serper.dev API as fallback
  const serperApiKey = process.env.SERPAPI_KEY || process.env.SERP_API_KEY || process.env.SERPER_API_KEY;
  if (serperApiKey) {
    try {
      return await performSerperSearch(query);
    } catch (error) {
      console.warn("Serper search failed:", error);
    }
  }

  // Try Tavily API as fallback
  if (process.env.TAVILY_API_KEY) {
    try {
      return await performTavilySearch(query);
    } catch (error) {
      console.warn("Tavily search failed:", error);
    }
  }

  throw new Error("No search API configured");
}

async function performGoogleSearch(query: string): Promise<SearchResponse> {
  const url = "https://www.googleapis.com/customsearch/v1";
  const params = new URLSearchParams({
    key: process.env.GOOGLE_SEARCH_API_KEY!,
    cx: process.env.GOOGLE_SEARCH_ENGINE_ID!,
    q: query,
    num: "5"
  });

  const response = await fetch(`${url}?${params}`);
  
  if (!response.ok) {
    throw new Error(`Google Search API error: ${response.statusText}`);
  }

  const data = await response.json();
  
  const results: SearchResult[] = (data.items || []).map((item: any) => ({
    title: item.title || '',
    url: item.link || '',
    snippet: item.snippet || '',
    displayUrl: item.displayLink || item.link || '',
    source: 'google',
    relevanceScore: 0.9
  }));

  return {
    results,
    query,
    totalResults: data.searchInformation?.totalResults || 0
  };
}

async function performSerperSearch(query: string): Promise<SearchResponse> {
  const apiKey = process.env.SERPAPI_KEY || process.env.SERP_API_KEY || process.env.SERPER_API_KEY;
  
  const response = await fetch(`https://serpapi.com/search.json?q=${encodeURIComponent(query)}&api_key=${apiKey}&num=5`);
  
  if (!response.ok) {
    throw new Error(`SerpAPI error: ${response.statusText}`);
  }

  const data = await response.json();
  
  const results: SearchResult[] = (data.organic_results || []).map((result: any) => ({
    title: result.title || '',
    url: result.link || '',
    snippet: result.snippet || '',
    displayUrl: result.displayed_link || result.link || '',
    source: 'serper',
    relevanceScore: 0.8
  }));

  return {
    results,
    query,
    totalResults: data.search_information?.total_results || 0
  };
}

async function performTavilySearch(query: string): Promise<SearchResponse> {
  const url = "https://api.tavily.com/search";
  const headers = { "api-key": process.env.TAVILY_API_KEY! };
  const params = new URLSearchParams({
    query,
    max_results: "5",
    search_depth: "advanced"
  });

  const response = await fetch(`${url}?${params}`, { headers });
  
  if (!response.ok) {
    throw new Error(`Tavily API error: ${response.statusText}`);
  }

  const data = await response.json();
  
  const results: SearchResult[] = (data.results || []).map((item: any) => ({
    title: item.title || '',
    url: item.url || '',
    snippet: item.content || '',
    displayUrl: item.url || '',
    source: 'tavily',
    relevanceScore: item.score || 0.7
  }));

  return {
    results,
    query,
    totalResults: results.length
  };
}

import fetch from "node-fetch";

async function getSearchAgentSummary(query: string, results: SearchResult[], model: string = "gpt-4o") {
  const response = await fetch("http://localhost:8000/summarize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      results: results.map(r => ({
        title: r.title,
        snippet: r.snippet,
        url: r.url,
      })),
      model: model
    }),
  });
  if (!response.ok) throw new Error("Failed to get search agent summary");
  return await response.json();
}

export async function searchAndSummarize(query: string, model: string = "gpt-4o"): Promise<{ searchResults: SearchResponse; summary: string; modelUsed: string }> {
  const searchResults = await performWebSearch(query);
  const summaryResponse = await getSearchAgentSummary(query, searchResults.results, model);
  
  return {
    searchResults,
    summary: summaryResponse.summary,
    modelUsed: summaryResponse.model_used
  };
}
