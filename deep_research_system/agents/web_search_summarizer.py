import openai
import anthropic
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os
import logging
from dotenv import load_dotenv
import spacy
from collections import Counter
from difflib import SequenceMatcher

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")

# Validate that required API keys are present
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable not set")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# Configure Google Gemini
genai.configure(api_key=google_api_key)

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def extract_entities(snippets):
    """Extract named entities from a list of snippets."""
    entities = []
    for text in snippets:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in {"ORG", "PRODUCT", "PERSON", "GPE", "DATE", "EVENT", "WORK_OF_ART"}:
                entities.append((ent.text, ent.label_))
    # Return most common entities by type
    entity_counter = Counter(entities)
    top_entities = entity_counter.most_common(10)
    return top_entities

def deduplicate_results(results, threshold=0.85):
    """Remove or merge search results with highly similar titles/snippets."""
    deduped = []
    seen = set()
    for r in results:
        key = r['title'].strip().lower()
        if any(SequenceMatcher(None, key, s).ratio() > threshold for s in seen):
            continue
        seen.add(key)
        deduped.append(r)
    return deduped

app = FastAPI()

class SearchResult(BaseModel):
    title: str
    snippet: str
    url: str

class SummarizeRequest(BaseModel):
    query: str
    results: List[SearchResult]
    model: str = "gpt-4o"  # Default model

class SummarizeResponse(BaseModel):
    summary: str
    model_used: str

CLAUDE_MODELS = [
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-3-opus-20240229",
    "claude-2.1",
    "claude-instant-1.2"
]

GEMINI_MODELS = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-pro",
    "gemini-1.0-pro"
]

