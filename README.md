# Deep Research System

A comprehensive research automation system built with Crew AI, featuring multiple specialized agents working together to produce high-quality research results. Supports multiple AI providers including OpenAI, Anthropic Claude, and Google Gemini.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for different research tasks
- **Multi-AI Provider Support**: OpenAI GPT-4, Anthropic Claude, Google Gemini
- **Comprehensive Research**: Multiple depth levels (basic, comprehensive, expert)
- **Multiple Data Sources**: Web search, academic papers, Wikipedia, arXiv, and more
- **Data Analysis**: Statistical analysis, visualization, and pattern recognition
- **Quality Assurance**: Content editing and review processes
- **Multiple Output Formats**: Markdown, HTML, JSON
- **Research History**: Track and analyze previous research projects

## 🤖 Research Agents

The system includes the following specialized agents:

1. **Research Project Manager**: Coordinates the entire research process
2. **Primary Research Specialist**: Conducts comprehensive information gathering
3. **Data Analysis Specialist**: Performs statistical analysis and creates visualizations
4. **Content Editor**: Reviews and enhances content quality
5. **Report Generator**: Synthesizes findings into comprehensive reports
6. **Specialist Agents**: Domain-specific experts (Technology, Business, Science, Finance)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Clone or download the project
cd MultiModalMind

# Install required packages
pip install -r requirements.txt
```

### API Keys Setup

**Required**: At least one AI provider API key
- **OpenAI API Key** (for GPT-4)
- **Anthropic API Key** (for Claude)
- **Google API Key** (for Gemini)

**Recommended**: Tavily API Key for enhanced search capabilities

**Alternative Search APIs**: The system supports multiple search engines including:
- **Google Custom Search API** (recommended alternative to Travily)
- **Serper.dev API** (Google search results)
- **Brave Search API** (privacy-focused)
- **DuckDuckGo** (free, no API key required)

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your API keys
nano .env
```

Or set environment variables:

```bash
# Choose one or more AI providers
export OPENAI_API_KEY="your_openai_api_key_here"
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
export GOOGLE_API_KEY="your_google_api_key_here"

# Optional search API
export TAVILY_API_KEY="your_tavily_api_key_here"

# Alternative search APIs
export SERPER_API_KEY="your_serper_api_key_here"
export GOOGLE_SEARCH_API_KEY="your_google_search_api_key_here"
export GOOGLE_SEARCH_ENGINE_ID="your_google_search_engine_id_here"
export BRAVE_API_KEY="your_brave_api_key_here"

# Set your preferred AI provider
export PREFERRED_AI_PROVIDER="openai"  # or "anthropic" or "google"
```

## 📖 Usage

### Command Line Interface

```bash
# Basic research with default AI provider
python main.py --topic "artificial intelligence trends 2024"

# Research with specific AI provider
python main.py --topic "AI in healthcare" --provider anthropic

# Comprehensive research for academic audience
python main.py --topic "climate change impact" --depth expert --audience academic

# Custom output format
python main.py --topic "blockchain technology" --format html --no-save

# Show available AI providers
python main.py --show-providers
```

### Programmatic Usage

```python
from deep_research_system.research_system import DeepResearchSystem

# Initialize the system
research_system = DeepResearchSystem()

# Conduct research
results = research_system.conduct_research(
    topic="renewable energy trends",
    research_depth="comprehensive",
    target_audience="business",
    output_format="markdown"
)

# Access results
print(f"Research completed in {results['execution_time']:.2f} seconds")
print(f"AI Provider: {results['ai_provider']}")
print(f"AI Model: {results['ai_model']}")
print(f"Summary: {results['summary']}")
print(f"Key findings: {results['key_findings']}")

# Get provider information
provider_info = research_system.get_provider_info()
print(f"Available providers: {provider_info['available_providers']}")
```

### Example Scripts

Run the comprehensive example script:

```bash
python example_usage.py
```

Quick start with provider check:

```bash
python quick_start.py --providers
python quick_start.py
```

## 🔧 Configuration

### AI Provider Configuration

| Provider | Model | API Key Required |
|----------|-------|------------------|
| **OpenAI** | GPT-4, GPT-3.5-turbo | `OPENAI_API_KEY` |
| **Anthropic** | Claude-3-Sonnet, Claude-3-Haiku | `ANTHROPIC_API_KEY` |
| **Google** | Gemini Pro | `GOOGLE_API_KEY` |

Set your preferred provider in the `.env` file:
```bash
PREFERRED_AI_PROVIDER=openai  # or anthropic or google
```

### Research Depth Levels

- **Basic**: Quick overview with essential information
- **Comprehensive**: Detailed research with multiple sources and analysis
- **Expert**: In-depth research with specialized agents and advanced analysis

