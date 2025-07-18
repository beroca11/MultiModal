import { useState } from "react";
import { Link, useLocation } from "wouter";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Plus, MessageCircle, Search, Image, Code, User, Trash2, Pencil, X, Check } from "lucide-react";
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
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editValue, setEditValue] = useState("");

  const createConversationMutation = useMutation({
    mutationFn: async () => {
      console.log("Creating new conversation...");
      const response = await apiRequest("POST", "/api/conversations", {
        title: "New Chat"
      });
      const result = await response.json();
      console.log("New conversation created:", result);
      return result;
    },
    onSuccess: (newConversation) => {
      console.log("Mutation success, navigating to:", newConversation.id);
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      setLocation(`/chat/${newConversation.id}`);
    },
    onError: (error) => {
      console.error("Mutation error:", error);
      toast({
        title: "Error",
        description: "Failed to create new chat",
        variant: "destructive",
      });
    }
  });

  const deleteConversationMutation = useMutation({
    mutationFn: async (conversationId: number) => {
      const response = await apiRequest("DELETE", `/api/conversations/${conversationId}`);
      return response.json();
    },
    onSuccess: (_, conversationId) => {
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      
      // If we deleted the currently active conversation, redirect to home
      if (location === `/chat/${conversationId}`) {
        setLocation("/");
      }
      
      toast({
        title: "Success",
        description: "Conversation deleted successfully",
      });
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to delete conversation",
        variant: "destructive",
      });
    }
  });

  const updateConversationMutation = useMutation({
    mutationFn: async ({ id, title }: { id: number; title: string }) => {
      const response = await apiRequest("PATCH", `/api/conversations/${id}`, { title });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      setEditingId(null);
      setEditValue("");
    },
    onError: () => {
      toast({ title: "Error", description: "Failed to update title", variant: "destructive" });
    }
  });

  const handleDeleteConversation = (e: React.MouseEvent, conversationId: number) => {
    e.stopPropagation(); // Prevent navigation when clicking delete
    const conversation = conversations.find(c => c.id === conversationId);
    const title = conversation?.title || 'this conversation';
    
    if (confirm(`Are you sure you want to delete "${title}"? This action cannot be undone.`)) {
      deleteConversationMutation.mutate(conversationId);
    }
  };

  const handleNewChat = () => {
    console.log("New Chat button clicked");
    createConversationMutation.mutate();
  };

  const handleConversationClick = (conversationId: number) => {
    setLocation(`/chat/${conversationId}`);
  };

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
          onClick={handleNewChat}
          disabled={createConversationMutation.isPending}
          className="w-full bg-teal-600 hover:bg-teal-700 text-white font-medium py-3 px-4 rounded-lg transition-colors flex items-center justify-center space-x-2"
        >
          {createConversationMutation.isPending ? (
            <>
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              <span>Creating...</span>
            </>
          ) : (
            <>
              <Plus className="h-4 w-4" />
              <span>New Chat</span>
            </>
          )}
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
                  {editingId === conversation.id ? (
                    <form
                      onSubmit={e => {
                        e.preventDefault();
                        if (editValue.trim()) {
                          updateConversationMutation.mutate({ id: conversation.id, title: editValue.trim() });
                        }
                      }}
                      className="flex items-center space-x-2"
                    >
                      <input
                        className="text-sm font-medium text-gray-800 dark:text-gray-200 bg-transparent border-b border-gray-300 dark:border-gray-600 focus:outline-none focus:border-teal-500 px-1 py-0.5 w-32"
                        value={editValue}
                        onChange={e => setEditValue(e.target.value)}
                        autoFocus
                        onBlur={() => setEditingId(null)}
                      />
                      <button type="submit" className="text-emerald-600 hover:text-emerald-800"><Check className="h-4 w-4" /></button>
                      <button type="button" onClick={() => setEditingId(null)} className="text-gray-400 hover:text-red-500"><X className="h-4 w-4" /></button>
                    </form>
                  ) : (
                    <div className="flex items-center group/title">
                      <h3 className="text-sm font-medium text-gray-800 dark:text-gray-200 truncate">
                        {conversation.title}
                      </h3>
                      <button
                        className="ml-1 opacity-0 group-hover/title:opacity-100 transition-opacity text-gray-400 hover:text-teal-600"
                        onClick={e => {
                          e.preventDefault();
                          e.stopPropagation();
                          setEditingId(conversation.id);
                          setEditValue(conversation.title);
                        }}
                        title="Edit title"
                      >
                        <Pencil className="h-4 w-4" />
                      </button>
                    </div>
                  )}
                  <div className="flex items-center space-x-2 mt-2">
                    <span className="text-xs text-gray-400">
                      {conversation.updatedAt
                        ? new Date(conversation.updatedAt).toLocaleDateString()
                        : "Just now"}
                    </span>
                  </div>
                </div>
                {/* Delete Button */}
                <Button
                  variant="ghost"
                  size="sm"
                  className="opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8 p-0 hover:bg-red-100 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400"
                  onClick={(e) => handleDeleteConversation(e, conversation.id)}
                  disabled={deleteConversationMutation.isPending}
                >
                  {deleteConversationMutation.isPending ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-red-600 border-t-transparent" />
                  ) : (
                    <Trash2 className="h-4 w-4" />
                  )}
                </Button>
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
