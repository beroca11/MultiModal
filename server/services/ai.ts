import OpenAI from "openai";
import Anthropic from '@anthropic-ai/sdk';
import { GoogleGenAI } from "@google/genai";

// the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
const openai = new OpenAI({ 
  apiKey: process.env.OPENAI_API_KEY || process.env.VITE_OPENAI_API_KEY || ""
});

/*
The newest Anthropic model is "claude-sonnet-4-20250514", not "claude-3-7-sonnet-20250219", "claude-3-5-sonnet-20241022" nor "claude-3-sonnet-20240229". 
If the user doesn't specify a model, always prefer using "claude-sonnet-4-20250514" as it is the latest model.
*/
const DEFAULT_MODEL_STR = "claude-sonnet-4-20250514";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_API_KEY || "",
});

// Note that the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
const ai = new GoogleGenAI({ 
  apiKey: process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || "" 
});

export interface AIResponse {
  content: string;
  model: string;
  metadata?: any;
}

export interface MultiModelResponse {
  responses: AIResponse[];
  combined?: string;
}

export async function generateWithGPT4o(prompt: string, context?: any): Promise<AIResponse> {
  try {
    const cleanPrompt = `${prompt}\n\nPlease provide a well-structured, professional response without using any markdown symbols (#, *, -, etc.). Write in clear, readable paragraphs with proper formatting.`;
    
    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "user", content: cleanPrompt }
      ],
      max_tokens: 2000,
    });

    return {
      content: response.choices[0].message.content || "",
      model: "gpt-4o",
      metadata: context
    };
  } catch (error) {
    throw new Error(`OpenAI API error: ${(error as Error).message}`);
  }
}

export async function generateWithClaude(prompt: string, context?: any): Promise<AIResponse> {
  try {
    const cleanPrompt = `${prompt}\n\nPlease provide a well-structured, professional response without using any markdown symbols (#, *, -, etc.). Write in clear, readable paragraphs with proper formatting.`;
    
    const message = await anthropic.messages.create({
      max_tokens: 2000,
      messages: [{ role: 'user', content: cleanPrompt }],
      model: DEFAULT_MODEL_STR,
    });

    return {
      content: message.content[0].type === 'text' ? message.content[0].text : '',
      model: DEFAULT_MODEL_STR,
      metadata: context
    };
  } catch (error) {
    throw new Error(`Anthropic API error: ${(error as Error).message}`);
  }
}

export async function generateWithGemini(prompt: string, context?: any): Promise<AIResponse> {
  try {
    const cleanPrompt = `${prompt}\n\nPlease provide a well-structured, professional response without using any markdown symbols (#, *, -, etc.). Write in clear, readable paragraphs with proper formatting.`;
    
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: cleanPrompt,
    });

    return {
      content: response.text || "",
      model: "gemini-2.5-flash",
      metadata: context
    };
  } catch (error) {
    throw new Error(`Gemini API error: ${(error as Error).message}`);
  }
}

export async function generateMultiModel(prompt: string, models: string[] = ["gpt-4o", "claude", "gemini"]): Promise<MultiModelResponse> {
  const responses: AIResponse[] = [];
  
  const tasks = models.map(async (model) => {
    try {
      switch (model) {
        case "gpt-4o":
          return await generateWithGPT4o(prompt);
        case "claude":
          return await generateWithClaude(prompt);
        case "gemini":
          return await generateWithGemini(prompt);
        default:
          throw new Error(`Unknown model: ${model}`);
      }
    } catch (error) {
      return {
        content: `Error with ${model}: ${(error as Error).message}`,
        model,
        metadata: { error: true }
      };
    }
  });

  const results = await Promise.all(tasks);
  responses.push(...results);

  // Generate a combined response using GPT-4o
  if (models.length > 1) {
    try {
      const combinedPrompt = `Based on these responses from different AI models, provide a synthesized answer:

${responses.map((r, i) => `${r.model}: ${r.content}`).join('\n\n')}

Please provide a comprehensive, well-structured response that combines the best insights from all models. Write in clear, professional paragraphs without using any markdown symbols (#, *, -, etc.). Focus on delivering actionable insights and valuable information.`;

      const combined = await generateWithGPT4o(combinedPrompt);
      return {
        responses,
        combined: combined.content
      };
    } catch (error) {
      return { responses };
    }
  }

  return { responses };
}

export async function generateImage(prompt: string): Promise<{ url: string; model: string }> {
  try {
    const response = await openai.images.generate({
      model: "dall-e-3",
      prompt: prompt,
      n: 1,
      size: "1024x1024",
      quality: "standard",
    });

    return {
      url: response.data?.[0]?.url || "",
      model: "dall-e-3"
    };
  } catch (error) {
    throw new Error(`Image generation error: ${(error as Error).message}`);
  }
}

export async function analyzeImage(base64Image: string, model: string = "gpt-4o"): Promise<AIResponse> {
  try {
    if (model === "gpt-4o") {
      const response = await openai.chat.completions.create({
        model: "gpt-4o",
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: "Analyze this image in detail and describe its key elements, context, and any notable aspects."
              },
              {
                type: "image_url",
                image_url: {
                  url: `data:image/jpeg;base64,${base64Image}`
                }
              }
            ],
          },
        ],
        max_tokens: 500,
      });

      return {
        content: response.choices[0].message.content || "",
        model: "gpt-4o"
      };
    } else if (model === "claude") {
      const response = await anthropic.messages.create({
        model: DEFAULT_MODEL_STR,
        max_tokens: 500,
        messages: [{
          role: "user",
          content: [
            {
              type: "text",
              text: "Analyze this image in detail and describe its key elements, context, and any notable aspects."
            },
            {
              type: "image",
              source: {
                type: "base64",
                media_type: "image/jpeg",
                data: base64Image
              }
            }
          ]
        }]
      });

      return {
        content: response.content[0].type === 'text' ? response.content[0].text : '',
        model: DEFAULT_MODEL_STR
      };
    }

    throw new Error(`Image analysis not supported for model: ${model}`);
  } catch (error) {
    throw new Error(`Image analysis error: ${(error as Error).message}`);
  }
}
