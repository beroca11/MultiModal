import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertMessageSchema, insertConversationSchema } from "@shared/schema";
import { generateWithGPT4o, generateWithClaude, generateWithGemini, generateMultiModel, generateImage, analyzeImage } from "./services/ai";
import { searchAndSummarize } from "./services/search";

export async function registerRoutes(app: Express): Promise<Server> {
  // Get all conversations for user
  app.get("/api/conversations", async (req, res) => {
    try {
      // For demo purposes, using userId = 1. In production, get from auth session
      const userId = 1;
      const conversations = await storage.getConversationsByUserId(userId);
      res.json(conversations);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Create new conversation
  app.post("/api/conversations", async (req, res) => {
    try {
      const { title } = req.body;
      const userId = 1; // Demo user
      
      const conversation = await storage.createConversation({
        title: title || "New Chat",
        userId
      });
      
      res.json(conversation);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Get messages for a conversation
  app.get("/api/conversations/:id/messages", async (req, res) => {
    try {
      const conversationId = parseInt(req.params.id);
      const messages = await storage.getMessagesByConversationId(conversationId);
      res.json(messages);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Send message and get AI response
  app.post("/api/conversations/:id/messages", async (req, res) => {
    try {
      const conversationId = parseInt(req.params.id);
      const { content, model = "auto", includeSearch = false, includeImage = false } = req.body;

      // Validate input
      if (!content || typeof content !== 'string') {
        return res.status(400).json({ error: "Message content is required" });
      }

      // Save user message
      const userMessage = await storage.createMessage({
        conversationId,
        role: "user",
        content,
        model: null,
        metadata: null
      });

      // Determine if we need web search
      const needsSearch = includeSearch || 
        /\b(search|latest|recent|current|news|update|trend|2024|2025)\b/i.test(content);

      let searchResults = null;
      let enhancedPrompt = content;

      if (needsSearch) {
        try {
          const searchResponse = await searchAndSummarize(content, model === "auto" ? "gpt-4o" : model);
          searchResults = searchResponse.searchResults;
          enhancedPrompt = `${content}\n\nRecent web search results:\n${searchResponse.summary}`;
        } catch (error) {
          console.warn("Web search failed:", error.message);
        }
      }

      // Generate AI response
      let aiResponse;
      let responseModel = model;

      try {
        if (model === "auto" || model === "combined") {
          const multiResponse = await generateMultiModel(enhancedPrompt, ["gpt-4o", "claude", "gemini"]);
          aiResponse = multiResponse.combined || multiResponse.responses[0]?.content || "No response generated";
          responseModel = "combined";
        } else if (model === "gpt-4o") {
          const response = await generateWithGPT4o(enhancedPrompt);
          aiResponse = response.content;
        } else if (model === "claude") {
          const response = await generateWithClaude(enhancedPrompt);
          aiResponse = response.content;
        } else if (model === "gemini") {
          const response = await generateWithGemini(enhancedPrompt);
          aiResponse = response.content;
        } else {
          const response = await generateWithGPT4o(enhancedPrompt);
          aiResponse = response.content;
          responseModel = "gpt-4o";
        }
      } catch (error) {
        aiResponse = `I encountered an error while processing your request: ${error.message}`;
        responseModel = "error";
      }

      // Save assistant message
      const assistantMessage = await storage.createMessage({
        conversationId,
        role: "assistant",
        content: aiResponse,
        model: responseModel,
        metadata: searchResults ? { searchResults } : null
      });

      // Update conversation timestamp
      await storage.updateConversation(conversationId, {
        updatedAt: new Date()
      });

      res.json({
        userMessage,
        assistantMessage,
        searchResults
      });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Generate image
  app.post("/api/generate-image", async (req, res) => {
    try {
      const { prompt } = req.body;
      
      if (!prompt) {
        return res.status(400).json({ error: "Prompt is required" });
      }

      const result = await generateImage(prompt);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Analyze image
  app.post("/api/analyze-image", async (req, res) => {
    try {
      const { image, model = "gpt-4o" } = req.body;
      
      if (!image) {
        return res.status(400).json({ error: "Image data is required" });
      }

      const result = await analyzeImage(image, model);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Web search endpoint
  app.post("/api/search", async (req, res) => {
    try {
      const { query, model = "gpt-4o" } = req.body;
      
      if (!query) {
        return res.status(400).json({ error: "Search query is required" });
      }

      const result = await searchAndSummarize(query, model);
      res.json(result);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