### Target Audiences

- **General**: Accessible language for broad audience
- **Academic**: Formal academic style with detailed citations
- **Business**: Focus on practical insights and business implications
- **Technical**: Technical details and specifications

### Output Formats

- **Markdown**: Structured text format with headers and lists
- **HTML**: Web-ready format with styling
- **JSON**: Machine-readable structured data

## 📁 Project Structure

```
MultiModalMind/
├── deep_research_system/
│   ├── __init__.py
│   ├── config.py                 # Configuration management
│   ├── research_system.py        # Main research system
│   ├── agents/
│   │   ├── __init__.py
│   │   └── research_agents.py    # Agent definitions
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── research_tasks.py     # Task definitions
│   └── tools/
│       ├── __init__.py
│       ├── search_tools.py       # Search and data collection tools
│       └── analysis_tools.py     # Data analysis and visualization tools
├── main.py                       # Command line interface
├── example_usage.py              # Usage examples
├── quick_start.py                # Quick start and testing
├── setup.py                      # Setup and installation
├── requirements.txt              # Python dependencies
├── env.example                   # Environment variables template
└── README.md                     # This file
```

## 🔍 Research Process

The system follows a comprehensive research workflow:

1. **Planning**: Research objectives, questions, and methodology
2. **Initial Research**: Broad information gathering from multiple sources
3. **Deep Dive**: Detailed investigation of specific areas (comprehensive/expert)
4. **Data Analysis**: Pattern recognition, statistical analysis, visualization
5. **Content Editing**: Quality assurance and content enhancement
6. **Report Generation**: Synthesis into comprehensive report
7. **Final Review**: Quality assessment and approval

## 🛠️ Customization

### Adding New Agents

```python
from deep_research_system.agents.research_agents import ResearchAgentFactory

# Create a custom specialist agent
custom_agent = ResearchAgentFactory.create_specialist_agent("your_specialty")
```

### Adding New Tools

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class CustomTool(BaseTool):
    name = "custom_tool"
    description = "Your custom tool description"
    
    class InputSchema(BaseModel):
        input_param: str = Field(description="Input parameter")
    
    def _run(self, input_param: str):
        # Your tool implementation
        return {"result": "tool output"}
```

### Custom Research Workflow

```python
from deep_research_system.research_system import DeepResearchSystem

class CustomResearchSystem(DeepResearchSystem):
    def custom_research_method(self, topic: str):
        # Your custom research implementation
        pass
```

## 📊 Output Examples

### Markdown Output

```markdown
# Deep Research Report: Artificial Intelligence Trends 2024

## Executive Summary
Comprehensive analysis of AI trends in 2024...

## Research Details
- **Topic**: Artificial Intelligence Trends 2024
- **Research Depth**: Comprehensive
- **Target Audience**: Business
- **AI Provider**: OPENAI
- **AI Model**: gpt-4
- **Execution Time**: 45.23 seconds

## Key Findings
1. AI adoption increased by 40% in 2024
2. Focus on responsible AI development
3. Integration with existing business processes

## Recommendations
1. Invest in AI training for employees
2. Develop AI ethics guidelines
3. Start with pilot projects
```

### HTML Output

The HTML output includes:
- Professional styling
- Interactive charts (if generated)
- Responsive design
- Easy navigation

## 🔧 Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: At least one AI provider API key is required
   ```
   Solution: Set at least one AI provider API key in environment variables or .env file

2. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'crewai'
   ```
   Solution: Install dependencies with `pip install -r requirements.txt`

3. **Search Tool Failures**
   ```
   Tavily search failed: API key not found
   ```
   Solution: Tavily is optional. The system will fall back to DuckDuckGo search.

4. **Provider Selection Issues**
   ```
   Error: Preferred AI provider not available
   ```
   Solution: Check that the API key for your preferred provider is set correctly

### Performance Tips

- Use "basic" depth for quick research
- Set appropriate target audience for better results
- Use JSON format for programmatic processing
- Monitor API usage to avoid rate limits
- Choose the AI provider that best fits your needs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Crew AI](https://github.com/joaomdmoura/crewAI) - Multi-agent framework
- [LangChain](https://github.com/langchain-ai/langchain) - LLM framework
- [OpenAI](https://openai.com/) - GPT models
- [Anthropic](https://www.anthropic.com/) - Claude models
- [Google](https://ai.google.dev/) - Gemini models
- [Tavily](https://tavily.com/) - Search API

## 📞 Support

For questions, issues, or contributions:

1. Check the troubleshooting section
2. Review example usage
3. Open an issue on GitHub
4. Contact the development team

---

**Happy Researching! 🚀** 