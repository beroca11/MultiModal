import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ExternalLink, Globe, Search } from "lucide-react";
import type { Message } from "@shared/schema";

interface MessageBubbleProps {
  message: Message;
}

interface SearchResult {
  title: string;
  url: string;
  snippet: string;
  displayUrl?: string;
  source?: string;
  relevanceScore?: number;
}

interface SearchResults {
  results: SearchResult[];
  query: string;
  totalResults: number;
}

// Ensure content is always a string
interface TypedMessage extends Omit<Message, 'content'> {
  content: string;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const typedMessage = message as TypedMessage;
  const isUser = typedMessage.role === "user";
  const isAssistant = typedMessage.role === "assistant";
  const [copied, setCopied] = useState(false);

  const getModelColor = (model: string | null) => {
    if (!model) return "bg-gray-500";
    
    switch (model) {
      case "gpt-4o":
        return "bg-green-500";
      case "claude-sonnet-4-20250514":
      case "claude":
        return "bg-blue-500";
      case "gemini-2.5-flash":
      case "gemini":
        return "bg-purple-500";
      case "combined":
        return "bg-gradient-to-r from-green-500 via-blue-500 to-purple-500";
      default:
        return "bg-gray-500";
    }
  };

  const getModelName = (model: string | null) => {
    if (!model) return "Unknown";
    
    switch (model) {
      case "gpt-4o":
        return "GPT-4o";
      case "claude-sonnet-4-20250514":
      case "claude":
        return "Claude Sonnet 4";
      case "gemini-2.5-flash":
      case "gemini":
        return "Gemini 2.5 Flash";
      case "combined":
        return "Combined AI";
      default:
        return model;
    }
  };

  const getSourceIcon = (source: string): JSX.Element => {
    switch (source) {
      case "google":
        return <Globe className="h-3 w-3 text-blue-500" />;
      case "serper":
        return <Search className="h-3 w-3 text-green-500" />;
      case "tavily":
        return <Search className="h-3 w-3 text-purple-500" />;
      default:
        return <Search className="h-3 w-3 text-gray-500" />;
    }
  };

  const getSourceName = (source: string): string => {
    switch (source) {
      case "google":
        return "Google Search";
      case "serper":
        return "Serper.dev";
      case "tavily":
        return "Tavily";
      default:
        return source;
    }
  };

  const hasSearchResults = typedMessage.metadata && 
    typeof typedMessage.metadata === 'object' && 
    'searchResults' in typedMessage.metadata && 
    typedMessage.metadata.searchResults;

  const searchResults = hasSearchResults ? (typedMessage.metadata as any).searchResults as SearchResults : null;

