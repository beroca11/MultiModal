import { useState } from "react";
import { Link, useLocation } from "wouter";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Plus, MessageCircle, Search, Image, Code, User } from "lucide-react";
import { apiRequest } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import type { Conversation } from "@shared/schema";

interface ChatSidebarProps {
  conversations: Conversation[];
}

export default function ChatSidebar({ conversations }: ChatSidebarProps) {
  const [location, setLocation] = useLocation();
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const createConversationMutation = useMutation({
    mutationFn: async () => {
      const response = await apiRequest("POST", "/api/conversations", {
        title: "New Chat"
      });
      return response.json();
    },
    onSuccess: (newConversation) => {
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      setLocation(`/chat/${newConversation.id}`);
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to create new chat",
        variant: "destructive",
      });
    }
  });

  const formatTimestamp = (timestamp: string | Date) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const days = Math.floor(hours / 24);
    
    if (days > 0) {
      return `${days} day${days > 1 ? 's' : ''} ago`;
    } else if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else {
      return 'Just now';
    }
  };

  const getConversationIcon = (title: string) => {
    if (title.toLowerCase().includes('search') || title.toLowerCase().includes('research')) {
      return <Search className="h-3 w-3 text-white" />;
    }
    if (title.toLowerCase().includes('image') || title.toLowerCase().includes('generate')) {
      return <Image className="h-3 w-3 text-white" />;
    }
    if (title.toLowerCase().includes('code') || title.toLowerCase().includes('programming')) {
      return <Code className="h-3 w-3 text-white" />;
    }
    return <MessageCircle className="h-3 w-3 text-white" />;
  };

  const getConversationColor = (title: string) => {
    if (title.toLowerCase().includes('search') || title.toLowerCase().includes('research')) {
      return 'bg-emerald-500';
    }
    if (title.toLowerCase().includes('image') || title.toLowerCase().includes('generate')) {
      return 'bg-purple-500';
    }
    if (title.toLowerCase().includes('code') || title.toLowerCase().includes('programming')) {
      return 'bg-orange-500';
    }
    return 'bg-teal-600';
  };

  return (
    <div className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
        <h1 className="text-lg font-semibold text-gray-800 dark:text-gray-100">AI Assistant</h1>
      </div>
      
      {/* New Chat Button */}
      <div className="p-4">
        <Button 
          onClick={() => createConversationMutation.mutate()}
          disabled={createConversationMutation.isPending}
          className="w-full bg-teal-600 hover:bg-teal-700 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
        >
          <Plus className="h-4 w-4" />
          <span>New Chat</span>
        </Button>
      </div>
      
      {/* Chat History */}
      <ScrollArea className="flex-1 px-4 pb-4">
        <div className="space-y-2">
          {conversations.map((conversation) => (
            <Link
              key={conversation.id}
              href={`/chat/${conversation.id}`}
              className={`block p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition-colors group ${
                location === `/chat/${conversation.id}` 
                  ? 'bg-gray-100 dark:bg-gray-700' 
                  : ''
              }`}
            >
              <div className="flex items-start space-x-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${getConversationColor(conversation.title)}`}>
                  {getConversationIcon(conversation.title)}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-gray-800 dark:text-gray-200 truncate">
                    {conversation.title}
                  </h3>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className="text-xs text-gray-400">
                      {formatTimestamp(conversation.updatedAt || conversation.createdAt)}
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </ScrollArea>
      
      {/* User Profile */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <div className="flex items-center space-x-3">
          <Avatar className="w-8 h-8 bg-gradient-to-r from-teal-600 to-emerald-600">
            <AvatarFallback className="bg-gradient-to-r from-teal-600 to-emerald-600 text-white">
              <User className="h-4 w-4" />
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-800 dark:text-gray-200">Demo User</p>
            <p className="text-xs text-gray-500 dark:text-gray-400">Pro Plan</p>
          </div>
        </div>
      </div>
    </div>
  );
}
