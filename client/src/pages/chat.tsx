import { useState, useEffect } from "react";
import { useParams } from "wouter";
import { useQuery } from "@tanstack/react-query";
import ChatSidebar from "@/components/chat/ChatSidebar";
import ChatMessages from "@/components/chat/ChatMessages";
import ChatInput from "@/components/chat/ChatInput";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { useTheme } from "@/components/ui/theme-provider";
import { Moon, Sun, Settings, Bolt, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

export default function Chat() {
  const { id } = useParams<{ id?: string }>();
  const [selectedModel, setSelectedModel] = useState("auto");
  const [isToolsOpen, setIsToolsOpen] = useState(false);
  const { theme, setTheme } = useTheme();

  const conversationId = id ? parseInt(id) : null;

  const { data: conversations } = useQuery({
    queryKey: ["/api/conversations"],
    refetchInterval: 5000,
  });

  const { data: messages, refetch: refetchMessages } = useQuery({
    queryKey: ["/api/conversations", conversationId, "messages"],
    enabled: !!conversationId,
  });

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
              <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100">
                {conversationId ? "Current Chat" : "AI Assistant"}
              </h2>
              
              {/* Status Indicators */}
              <div className="flex items-center space-x-2">
                <Badge variant="outline" className="bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 border-green-200 dark:border-green-800">
                  <div className="w-2 h-2 rounded-full bg-green-500 mr-1"></div>
                  GPT-4o Active
                </Badge>
                <Badge variant="outline" className="bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800">
                  <div className="w-2 h-2 rounded-full bg-blue-500 mr-1"></div>
                  Claude Ready
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
                  <SelectItem value="claude">Claude</SelectItem>
                  <SelectItem value="gemini">Gemini</SelectItem>
                  <SelectItem value="combined">Combined Response</SelectItem>
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
          messages={messages || []} 
          conversationId={conversationId}
          isLoading={!conversationId}
        />

        {/* Input */}
        <ChatInput 
          conversationId={conversationId}
          selectedModel={selectedModel}
          onMessageSent={refetchMessages}
        />
      </div>
    </div>
  );
}
