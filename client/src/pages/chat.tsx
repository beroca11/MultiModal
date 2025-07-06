import { useState, useEffect } from "react";
import { useParams } from "wouter";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import ChatSidebar from "@/components/chat/ChatSidebar";
import ChatMessages from "@/components/chat/ChatMessages";
import ChatInput from "@/components/chat/ChatInput";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { useTheme } from "@/components/ui/theme-provider";
import { Moon, Sun, Settings, Bolt, ChevronDown, Pencil, X, Check, Trash2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { useMutation } from "@tanstack/react-query";
import type { Conversation } from "@shared/schema";

export default function Chat() {
  const { id } = useParams<{ id?: string }>();
  const [selectedModel, setSelectedModel] = useState("auto");
  const [isToolsOpen, setIsToolsOpen] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [thinkingModel, setThinkingModel] = useState<string>();
  const [tempMessages, setTempMessages] = useState<any[]>([]);
  const { theme, setTheme } = useTheme();
  const [editingTitle, setEditingTitle] = useState(false);
  const [editValue, setEditValue] = useState("");

  const conversationId = id ? parseInt(id) : null;

  const { data: conversations } = useQuery({
    queryKey: ["/api/conversations"],
    refetchInterval: 5000,
  });

  const { data: messages, refetch: refetchMessages } = useQuery({
    queryKey: ["/api/conversations", conversationId, "messages"],
    enabled: !!conversationId,
  });

  const queryClient = useQueryClient();
  const updateConversationMutation = useMutation({
    mutationFn: async ({ id, title }: { id: number; title: string }) => {
      const response = await fetch(`/api/conversations/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title })
      });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      setEditingTitle(false);
      setEditValue("");
    }
  });
  const deleteConversationMutation = useMutation({
    mutationFn: async (conversationId: number) => {
      const response = await fetch(`/api/conversations/${conversationId}`, { method: "DELETE" });
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      window.location.href = "/";
    }
  });

  // Find the current conversation safely
  const conversationList: Conversation[] = Array.isArray(conversations) ? conversations as Conversation[] : [];
  const currentConversation = conversationList.find((c) => c.id === conversationId);

  // After messages are updated, auto-update the conversation title if needed
  useEffect(() => {
    if (!conversationId || !Array.isArray(messages) || !messages.length) return;
    // Find the latest assistant message with a summary
    const lastAssistant = [...messages].reverse().find(
      (msg: any) => msg.role === "assistant" && msg.metadata && msg.metadata.searchSummary && msg.metadata.searchSummary.summary
    );
    if (!lastAssistant) return;
    // Prefer the search query as the title
    let summaryTitle = "";
    const searchSummary = lastAssistant.metadata.searchSummary;
    if (searchSummary.searchResults && searchSummary.searchResults.query) {
      summaryTitle = searchSummary.searchResults.query.trim();
    }
    // Fallback: first non-empty line of the summary
    if (!summaryTitle) {
      const summary = searchSummary.summary as string;
      const headingMatch = summary.match(/^(.*?)(\n|$)/);
      if (headingMatch) {
        summaryTitle = headingMatch[1].replace(/[*#:\-]+/g, '').trim();
      }
    }
    if (!summaryTitle) return;
    // If the current conversation title is 'New Chat', update it
    if (currentConversation && currentConversation.title === "New Chat") {
      fetch(`/api/conversations/${conversationId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: summaryTitle })
      }).then(() => {
        queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      });
    }
  }, [messages, conversationId, currentConversation, queryClient]);

  const handleThinkingChange = (thinking: boolean, model?: string) => {
    setIsThinking(thinking);
    setThinkingModel(model);
    
    // Clear temp messages when thinking stops (response received)
    if (!thinking) {
      setTempMessages([]);
    }
  };

  const handleUserMessageSent = (userMessage: any) => {
    setTempMessages([userMessage]);
  };

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <div className="flex h-screen overflow-hidden bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <ChatSidebar conversations={conversations || []} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Top Bar */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {conversationId && currentConversation ? (
                <div className="flex items-center group">
                  {editingTitle ? (
                    <form
                      onSubmit={e => {
                        e.preventDefault();
                        if (editValue.trim()) {
                          updateConversationMutation.mutate({ id: conversationId, title: editValue.trim() });
                        }
                      }}
                      className="flex items-center space-x-2"
                    >
                      <input
                        className="text-xl font-semibold text-gray-800 dark:text-gray-100 bg-transparent border-b border-gray-300 dark:border-gray-600 focus:outline-none focus:border-teal-500 px-1 py-0.5 w-48"
                        value={editValue}
                        onChange={e => setEditValue(e.target.value)}
                        autoFocus
                        onBlur={() => setEditingTitle(false)}
                      />
                      <button type="submit" className="text-emerald-600 hover:text-emerald-800"><Check className="h-5 w-5" /></button>
                      <button type="button" onClick={() => setEditingTitle(false)} className="text-gray-400 hover:text-red-500"><X className="h-5 w-5" /></button>
                    </form>
                  ) : (
                    <>
                      <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100">
                        {currentConversation.title}
                      </h2>
                      <button
                        className="ml-2 text-gray-400 hover:text-teal-600"
                        onClick={() => {
                          setEditingTitle(true);
                          setEditValue(currentConversation.title);
                        }}
                        title="Edit title"
                      >
                        <Pencil className="h-5 w-5" />
                      </button>
                      <button
                        className="ml-1 text-gray-400 hover:text-red-600"
                        onClick={() => {
                          if (window.confirm("Are you sure you want to delete this conversation?")) {
                            deleteConversationMutation.mutate(conversationId);
                          }
                        }}
                        title="Delete conversation"
                      >
                        <Trash2 className="h-5 w-5" />
                      </button>
                    </>
                  )}
                </div>
              ) : (
                <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100">
                  AI Assistant
                </h2>
              )}
              
              {/* Status Indicators */}
              <div className="flex items-center space-x-2">
                <Badge variant="outline" className="bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 border-green-200 dark:border-green-800">
                  <div className="w-2 h-2 rounded-full bg-green-500 mr-1"></div>
                  GPT-4o Active
                </Badge>
                <Badge variant="outline" className="bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800">
                  <div className="w-2 h-2 rounded-full bg-blue-500 mr-1"></div>
                  Claude Sonnet 4 Ready
                </Badge>
                <Badge variant="outline" className="bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-800">
                  <div className="w-2 h-2 rounded-full bg-purple-500 mr-1"></div>
                  Gemini 2.5 Flash Ready
                </Badge>
              </div>
            </div>
            
            {/* Controls */}
            <div className="flex items-center space-x-3">
              <Select value={selectedModel} onValueChange={setSelectedModel}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="Select model" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="auto">Auto Select</SelectItem>
                  <SelectItem value="gpt-4o">GPT-4o</SelectItem>
                  <SelectItem value="claude">Claude Sonnet 4</SelectItem>
                  <SelectItem value="gemini">Gemini 2.5 Flash</SelectItem>
                  <SelectItem value="combined">Combined AI</SelectItem>
                </SelectContent>
              </Select>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsToolsOpen(!isToolsOpen)}
                className="flex items-center space-x-2"
              >
                <Bolt className="h-4 w-4" />
                <span>Bolt</span>
                <ChevronDown className="h-3 w-3" />
              </Button>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={toggleTheme}
                className="p-2"
              >
                {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
              </Button>
              
              <Button variant="ghost" size="sm" className="p-2">
                <Settings className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>

        {/* Messages */}
        <ChatMessages 
          messages={[...(messages as any[] || []), ...tempMessages]} 
          conversationId={conversationId}
          isLoading={!conversationId}
          isThinking={isThinking}
          thinkingModel={thinkingModel}
        />

        {/* Input */}
        <ChatInput 
          conversationId={conversationId}
          selectedModel={selectedModel}
          onMessageSent={refetchMessages}
          onThinkingChange={handleThinkingChange}
          onUserMessageSent={handleUserMessageSent}
        />
      </div>
    </div>
  );
}
