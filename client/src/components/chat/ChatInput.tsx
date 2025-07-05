import { useState, useRef, useCallback } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import { useLocation } from "wouter";
import { 
  Send, 
  Paperclip, 
  Mic, 
  Search, 
  Code, 
  Image as ImageIcon, 
  Brain,
  Play,
  Wand2
} from "lucide-react";
import ToolPanel from "./ToolPanel";

interface ChatInputProps {
  conversationId: number | null;
  selectedModel: string;
  onMessageSent?: () => void;
}

export default function ChatInput({ conversationId, selectedModel, onMessageSent }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [activeTools, setActiveTools] = useState<string[]>([]);
  const [codeContent, setCodeContent] = useState("");
  const [codeLanguage, setCodeLanguage] = useState("javascript");
  const [imagePrompt, setImagePrompt] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const queryClient = useQueryClient();
  const [, setLocation] = useLocation();
  const { toast } = useToast();

  const sendMessageMutation = useMutation({
    mutationFn: async (data: { content: string; model: string; includeSearch: boolean }) => {
      if (!conversationId) {
        // Create new conversation first
        const newConversation = await apiRequest("POST", "/api/conversations", {
          title: data.content.slice(0, 50) + (data.content.length > 50 ? "..." : "")
        });
        const conversation = await newConversation.json();
        
        // Navigate to the new conversation
        setLocation(`/chat/${conversation.id}`);
        
        // Send message to new conversation
        const response = await apiRequest("POST", `/api/conversations/${conversation.id}/messages`, data);
        return response.json();
      } else {
        const response = await apiRequest("POST", `/api/conversations/${conversationId}/messages`, data);
        return response.json();
      }
    },
    onSuccess: () => {
      setMessage("");
      setActiveTools([]);
      setCodeContent("");
      setImagePrompt("");
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      if (conversationId) {
        queryClient.invalidateQueries({ queryKey: ["/api/conversations", conversationId, "messages"] });
      }
      onMessageSent?.();
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to send message",
        variant: "destructive",
      });
    }
  });

  const generateImageMutation = useMutation({
    mutationFn: async (prompt: string) => {
      const response = await apiRequest("POST", "/api/generate-image", { prompt });
      return response.json();
    },
    onSuccess: (data) => {
      toast({
        title: "Image Generated",
        description: "Your image has been generated successfully",
      });
      // Add image to message
      setMessage(prev => prev + `\n\n![Generated Image](${data.url})`);
    },
    onError: (error) => {
      toast({
        title: "Error",
        description: "Failed to generate image",
        variant: "destructive",
      });
    }
  });

  const handleSubmit = useCallback(() => {
    if (!message.trim() || sendMessageMutation.isPending) return;
    
    const includeSearch = activeTools.includes("search") || 
      /\b(search|latest|recent|current|news|update|trend|2024|2025)\b/i.test(message);
    
    let finalMessage = message;
    
    // Add code if present
    if (codeContent.trim()) {
      finalMessage += `\n\n\`\`\`${codeLanguage}\n${codeContent}\n\`\`\``;
    }
    
    sendMessageMutation.mutate({
      content: finalMessage,
      model: selectedModel,
      includeSearch
    });
  }, [message, selectedModel, activeTools, codeContent, codeLanguage, sendMessageMutation, conversationId]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 200) + 'px';
    }
  };

  const toggleTool = (tool: string) => {
    setActiveTools(prev => 
      prev.includes(tool) 
        ? prev.filter(t => t !== tool)
        : [...prev, tool]
    );
  };

  const handleGenerateImage = () => {
    if (imagePrompt.trim()) {
      generateImageMutation.mutate(imagePrompt);
    }
  };

  const tokenCount = Math.floor(message.length / 4); // Rough estimate

  return (
    <div className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-6 py-4">
      <div className="max-w-4xl mx-auto">
        {/* Tool Panels */}
        {activeTools.length > 0 && (
          <div className="mb-4 space-y-3">
            <ToolPanel
              activeTools={activeTools}
              codeContent={codeContent}
              setCodeContent={setCodeContent}
              codeLanguage={codeLanguage}
              setCodeLanguage={setCodeLanguage}
              imagePrompt={imagePrompt}
              setImagePrompt={setImagePrompt}
              onGenerateImage={handleGenerateImage}
              isGeneratingImage={generateImageMutation.isPending}
            />
          </div>
        )}
        
        {/* Main Input */}
        <div className="flex items-end space-x-4">
          <div className="flex-1">
            <div className="relative">
              <Textarea
                ref={textareaRef}
                value={message}
                onChange={handleTextareaChange}
                onKeyDown={handleKeyDown}
                placeholder="Ask me anything... (Enter to send, Shift+Enter for new line)"
                className="min-h-[44px] max-h-[200px] bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-xl px-4 py-3 pr-12 resize-none"
                style={{ height: '44px' }}
              />
              
              <Button
                variant="ghost"
                size="sm"
                className="absolute right-12 top-1/2 transform -translate-y-1/2 p-2 h-8 w-8"
              >
                <Paperclip className="h-4 w-4" />
              </Button>
              
              <Button
                variant="ghost"
                size="sm"
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 h-8 w-8"
              >
                <Mic className="h-4 w-4" />
              </Button>
            </div>
          </div>
          
          <Button
            onClick={handleSubmit}
            disabled={!message.trim() || sendMessageMutation.isPending}
            className="bg-teal-600 hover:bg-teal-700 text-white p-3 rounded-xl transition-all duration-200 transform hover:scale-105 shadow-lg"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
        
        {/* Quick Actions */}
        <div className="flex items-center justify-between mt-3">
          <div className="flex items-center space-x-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => toggleTool("search")}
              className={`flex items-center space-x-1 text-xs transition-colors ${
                activeTools.includes("search") 
                  ? 'text-teal-600 bg-teal-50 dark:bg-teal-900/20' 
                  : 'text-gray-500 hover:text-teal-600'
              }`}
            >
              <Search className="h-3 w-3" />
              <span>Web Search</span>
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => toggleTool("code")}
              className={`flex items-center space-x-1 text-xs transition-colors ${
                activeTools.includes("code") 
                  ? 'text-teal-600 bg-teal-50 dark:bg-teal-900/20' 
                  : 'text-gray-500 hover:text-teal-600'
              }`}
            >
              <Code className="h-3 w-3" />
              <span>Code</span>
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => toggleTool("image")}
              className={`flex items-center space-x-1 text-xs transition-colors ${
                activeTools.includes("image") 
                  ? 'text-teal-600 bg-teal-50 dark:bg-teal-900/20' 
                  : 'text-gray-500 hover:text-teal-600'
              }`}
            >
              <ImageIcon className="h-3 w-3" />
              <span>Image</span>
            </Button>
            
            <Button
              variant="ghost"
              size="sm"
              onClick={() => toggleTool("research")}
              className={`flex items-center space-x-1 text-xs transition-colors ${
                activeTools.includes("research") 
                  ? 'text-teal-600 bg-teal-50 dark:bg-teal-900/20' 
                  : 'text-gray-500 hover:text-teal-600'
              }`}
            >
              <Brain className="h-3 w-3" />
              <span>Research</span>
            </Button>
          </div>
          
          <div className="flex items-center space-x-2 text-xs text-gray-400">
            <span>Press Enter to send</span>
            <span>•</span>
            <span>{tokenCount}/4096 tokens</span>
          </div>
        </div>
      </div>
    </div>
  );
}
