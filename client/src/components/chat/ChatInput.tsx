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
  onThinkingChange?: (isThinking: boolean, model?: string) => void;
  onUserMessageSent?: (message: { content: string; role: string; id: string; timestamp: Date }) => void;
}

export default function ChatInput({ conversationId, selectedModel, onMessageSent, onThinkingChange, onUserMessageSent }: ChatInputProps) {
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
        return { ...response.json(), newConversationId: conversation.id };
      } else {
        const response = await apiRequest("POST", `/api/conversations/${conversationId}/messages`, data);
        return response.json();
      }
    },
    onMutate: (data) => {
      // Clear input field immediately
      setMessage("");
      setActiveTools([]);
      setCodeContent("");
      setImagePrompt("");
      
      // Show user message immediately
      const userMessage = {
        content: data.content,
        role: "user",
        id: `temp-${Date.now()}`,
        timestamp: new Date()
      };
      onUserMessageSent?.(userMessage);
      
      // Show thinking UI when mutation starts
      onThinkingChange?.(true, selectedModel);
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["/api/conversations"] });
      
      // If this was a new conversation, invalidate messages for the new conversation ID
      if (data.newConversationId) {
        setTimeout(() => {
          queryClient.invalidateQueries({ queryKey: ["/api/conversations", data.newConversationId, "messages"] });
        }, 100);
      } else if (conversationId) {
        queryClient.invalidateQueries({ queryKey: ["/api/conversations", conversationId, "messages"] });
      }
      
      // Hide thinking UI when mutation completes
      onThinkingChange?.(false);
      onMessageSent?.();
    },
    onError: (error) => {
      // Hide thinking UI on error
      onThinkingChange?.(false);
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
        <div className="relative">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={handleTextareaChange}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
            className="w-full min-h-[60px] max-h-[200px] resize-none rounded-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 px-6 py-4 pr-16 focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            disabled={sendMessageMutation.isPending}
          />
          <Button
            onClick={handleSubmit}
            disabled={!message.trim() || sendMessageMutation.isPending}
            className="absolute right-4 bottom-4 h-12 w-12 p-0 bg-teal-600 hover:bg-teal-700 text-white rounded-full transition-colors flex items-center justify-center shadow-md"
          >
            {sendMessageMutation.isPending ? (
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </Button>
        </div>

        <div className="flex items-center justify-between mt-3">
          <div className="flex items-center space-x-3">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => toggleTool("search")}
              className={`flex items-center space-x-1 text-xs transition-colors ${
                activeTools.includes("search") 
                  ? 'text-emerald-600 bg-emerald-50 dark:bg-emerald-900/20' 
                  : 'text-gray-500 hover:text-emerald-600'
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