def create_search_agent_prompt(query: str, results: List[SearchResult]) -> str:
    """Create a dynamic prompt based on query type for more autonomous and helpful responses."""
    # --- Hybrid Preprocessing ---
    # Deduplicate results
    deduped_results = deduplicate_results([r.dict() if hasattr(r, 'dict') else r for r in results])
    # Extract entities from snippets
    snippets = [r['snippet'] for r in deduped_results]
    top_entities = extract_entities(snippets)
    entity_section = "\n".join([f"- {text} ({label})" for (text, label), _ in top_entities])
    entity_section = f"\n\nKey Entities Extracted from Search Results:\n{entity_section}\n" if entity_section else ""
    # ---
    context = "\n\n".join(
        f"[{i+1}] {r['title']}\n{r['snippet']}\nSource: {r['url']}" 
        for i, r in enumerate(deduped_results)
    )
    
    # Helper to extract domain from URL
    def get_domain(url):
        from urllib.parse import urlparse
        return urlparse(url).netloc.replace('www.', '')

    # Build a mapping of index to domain for citation
    domain_map = {str(i+1): get_domain(r['url']) for i, r in enumerate(deduped_results)}

    query_lower = query.lower()
    is_list_query = any(word in query_lower for word in ['top', 'list', 'best', 'worst', 'ranking', 'ranked', '10', '5', '3', '20'])
    is_how_to_query = any(word in query_lower for word in ['how to', 'how do', 'steps', 'guide', 'tutorial', 'process'])
    is_definition_query = any(word in query_lower for word in ['what is', 'define', 'definition', 'meaning', 'explain'])
    is_comparison_query = any(word in query_lower for word in ['vs', 'versus', 'compare', 'difference', 'better', 'which'])
    is_news_query = any(word in query_lower for word in ['latest', 'recent', 'news', 'update', '2024', '2025', 'announcement'])
    is_technical_query = any(word in query_lower for word in ['api', 'code', 'programming', 'technical', 'implementation', 'architecture'])

    # Citation instructions
    citation_instructions = (
        "For all citations, instead of using [1], [2], etc., use the source's domain name in parentheses, e.g., (techradar.com), right after the relevant information. Do not use numbers for citations."
    )
    # Multi-question instructions
    multi_question_instructions = (
        "If the prompt contains multiple questions or requirements, break them down and answer each as a separate item or section."
    )

    # Add these instructions to all prompt types
    if is_list_query:
        return f"""You are a helpful research assistant. Based on the following web search results for "{query}", provide a comprehensive and well-structured response.\n{entity_section}\nSEARCH RESULTS:\n{context}\n\nINSTRUCTIONS:\n1. Analyze the query and provide exactly what was asked for (e.g., if asked for "top 10", provide exactly 10 items)\n2. Use clear, engaging formatting with emojis and bullet points\n3. DO NOT use markdown symbols (#, *, -, etc.)\n4. {citation_instructions}\n5. {multi_question_instructions}\n6. Focus on providing the specific information requested\n7. If the query asks for a specific number, provide exactly that number\n8. Make the response directly answer the question asked\n\nFORMAT EXAMPLE for list queries:\n"📋 Top 10 AI Tools for 2024\n\nBased on recent research and market analysis, here are the top 10 AI tools that are making waves in 2024:\n\n🥇 ChatGPT by OpenAI (openai.com)\n• Most popular conversational AI with advanced reasoning capabilities\n• Used by over 100 million users worldwide\n\n🥈 Claude by Anthropic (anthropic.com)\n• Known for safety and helpfulness in complex tasks\n• Excellent for research and analysis\n\n🥉 Gemini by Google (google.com)\n• Multimodal capabilities for text, image, and code\n• Integrated with Google's ecosystem\n\n4. GitHub Copilot (github.com)\n• AI-powered code completion and generation\n• Trusted by millions of developers\n\n5. Midjourney (midjourney.com)\n• Leading AI image generation tool\n• Creates stunning visual content\n\n6. Notion AI (notion.com)\n• AI-powered workspace and productivity tool\n• Helps with writing, organization, and collaboration\n\n7. Grammarly (grammarly.com)\n• AI writing assistant with advanced grammar checking\n• Improves writing quality and clarity\n\n8. Jasper (jasper.ai)\n• AI content creation platform for marketing\n• Generates high-quality marketing copy\n\n9. Runway ML (runwayml.com)\n• AI video generation and editing platform\n• Revolutionizing video content creation\n\n10. Replika (replika.com)\n• AI companion and mental health support\n• Personalized conversational experience\n\n💡 Key Insights:\n• AI tools are becoming more specialized and user-friendly\n• Integration with existing workflows is a key trend\n• Focus on productivity and creativity enhancement"

Please provide a response that directly answers the specific query, using domain-based citations and breaking down multiple questions if present:"""
    
    elif is_how_to_query:
        return f"""You are a helpful guide and instructor. Based on the following web search results for "{query}", provide a clear, step-by-step guide.\n{entity_section}\nSEARCH RESULTS:\n{context}\n\nINSTRUCTIONS:\n1. Provide a practical, actionable guide with clear steps\n2. Use numbered steps and bullet points for clarity\n3. Include tips, warnings, and best practices where relevant\n4. DO NOT use markdown symbols (#, *, -, etc.)\n5. {citation_instructions}\n6. {multi_question_instructions}\n7. Include inline citations by referencing the source number [1], [2], etc.\n8. Focus on being helpful and practical\n9. Add relevant emojis to make the guide engaging\n\nFORMAT EXAMPLE for how-to queries:\n"🔧 How to Set Up a Web Search Feature\n\nHere's a comprehensive guide to implementing web search functionality:\n\n📋 Prerequisites\n• API keys for search services (Google, Serper, or Tavily)\n• Backend server with Node.js/Express\n• Frontend with React or similar framework\n\n🚀 Step-by-Step Implementation\n\nStep 1: Set Up Search APIs\n• Obtain API keys from your chosen search provider [1]\n• Configure environment variables for secure access\n• Test API connectivity and rate limits\n\nStep 2: Create Backend Search Service\n• Implement search endpoint in your Express server [2]\n• Add error handling and fallback mechanisms\n• Configure CORS for frontend communication\n\nStep 3: Build Frontend Interface\n• Create search toggle component [3]\n• Implement real-time search results display\n• Add loading states and error handling\n\nStep 4: Integrate with AI Summarization\n• Set up Python microservice for summarization [4]\n• Configure multiple LLM options (GPT-4o, Claude, Gemini)\n• Implement citation and reference system\n\nStep 5: Style and Polish\n• Apply modern UI design with gradients and animations [5]\n• Ensure responsive design for all devices\n• Add accessibility features\n\n💡 Pro Tips:\n• Always implement rate limiting to avoid API costs\n• Use caching for frequently searched terms\n• Provide fallback options for when APIs fail\n• Test thoroughly with various query types\n\n⚠️ Common Pitfalls:\n• Don't forget to handle API errors gracefully\n• Avoid hardcoding API keys in your code\n• Remember to implement proper security measures"

Please provide a helpful, practical guide that directly addresses the query:"""
    
    elif is_definition_query:
        return f"""You are a knowledgeable educator. Based on the following web search results for "{query}", provide a clear, comprehensive explanation.\n{entity_section}\nSEARCH RESULTS:\n{context}\n\nINSTRUCTIONS:\n1. Provide a clear, accurate definition or explanation\n2. Include relevant context, examples, and applications\n3. Use simple language while being comprehensive\n4. DO NOT use markdown symbols (#, *, -, etc.)\n5. {citation_instructions}\n6. {multi_question_instructions}\n7. Include inline citations by referencing the source number [1], [2], etc.\n8. Add relevant emojis to make the explanation engaging\n9. Structure the response logically with clear sections\n\nFORMAT EXAMPLE for definition queries:\n"📚 What is Web Search Integration?\n\nWeb search integration is a technology that combines real-time internet search capabilities with AI-powered applications to provide up-to-date, comprehensive information to users.\n\n🔍 Core Components\n\nSearch APIs: Connect to search engines like Google, Bing, or specialized APIs like Serper.dev [1]. These provide access to current web content and real-time information.\n\nAI Summarization: Use large language models (LLMs) like GPT-4o, Claude, or Gemini to process and summarize search results [2]. This transforms raw web data into coherent, useful information.\n\nFrontend Interface: User-friendly components that allow users to toggle search functionality and view results in an organized, visually appealing format [3].\n\nBackend Processing: Server-side logic that coordinates between search APIs, AI models, and the frontend interface [4].\n\n🚀 Key Benefits\n\nReal-time Information: Access to current events, latest developments, and up-to-date data that AI models might not have in their training data [5].\n\nComprehensive Coverage: Combines multiple information sources to provide well-rounded perspectives on topics.\n\nEnhanced Accuracy: Cross-references information from multiple sources to verify facts and provide reliable information.\n\nUser Control: Allows users to choose when they want web-enhanced responses versus AI-only responses.\n\n💡 Applications\n\nResearch and Analysis: Perfect for academic research, market analysis, and competitive intelligence [6].\n\nNews and Updates: Stay current with breaking news, product releases, and industry developments.\n\nFact-checking: Verify information and get multiple perspectives on controversial topics.\n\nLearning and Education: Access the latest information for educational purposes and skill development.\n\n🔧 Technical Implementation\n\nThe system typically involves:\n• API integration with search providers\n• AI model coordination for summarization\n• Real-time data processing and caching\n• User interface for search control and result display\n• Error handling and fallback mechanisms\n\nThis technology represents a significant advancement in AI applications, bridging the gap between static AI knowledge and dynamic real-world information."

Please provide a clear, comprehensive explanation that directly addresses the query:"""
    
    elif is_comparison_query:
        return f"""You are an expert analyst. Based on the following web search results for "{query}", provide a detailed comparison.\n{entity_section}\nSEARCH RESULTS:\n{context}\n\nINSTRUCTIONS:\n1. Provide a balanced, objective comparison\n2. Use clear comparison tables or structured format\n3. Include pros and cons for each option\n4. DO NOT use markdown symbols (#, *, -, etc.)\n5. {citation_instructions}\n6. {multi_question_instructions}\n7. Include inline citations by referencing the source number [1], [2], etc.\n8. Add relevant emojis to make the comparison engaging\n9. Provide a clear recommendation if appropriate\n\nFORMAT EXAMPLE for comparison queries:\n"⚖️ GPT-4o vs Claude vs Gemini: AI Model Comparison\n\nHere's a comprehensive comparison of the three leading AI models based on current capabilities and performance:\n\n📊 Performance Comparison\n\n🤖 GPT-4o (OpenAI)\n• Reasoning: Excellent for complex problem-solving [1]\n• Creativity: Strong creative writing and brainstorming capabilities\n• Speed: Fast response times with good accuracy\n• Cost: Competitive pricing for high-quality output\n• Integration: Extensive API ecosystem and developer tools\n\n🧠 Claude (Anthropic)\n• Safety: Industry-leading safety and helpfulness [2]\n• Analysis: Superior for research and analytical tasks\n• Context: Excellent long-context understanding\n• Ethics: Built with constitutional AI principles\n• Specialization: Strong in academic and professional writing\n\n🌟 Gemini (Google)\n• Multimodal: Best-in-class image, text, and code understanding [3]\n• Integration: Seamless Google ecosystem integration\n• Innovation: Cutting-edge research and development\n• Scalability: Enterprise-grade infrastructure\n• Future-ready: Advanced reasoning and planning capabilities\n\n📈 Key Metrics Comparison\n\n| Feature | GPT-4o | Claude | Gemini |\n|---------|--------|--------|--------|\n| Reasoning | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |\n| Creativity | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |\n| Safety | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |\n| Speed | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |\n| Cost | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |\n\n🎯 Use Case Recommendations\n\nChoose GPT-4o for:\n• General-purpose AI tasks and creative projects\n• Fast, reliable responses for everyday use\n• Extensive API integration needs\n\nChoose Claude for:\n• Research and analysis tasks\n• Safety-critical applications\n• Academic and professional writing\n\nChoose Gemini for:\n• Multimodal applications (text + images)\n• Google ecosystem integration\n• Cutting-edge AI research and development\n\n💡 Final Verdict\n\nEach model excels in different areas, making the choice dependent on your specific needs. For general use, GPT-4o offers the best balance of capabilities and accessibility. For research and safety-critical applications, Claude is the top choice. For multimodal and Google-integrated solutions, Gemini leads the way."

Please provide a detailed, balanced comparison that directly addresses the query:"""
    
    elif is_news_query:
        return f"""You are a news analyst and reporter. Based on the following web search results for "{query}", provide the latest news and developments.\n{entity_section}\nSEARCH RESULTS:\n{context}\n\nINSTRUCTIONS:\n1. Focus on the most recent and relevant news\n2. Provide context and background information\n3. Include multiple perspectives when available\n4. DO NOT use markdown symbols (#, *, -, etc.)\n5. {citation_instructions}\n6. {multi_question_instructions}\n7. Include inline citations by referencing the source number [1], [2], etc.\n8. Add relevant emojis to make the news engaging\n9. Structure with clear sections for different aspects\n\nFORMAT EXAMPLE for news queries:\n"📰 Latest AI Developments and Breakthroughs\n\nHere are the most recent and significant developments in artificial intelligence:\n\n🚀 Major Announcements\n\nOpenAI's GPT-5 Development: OpenAI has officially confirmed they are working on GPT-5, the next generation of their language model [1]. The company expects significant improvements in reasoning, creativity, and multimodal capabilities.\n\nGoogle's Gemini 2.0 Release: Google has launched Gemini 2.0 with enhanced reasoning abilities and improved performance across all benchmarks [2]. The new model shows 40% improvement in complex problem-solving tasks.\n\nAnthropic's Constitutional AI Advances: Anthropic has published new research on constitutional AI, demonstrating improved safety and alignment in large language models [3]. Their latest models show better adherence to safety principles.\n\n💼 Industry Impact\n\nInvestment Surge: AI startups have seen a 150% increase in funding compared to last year [4]. Major investments are flowing into AI infrastructure, applications, and research.\n\nEnterprise Adoption: 78% of Fortune 500 companies are now actively implementing AI solutions [5]. The focus is shifting from experimentation to production deployment.\n\nRegulatory Developments: New AI regulations are being proposed in the EU and US [6]. These focus on transparency, safety, and responsible AI development.\n\n🔬 Research Breakthroughs\n\nMultimodal AI: Researchers have achieved breakthroughs in combining text, image, and audio understanding [7]. This enables more human-like AI interactions.\n\nAI Reasoning: New techniques have significantly improved AI's ability to reason through complex problems [8]. This includes better logical thinking and step-by-step problem solving.\n\nEnergy Efficiency: AI models are becoming more energy-efficient, reducing environmental impact [9]. New training methods can reduce energy consumption by up to 70%.\n\n🎯 Future Outlook\n\nShort-term (6-12 months): Expect more specialized AI models for specific industries and use cases [10]. Integration with existing business processes will accelerate.\n\nMedium-term (1-2 years): AI will become more autonomous and capable of complex decision-making. We'll see more AI agents that can work independently.\n\nLong-term (3-5 years): AI will likely achieve human-level performance in many cognitive tasks. The focus will shift to AI-human collaboration and augmentation.\n\n💡 Key Takeaways\n\n• AI development is accelerating rapidly with major breakthroughs every few months\n• Industry adoption is moving from experimentation to production\n• Regulatory frameworks are evolving to ensure responsible AI development\n• The focus is shifting toward more specialized and efficient AI models"

Please provide the latest news and developments that directly address the query:"""
    
    elif is_technical_query:
        return f"""You are a technical expert and developer. Based on the following web search results for "{query}", provide technical guidance and implementation details.\n{entity_section}\nSEARCH RESULTS:\n{context}\n\nINSTRUCTIONS:\n1. Provide technical details and implementation guidance\n2. Include code examples, architecture considerations, and best practices\n3. Address technical challenges and solutions\n4. DO NOT use markdown symbols (#, *, -, etc.)\n5. {citation_instructions}\n6. {multi_question_instructions}\n7. Include inline citations by referencing the source number [1], [2], etc.\n8. Add relevant emojis to make the technical content engaging\n9. Structure with clear sections for different technical aspects\n\nFORMAT EXAMPLE for technical queries:\n"⚙️ Technical Implementation of Web Search Integration\n\nHere's a comprehensive technical guide for implementing web search functionality:\n\n🏗️ Architecture Overview\n\nThe system consists of three main components:\n• Frontend: React/TypeScript interface for user interaction\n• Backend: Node.js/Express API for request handling\n• Python Microservice: FastAPI service for AI summarization\n\n🔧 Backend Implementation\n\nAPI Endpoint Structure:\n    // Search endpoint\n    POST /api/search\n    {{\n      \"query\": \"string\",\n      \"model\": \"gpt-4o|claude|gemini\"\n    }}\n\n    // Response structure\n    {{\n      \"searchResults\": {{...}},\n      \"summary\": \"string\",\n      \"modelUsed\": \"string\"\n    }}\n\nSearch Service Integration:\n• Google Custom Search API as primary [1]\n• Serper.dev and Tavily as fallbacks\n• Error handling and rate limiting\n• Caching for frequently searched terms\n\n🤖 Python Microservice\n\nFastAPI Implementation:\n    @app.post(\"/summarize\")\n    async def summarize(request: SummarizeRequest):\n        # Process search results\n        # Generate AI summary\n        # Return formatted response\n\nLLM Integration:\n• OpenAI GPT-4o for primary summarization [2]\n• Claude and Gemini as alternatives\n• Model fallback mechanisms\n• Error handling and retry logic\n\n🎨 Frontend Components\n\nSearch Toggle Component:\n• React state management for search toggle\n• Real-time UI updates\n• Loading states and error handling\n\nResults Display:\n• Responsive design with Tailwind CSS\n• Citation system with clickable links\n• Professional typography with Satoshi font\n\n🔒 Security Considerations\n\nAPI Key Management:\n• Environment variables for sensitive data\n• Secure key rotation mechanisms\n• Rate limiting to prevent abuse\n\nData Privacy:\n• No storage of search queries\n• Secure transmission of data\n• Compliance with privacy regulations\n\n📊 Performance Optimization\n\nCaching Strategy:\n• Redis for search result caching [3]\n• CDN for static assets\n• Database optimization for conversation storage\n\nLoad Balancing:\n• Horizontal scaling for high traffic\n• Health checks and failover\n• Monitoring and alerting\n\n🧪 Testing Strategy\n\nUnit Tests:\n• API endpoint testing\n• Search service validation\n• AI model integration testing\n\nIntegration Tests:\n• End-to-end workflow testing\n• Cross-browser compatibility\n• Performance benchmarking\n\n🚀 Deployment\n\nContainerization:\n• Docker containers for each service\n• Kubernetes orchestration for scaling\n• CI/CD pipeline for automated deployment\n\nMonitoring:\n• Application performance monitoring\n• Error tracking and alerting\n• Usage analytics and reporting\n\n💡 Best Practices\n\n• Always implement proper error handling\n• Use environment-specific configurations\n• Monitor API usage and costs\n• Implement comprehensive logging\n• Regular security audits and updates"\n\nPlease provide technical guidance that directly addresses the query:"""
    
    else:
        # Default dynamic response for general queries
        return f"""You are a helpful AI assistant. Based on the following web search results for "{query}", provide a comprehensive and useful response.\n{entity_section}\nSEARCH RESULTS:\n{context}\n\nINSTRUCTIONS:\n1. Analyze the query and provide the most relevant and helpful information\n2. Structure your response logically based on the query type\n3. Use clear, engaging formatting with appropriate emojis\n4. DO NOT use markdown symbols (#, *, -, etc.)\n5. {citation_instructions}\n6. {multi_question_instructions}\n7. Focus on being genuinely helpful and informative\n8. Adapt the format to best serve the specific query\n\nFORMAT GUIDELINES:\n• Use emojis to highlight important sections\n• Include bullet points for lists and key information\n• Provide context and background when relevant\n• Structure with clear sections for different aspects\n• Make the response directly answer what was asked\n\nPlease provide a helpful, comprehensive response that directly addresses the query, using domain-based citations and breaking down multiple questions if present:"""

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    query = request.query
    search_results = [r.dict() for r in request.results]
    model = request.model
    
    logger.info(f"Processing summarize request for query: {query} with {len(search_results)} results using model: {model}")

    prompt = create_search_agent_prompt(query, search_results)
    
    summary = None
    model_used = model

    try:
        if model == "gpt-4o":
            logger.info("Using GPT-4o for summarization...")
            client = openai.OpenAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7,
            )
            summary = response.choices[0].message.content
            logger.info("GPT-4o summarization completed")
            
        elif model == "claude":
            logger.info("Using Claude for summarization...")
            for model_name in CLAUDE_MODELS:
                try:
                    logger.info(f"Trying Claude model: {model_name} ...")
                    client_anthropic = anthropic.Anthropic(api_key=anthropic_api_key)
                    claude_response = client_anthropic.messages.create(
                        model=model_name,
                        max_tokens=800,
                        temperature=0.7,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    summary = claude_response.content[0].text
                    model_used = model_name
                    logger.info(f"Claude summarization completed with model: {model_name}")
                    break
                except Exception as e:
                    logger.warning(f"Claude model {model_name} failed: {str(e)}")
                    continue
                    
        elif model == "gemini":
            logger.info("Using Gemini for summarization...")
            for model_name in GEMINI_MODELS:
                try:
                    logger.info(f"Trying Gemini model: {model_name} ...")
                    genai_model = genai.GenerativeModel(model_name)
                    gemini_response = genai_model.generate_content(prompt)
                    summary = gemini_response.text
                    model_used = model_name
                    logger.info(f"Gemini summarization completed with model: {model_name}")
                    break
                except Exception as e:
                    logger.warning(f"Gemini model {model_name} failed: {str(e)}")
                    continue
        
        if not summary:
            summary = f"Unable to generate summary with the selected model: {model}"
            
    except Exception as e:
        logger.error(f"Error in summarize endpoint: {str(e)}")
        summary = f"Error generating summary: {str(e)}"

    return SummarizeResponse(
        summary=summary,
        model_used=model_used
    ) 

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Web Search Summarizer Agent...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📋 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info") 