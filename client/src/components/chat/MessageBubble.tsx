import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { User, Bot, Copy, ThumbsUp, ThumbsDown } from "lucide-react";
import { cn } from "@/lib/utils";
import ReactMarkdown from "react-markdown";
import type { Message } from "@shared/schema";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";

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

  const hasSearchResults = message.metadata && 
    typeof message.metadata === 'object' && 
    'searchResults' in message.metadata && 
    message.metadata.searchResults;

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-3xl bg-teal-600 text-white rounded-2xl px-6 py-4 shadow-sm">
          <p className="text-sm leading-relaxed">{message.content}</p>
        </div>
      </div>
    );
  }

  if (isAssistant) {
    return (
      <div className="flex justify-start">
        <div className="max-w-3xl w-full">
          <div className="flex items-center space-x-2 mb-3">
            <Avatar className="w-8 h-8 bg-gradient-to-r from-emerald-500 to-blue-500">
              <AvatarFallback className="bg-gradient-to-r from-emerald-500 to-blue-500 text-white">
                <Bot className="h-4 w-4" />
              </AvatarFallback>
            </Avatar>
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              AI Assistant
            </span>
            {message.model && (
              <Badge variant="outline" className="text-xs">
                <div className={cn("w-2 h-2 rounded-full mr-1", getModelColor(message.model))}></div>
                {getModelName(message.model)}
              </Badge>
            )}
          </div>
          
          <Card className="bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700">
            <CardContent className="p-6">
              {/* Search Results */}
              {hasSearchResults && (
                <div className="bg-emerald-50 dark:bg-emerald-900/20 rounded-lg p-4 mb-4">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
                    <span className="text-sm font-medium text-emerald-700 dark:text-emerald-300">
                      Web Search Results
                    </span>
                  </div>
                  <div className="space-y-2">
                    {(message.metadata as any)?.searchResults?.results?.slice(0, 3).map((result: any, index: number) => (
                      <div key={index} className="bg-white dark:bg-gray-700 rounded p-3">
                        <h4 className="text-sm font-medium text-gray-800 dark:text-gray-200">
                          {result.title}
                        </h4>
                        <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                          {result.snippet}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {/* Main Content */}
              <div className="prose prose-sm max-w-none text-gray-700 dark:text-gray-300 dark:prose-invert">
                <ReactMarkdown
                  components={{
                    h1: ({ children }) => <h1 className="text-lg font-semibold mb-3 text-gray-800 dark:text-gray-200">{children}</h1>,
                    h2: ({ children }) => <h2 className="text-lg font-semibold mb-3 text-gray-800 dark:text-gray-200">{children}</h2>,
                    h3: ({ children }) => <h3 className="text-base font-semibold mb-2 text-gray-800 dark:text-gray-200">{children}</h3>,
                    p: ({ children }) => <p className="mb-4 leading-relaxed">{children}</p>,
                    ul: ({ children }) => <ul className="mb-4 space-y-1 list-disc pl-6">{children}</ul>,
                    ol: ({ children }) => <ol className="mb-4 space-y-1 list-decimal pl-6">{children}</ol>,
                    li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                    code: ({ children, className }) => {
                      const isBlock = className?.includes('language-');
                      return isBlock ? (
                        <pre className="bg-gray-100 dark:bg-gray-900 rounded p-3 overflow-x-auto">
                          <code className={className}>{children}</code>
                        </pre>
                      ) : (
                        <code className="bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded text-sm">{children}</code>
                      );
                    },
                    blockquote: ({ children }) => (
                      <blockquote className="border-l-4 border-gray-300 dark:border-gray-600 pl-4 italic">{children}</blockquote>
                    ),
                  }}
                >
                  {String(message.content)}
                </ReactMarkdown>
              </div>
            </CardContent>
          </Card>
          
          {/* Actions */}
          <div className="flex items-center space-x-2 mt-2">
            <Button variant="ghost" size="sm" className="h-8 px-2">
              <Copy className="h-3 w-3" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 px-2">
              <ThumbsUp className="h-3 w-3" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 px-2">
              <ThumbsDown className="h-3 w-3" />
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return null;
}
