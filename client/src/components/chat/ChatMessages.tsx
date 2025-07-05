import { useEffect, useRef } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import MessageBubble from "./MessageBubble";
import { Bot, Sparkles } from "lucide-react";
import type { Message } from "@shared/schema";

interface ChatMessagesProps {
  messages: Message[];
  conversationId: number | null;
  isLoading?: boolean;
}

export default function ChatMessages({ messages, conversationId, isLoading }: ChatMessagesProps) {
  const scrollAreaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  if (isLoading) {
    return (
      <div className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="space-y-6">
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-16 w-3/4" />
            <Skeleton className="h-24 w-full" />
          </div>
        </div>
      </div>
    );
  }

  if (!conversationId) {
    return (
      <div className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-gradient-to-r from-teal-600 to-emerald-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <Bot className="h-8 w-8 text-white" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-2">
              Welcome to AI Assistant
            </h3>
            <p className="text-gray-600 dark:text-gray-400 max-w-md mx-auto">
              Your multi-model AI assistant with web search, image generation, and code execution capabilities.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ScrollArea ref={scrollAreaRef} className="flex-1 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="space-y-6">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
        </div>
      </div>
    </ScrollArea>
  );
}
