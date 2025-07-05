export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
  displayUrl: string;
}

export interface SearchResponse {
  results: SearchResult[];
  query: string;
  totalResults: number;
}

export async function performWebSearch(query: string): Promise<SearchResponse> {
  const apiKey = process.env.SERPAPI_KEY || process.env.SERP_API_KEY || process.env.SERPER_API_KEY;
  
  if (!apiKey) {
    throw new Error("SerpAPI key not configured");
  }

  try {
    const response = await fetch(`https://serpapi.com/search.json?q=${encodeURIComponent(query)}&api_key=${apiKey}&num=5`);
    
    if (!response.ok) {
      throw new Error(`Search API error: ${response.statusText}`);
    }

    const data = await response.json();
    
    const results: SearchResult[] = (data.organic_results || []).map((result: any) => ({
      title: result.title || '',
      url: result.link || '',
      snippet: result.snippet || '',
      displayUrl: result.displayed_link || result.link || ''
    }));

    return {
      results,
      query,
      totalResults: data.search_information?.total_results || 0
    };
  } catch (error) {
    throw new Error(`Web search failed: ${error instanceof Error ? error.message : String(error)}`);
  }
}

export async function searchAndSummarize(query: string, model: string = "gpt-4o"): Promise<{ searchResults: SearchResponse; summary: string }> {
  const searchResults = await performWebSearch(query);
  
  const searchContext = searchResults.results.map(result => 
    `${result.title}\n${result.snippet}\nURL: ${result.url}`
  ).join('\n\n');

  const summaryPrompt = `Based on these web search results for "${query}", provide a comprehensive summary:

${searchContext}

Please synthesize the information and provide key insights, trends, and important findings.`;

  // Import AI functions
  const { generateWithGPT4o, generateWithClaude, generateWithGemini } = await import('./ai');

  let summary = "";
  try {
    switch (model) {
      case "gpt-4o":
        const gptResponse = await generateWithGPT4o(summaryPrompt);
        summary = gptResponse.content;
        break;
      case "claude":
        const claudeResponse = await generateWithClaude(summaryPrompt);
        summary = claudeResponse.content;
        break;
      case "gemini":
        const geminiResponse = await generateWithGemini(summaryPrompt);
        summary = geminiResponse.content;
        break;
      default:
        const defaultResponse = await generateWithGPT4o(summaryPrompt);
        summary = defaultResponse.content;
    }
  } catch (error) {
    summary = `Error generating summary: ${error instanceof Error ? error.message : String(error)}`;
  }

  return {
    searchResults,
    summary
  };
}