  // Helper to strip HTML tags for copying plain text
  const stripHtml = (html: string) => {
    const tmp = document.createElement("DIV");
    tmp.innerHTML = html;
    return tmp.textContent || tmp.innerText || "";
  };

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-3xl bg-teal-600 text-white rounded-2xl px-6 py-4 shadow-sm">
          <p className="text-sm leading-relaxed">{typedMessage.content}</p>
        </div>
      </div>
    );
  }

  if (isAssistant) {
    // Type guard for search summary
    const searchSummary = (typedMessage.metadata && typeof typedMessage.metadata === 'object' && 'searchSummary' in typedMessage.metadata)
      ? (typedMessage.metadata as any).searchSummary as { summary?: string; modelUsed?: string; searchResults?: SearchResults }
      : null;

    // Function to render summary with hyperlinked domain citations as pills
    const renderSummaryWithCitations = (summary: string, searchResults: SearchResults) => {
      if (!summary) return summary;
      // Convert markdown bold/italic to HTML tags
      let cleanSummary = summary
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>') // bold
        .replace(/\*(.*?)\*/g, '<i>$1</i>') // italics
        .replace(/__(.*?)__/g, '<b>$1</b>') // bold (underscore)
        .replace(/_(.*?)_/g, '<i>$1</i>') // italics (underscore)
        .replace(/`+/g, '') // backticks
        .replace(/\s*\n\s*/g, '\n'); // clean up newlines
      // Regex to match (domain.com) style citations
      const domainRegex = /\((([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})\)/g;
      // Build a map of domain to URL from searchResults
      const domainToUrl: Record<string, string> = {};
      if (searchResults?.results) {
        searchResults.results.forEach((result) => {
          try {
            const url = new URL(result.url);
            const domain = url.hostname.replace(/^www\./, '');
            domainToUrl[domain] = result.url;
          } catch {}
        });
      }
      // Replace (domain.com) with a styled clickable pill
      let renderedSummary = cleanSummary.replace(domainRegex, (match, domain) => {
        const url = domainToUrl[domain];
        if (url) {
          return `<a href=\"${url}\" target=\"_blank\" rel=\"noopener noreferrer\" class=\"inline-block px-3 py-0.5 rounded-full bg-gray-800 text-white text-xs font-inter font-medium mr-1 align-middle\" style=\"text-decoration:none;\">${domain}</a>`;
        }
        return `<span class=\"inline-block px-3 py-0.5 rounded-full bg-gray-800 text-white text-xs font-inter font-medium mr-1 align-middle\">${domain}</span>`;
      });
      // Style headings: lines starting with number+dot or ending with colon
      renderedSummary = renderedSummary.replace(/(^|\n)(\d+\.\s*<b>.*?<\/b>)/g, '$1<span class="block text-lg font-bold text-gray-900 dark:text-gray-100 mt-6 mb-2">$2</span>');
      renderedSummary = renderedSummary.replace(/(^|\n)([A-Za-z0-9 \-]+:)/g, '$1<span class="block text-base font-semibold text-gray-800 dark:text-gray-200 mt-4 mb-1">$2</span>');
      // Remove all paragraph indentation and bullet point wrapping, just wrap in div for spacing
      renderedSummary = renderedSummary.replace(/(\n|^)([^<\n][^\n]+)(?=\n|$)/g, (match, p1, p2) => {
        // Only wrap if not a heading
        if (/^\s*<span/.test(p2)) return match;
        return `${p1}<div class=\"mb-2\">${p2}</div>`;
      });
      // Remove any leftover indentation or bullet classes
      renderedSummary = renderedSummary.replace(/pl-8|list-disc|ml-6/g, '');
      return renderedSummary;
    };

    return (
      <div className="flex justify-start">
        <div className="max-w-3xl">
          {/* Model Badge */}
          <div className="flex items-center space-x-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${getModelColor(typedMessage.model)}`}></div>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {getModelName(typedMessage.model)}
            </span>
            {searchSummary && searchSummary.modelUsed && (
              <Badge variant="secondary" className="text-xs bg-emerald-100 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-300">
                <Search className="h-3 w-3 mr-1" />
                Web Search ({getModelName(searchSummary.modelUsed)})
              </Badge>
            )}
          </div>

          <Card className="bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700">
            <CardContent className="p-6">
              {/* Search Summary */}
              {searchSummary && searchSummary.summary && searchSummary.searchResults && (
                <div className="mb-8 mt-2 w-full">
                  <div className="flex items-center space-x-2 mb-6">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                      Web Search
                    </h3>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      (via {getModelName(searchSummary.modelUsed || 'Unknown')})
                    </span>
                  </div>
                  <div className="prose prose-lg max-w-none text-gray-700 dark:text-gray-300 leading-relaxed font-inter mb-8">
                    <div 
                      className="font-medium text-base leading-7 font-inter"
                      dangerouslySetInnerHTML={{
                        __html: renderSummaryWithCitations(searchSummary.summary, searchSummary.searchResults)
                      }}
                    />
                  </div>
                  {/* Feedback Buttons + Copy */}
                  <div className="flex justify-end space-x-3 mt-4">
                    <button
                      className="flex items-center px-4 py-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold shadow transition-colors"
                      title="Like this result"
                      // onClick={() => handleLike()} // Implement feedback logic as needed
                    >
                      <span className="mr-1">👍</span> Like
                    </button>
                    <button
                      className="flex items-center px-4 py-2 rounded-full bg-gray-300 hover:bg-gray-400 text-gray-800 text-sm font-semibold shadow transition-colors"
                      title="Not like this result"
                      // onClick={() => handleDislike()} // Implement feedback logic as needed
                    >
                      <span className="mr-1">👎</span> Not Like
                    </button>
                    <button
                      className="flex items-center px-4 py-2 rounded-full bg-blue-500 hover:bg-blue-600 text-white text-sm font-semibold shadow transition-colors"
                      title={copied ? "Copied!" : "Copy summary"}
                      onClick={() => {
                        const html = renderSummaryWithCitations(
                          searchSummary.summary || '',
                          searchSummary.searchResults || { results: [], query: '', totalResults: 0 }
                        );
                        const text = stripHtml(html);
                        navigator.clipboard.writeText(text);
                        setCopied(true);
                        setTimeout(() => setCopied(false), 1200);
                      }}
                    >
                      <span className="mr-1">📋</span> {copied ? "Copied!" : "Copy"}
                    </button>
                  </div>
                </div>
              )}
              
              {/* Main Content - Only show if it's different from the search summary */}
              {typedMessage.content && (!searchSummary || typedMessage.content !== searchSummary.summary) && (
                <div className="prose prose-lg dark:prose-invert max-w-none mb-6">
                  <div 
                    className="whitespace-pre-wrap text-base leading-7 text-gray-800 dark:text-gray-200 font-medium font-inter"
                  >
                    {typedMessage.content}
                  </div>
                </div>
              )}

              {/* Search Results - References at the bottom */}
              {searchSummary && searchSummary.searchResults && searchSummary.searchResults.results && searchSummary.searchResults.results.length > 0 && (
                <div className="mt-6">
                  <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 font-inter">
                    📚 References
                  </h4>
                  <div className="space-y-2">
                    {searchSummary.searchResults.results.map((result: SearchResult, index: number) => (
                      <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-200 dark:border-gray-700">
                        <span className="flex-shrink-0 w-6 h-6 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 text-xs font-semibold rounded-full flex items-center justify-center font-inter">
                          {index + 1}
                        </span>
                        <div className="flex-1 min-w-0">
                          <a
                            href={result.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm font-medium text-emerald-700 dark:text-emerald-300 hover:text-emerald-800 dark:hover:text-emerald-200 transition-colors font-inter line-clamp-2"
                          >
                            {result.title}
                          </a>
                          <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 font-inter line-clamp-2">
                            {result.snippet}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-500 mt-1 font-inter">
                            {new URL(result.url).hostname}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return null;
}
