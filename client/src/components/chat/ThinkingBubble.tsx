import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Bot, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface ThinkingBubbleProps {
  model?: string;
}

export default function ThinkingBubble({ model }: ThinkingBubbleProps) {
  const getModelColor = (model: string | undefined) => {
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

  const getModelName = (model: string | undefined) => {
    if (!model) return "AI Assistant";
    
    switch (model) {
      case "gpt-4o":
        return "GPT-4o";
      case "claude-sonnet-4-20250514":
      case "claude":
        return "Claude";
      case "gemini-2.5-flash":
      case "gemini":
        return "Gemini";
      case "combined":
        return "Combined AI";
      default:
        return model;
    }
  };

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
            {getModelName(model)}
          </span>
          {model && (
            <Badge variant="outline" className="text-xs">
              <div className={cn("w-2 h-2 rounded-full mr-1", getModelColor(model))}></div>
              {getModelName(model)}
            </Badge>
          )}
        </div>
        
        <Card className="bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <Loader2 className="h-5 w-5 animate-spin text-teal-600" />
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-teal-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-teal-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-teal-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {getModelName(model)} is thinking...
              </span>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 