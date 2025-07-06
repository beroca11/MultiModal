"""
Configuration management for the Deep Research System
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Deep Research System"""
    
    # AI Provider API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Search API Keys
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
    
    # Database Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/deepresearch")
    SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "./data/research.db")
    
    # Research Configuration
    MAX_RESEARCH_ITERATIONS = int(os.getenv("MAX_RESEARCH_ITERATIONS", "5"))
    RESEARCH_TIMEOUT = int(os.getenv("RESEARCH_TIMEOUT", "300"))
    MAX_SOURCES_PER_TOPIC = int(os.getenv("MAX_SOURCES_PER_TOPIC", "10"))
    
    # AI Provider Configuration
    PREFERRED_AI_PROVIDER = os.getenv("PREFERRED_AI_PROVIDER", "openai").lower()
    
    # Model Configuration
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4000"))
    
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
    ANTHROPIC_TEMPERATURE = float(os.getenv("ANTHROPIC_TEMPERATURE", "0.7"))
    ANTHROPIC_MAX_TOKENS = int(os.getenv("ANTHROPIC_MAX_TOKENS", "4000"))
    
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-pro")
    GOOGLE_TEMPERATURE = float(os.getenv("GOOGLE_TEMPERATURE", "0.7"))
    GOOGLE_MAX_TOKENS = int(os.getenv("GOOGLE_MAX_TOKENS", "4000"))
    
    # Agent Configuration - Updated to support multiple providers
    AGENT_MODELS = {
        "manager": PREFERRED_AI_PROVIDER,
        "researcher": PREFERRED_AI_PROVIDER,
        "analyst": PREFERRED_AI_PROVIDER,
        "editor": PREFERRED_AI_PROVIDER,
        "reporter": PREFERRED_AI_PROVIDER
    }
    
    # Research Tools Configuration
    SEARCH_TOOLS = [
        "tavily_search",
        "duckduckgo_search",
        "wikipedia_search",
        "arxiv_search",
        "scholarly_search"
    ]
    
    # Output Configuration
    OUTPUT_FORMATS = ["markdown", "pdf", "html", "json"]
    DEFAULT_OUTPUT_FORMAT = "markdown"
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return any issues"""
        issues = {}
        
        # Check if at least one AI provider is configured
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY and not cls.GOOGLE_API_KEY:
            issues["AI_PROVIDERS"] = "At least one AI provider API key is required (OpenAI, Anthropic, or Google)"
        
        # Check preferred provider
        if cls.PREFERRED_AI_PROVIDER not in ["openai", "anthropic", "google"]:
            issues["PREFERRED_AI_PROVIDER"] = "Preferred AI provider must be 'openai', 'anthropic', or 'google'"
        
        # Check if preferred provider has API key
        if cls.PREFERRED_AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            issues["OPENAI_API_KEY"] = "OpenAI API key is required when using OpenAI as preferred provider"
        elif cls.PREFERRED_AI_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            issues["ANTHROPIC_API_KEY"] = "Anthropic API key is required when using Anthropic as preferred provider"
        elif cls.PREFERRED_AI_PROVIDER == "google" and not cls.GOOGLE_API_KEY:
            issues["GOOGLE_API_KEY"] = "Google API key is required when using Google as preferred provider"
        
        if not cls.TAVILY_API_KEY:
            issues["TAVILY_API_KEY"] = "Tavily API key is recommended for better search results"
        
        return issues
    
    @classmethod
    def get_agent_config(cls, agent_type: str) -> Dict[str, Any]:
        """Get configuration for a specific agent type"""
        provider = cls.AGENT_MODELS.get(agent_type, cls.PREFERRED_AI_PROVIDER)
        
        if provider == "openai":
            return {
                "model": cls.OPENAI_MODEL,
                "temperature": cls.OPENAI_TEMPERATURE,
                "max_tokens": cls.OPENAI_MAX_TOKENS,
                "verbose": True
            }
        elif provider == "anthropic":
            return {
                "model": cls.ANTHROPIC_MODEL,
                "temperature": cls.ANTHROPIC_TEMPERATURE,
                "max_tokens": cls.ANTHROPIC_MAX_TOKENS,
                "verbose": True
            }
        elif provider == "google":
            return {
                "model": cls.GOOGLE_MODEL,
                "temperature": cls.GOOGLE_TEMPERATURE,
                "max_tokens": cls.GOOGLE_MAX_TOKENS,
                "verbose": True
            }
        else:
            # Fallback to OpenAI
            return {
                "model": cls.OPENAI_MODEL,
                "temperature": cls.OPENAI_TEMPERATURE,
                "max_tokens": cls.OPENAI_MAX_TOKENS,
                "verbose": True
            }
    
    @classmethod
    def get_available_providers(cls) -> Dict[str, bool]:
        """Get available AI providers and their status"""
        return {
            "openai": bool(cls.OPENAI_API_KEY),
            "anthropic": bool(cls.ANTHROPIC_API_KEY),
            "google": bool(cls.GOOGLE_API_KEY)
        }
    
    @classmethod
    def get_provider_info(cls) -> Dict[str, Any]:
        """Get information about the current AI provider configuration"""
        available = cls.get_available_providers()
        
        return {
            "preferred_provider": cls.PREFERRED_AI_PROVIDER,
            "available_providers": available,
            "current_model": cls.get_agent_config("manager")["model"],
            "current_temperature": cls.get_agent_config("manager")["temperature"],
            "current_max_tokens": cls.get_agent_config("manager")["max_tokens"]
        } 