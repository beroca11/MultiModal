"""
Specialized research agents for comprehensive deep research
"""
from crewai import Agent
from typing import List, Dict, Any
from deep_research_system.config import Config
from deep_research_system.tools.search_tools import web_search_tool, academic_search_tool, content_extraction_tool
from deep_research_system.tools.analysis_tools import text_analysis_tool, data_visualization_tool, statistical_analysis_tool

class ResearchAgentFactory:
    """Factory for creating specialized research agents"""
    
    @staticmethod
    def create_manager_agent() -> Agent:
        """Create the research manager agent"""
        return Agent(
            role="Research Project Manager",
            goal="Coordinate and oversee the entire research process, ensuring all agents work together effectively to produce comprehensive research results",
            backstory="""You are an experienced research project manager with expertise in coordinating complex research projects. 
            You excel at breaking down research topics into manageable tasks, assigning appropriate agents to specific areas, 
            and ensuring the final research output is comprehensive, well-structured, and meets the highest quality standards. 
            You have a strong background in project management and research methodology.""",
            allow_delegation=True,
            tools=[
                web_search_tool,
                academic_search_tool,
                text_analysis_tool
            ],
            **Config.get_agent_config("manager")
        )
    
    @staticmethod
    def create_researcher_agent() -> Agent:
        """Create the primary researcher agent"""
        return Agent(
            role="Primary Research Specialist",
            goal="Conduct comprehensive research on assigned topics, gather high-quality information from multiple sources, and identify key insights and patterns",
            backstory="""You are a skilled research specialist with expertise in gathering and analyzing information from diverse sources. 
            You have a keen eye for identifying credible sources, extracting relevant information, and synthesizing findings into coherent insights. 
            Your research methodology is thorough and systematic, ensuring no important information is overlooked.""",
            allow_delegation=False,
            tools=[
                web_search_tool,
                academic_search_tool,
                content_extraction_tool,
                text_analysis_tool
            ],
            **Config.get_agent_config("researcher")
        )
    
    @staticmethod
    def create_analyst_agent() -> Agent:
        """Create the data analyst agent"""
        return Agent(
            role="Data Analysis Specialist",
            goal="Analyze research data, identify patterns and trends, perform statistical analysis, and create visualizations to support research findings",
            backstory="""You are a data analysis expert with strong skills in statistical analysis, data visualization, and pattern recognition. 
            You excel at transforming raw research data into meaningful insights through quantitative analysis, creating compelling visualizations, 
            and identifying correlations and trends that support research conclusions. Your analytical approach is both rigorous and creative.""",
            allow_delegation=False,
            tools=[
                text_analysis_tool,
                data_visualization_tool,
                statistical_analysis_tool,
                web_search_tool
            ],
            **Config.get_agent_config("analyst")
        )
    
    @staticmethod
    def create_editor_agent() -> Agent:
        """Create the content editor agent"""
        return Agent(
            role="Content Editor and Quality Assurance Specialist",
            goal="Review, edit, and enhance research content for clarity, accuracy, coherence, and professional presentation",
            backstory="""You are a senior content editor with extensive experience in academic and professional writing. 
            You have a strong command of language, excellent attention to detail, and the ability to improve content structure and flow. 
            You ensure that all research outputs meet the highest standards of quality, accuracy, and readability while maintaining the integrity of the original findings.""",
            allow_delegation=False,
            tools=[
                text_analysis_tool,
                web_search_tool
            ],
            **Config.get_agent_config("editor")
        )
    
    @staticmethod
    def create_reporter_agent() -> Agent:
        """Create the report generator agent"""
        return Agent(
            role="Research Report Generator",
            goal="Synthesize all research findings into comprehensive, well-structured reports with clear conclusions and actionable insights",
            backstory="""You are an expert report writer with a talent for synthesizing complex information into clear, compelling narratives. 
            You excel at organizing research findings into logical structures, creating executive summaries, and presenting information in formats 
            that are accessible to different audiences. Your reports are known for their clarity, thoroughness, and actionable insights.""",
            allow_delegation=False,
            tools=[
                text_analysis_tool,
                data_visualization_tool,
                web_search_tool
            ],
            **Config.get_agent_config("reporter")
        )
    
    @staticmethod
    def create_specialist_agent(specialty: str) -> Agent:
        """Create a specialist agent for specific domains"""
        specialties = {
            "technology": {
                "role": "Technology Research Specialist",
                "goal": "Conduct in-depth research on technology trends, innovations, and technical specifications",
                "backstory": "You are a technology expert with deep knowledge of current tech trends, emerging technologies, and technical specifications. You stay updated with the latest developments in software, hardware, and digital innovations."
            },
            "business": {
                "role": "Business Research Specialist", 
                "goal": "Research business strategies, market trends, competitive analysis, and industry insights",
                "backstory": "You are a business research expert with expertise in market analysis, competitive intelligence, business strategies, and industry trends. You understand business models, financial metrics, and market dynamics."
            },
            "science": {
                "role": "Scientific Research Specialist",
                "goal": "Conduct research on scientific topics, peer-reviewed studies, and academic publications",
                "backstory": "You are a scientific research specialist with expertise in academic literature, peer-reviewed studies, and scientific methodology. You understand research design, statistical analysis, and scientific reporting standards."
            },
            "finance": {
                "role": "Financial Research Specialist",
                "goal": "Research financial markets, economic indicators, investment opportunities, and financial analysis",
                "backstory": "You are a financial research expert with deep knowledge of markets, economic indicators, investment strategies, and financial analysis. You understand financial statements, market dynamics, and economic trends."
            }
        }
        
        if specialty not in specialties:
            raise ValueError(f"Unknown specialty: {specialty}. Available: {list(specialties.keys())}")
        
        spec = specialties[specialty]
        
        return Agent(
            role=spec["role"],
            goal=spec["goal"],
            backstory=spec["backstory"],
            allow_delegation=False,
            tools=[
                web_search_tool,
                academic_search_tool,
                content_extraction_tool,
                text_analysis_tool
            ],
            **Config.get_agent_config("researcher")
        )

class ResearchTeam:
    """Manages a team of research agents"""
    
    def __init__(self, topic: str, research_depth: str = "comprehensive"):
        self.topic = topic
        self.research_depth = research_depth
        self.agents = {}
        self._create_team()
    
    def _create_team(self):
        """Create the research team based on topic and depth"""
        # Core team
        self.agents["manager"] = ResearchAgentFactory.create_manager_agent()
        self.agents["researcher"] = ResearchAgentFactory.create_researcher_agent()
        self.agents["analyst"] = ResearchAgentFactory.create_analyst_agent()
        self.agents["editor"] = ResearchAgentFactory.create_editor_agent()
        self.agents["reporter"] = ResearchAgentFactory.create_reporter_agent()
        
        # Add specialists based on topic analysis
        topic_lower = self.topic.lower()
        
        if any(word in topic_lower for word in ["tech", "software", "ai", "machine learning", "programming"]):
            self.agents["tech_specialist"] = ResearchAgentFactory.create_specialist_agent("technology")
        
        if any(word in topic_lower for word in ["business", "market", "company", "industry", "strategy"]):
            self.agents["business_specialist"] = ResearchAgentFactory.create_specialist_agent("business")
        
        if any(word in topic_lower for word in ["science", "research", "study", "experiment", "laboratory"]):
            self.agents["science_specialist"] = ResearchAgentFactory.create_specialist_agent("science")
        
        if any(word in topic_lower for word in ["finance", "investment", "market", "economy", "financial"]):
            self.agents["finance_specialist"] = ResearchAgentFactory.create_specialist_agent("finance")
    
    def get_agents(self) -> List[Agent]:
        """Get all agents in the team"""
        return list(self.agents.values())
    
    def get_agent(self, role: str) -> Agent:
        """Get a specific agent by role"""
        return self.agents.get(role)
    
    def get_agent_roles(self) -> List[str]:
        """Get all agent roles in the team"""
        return list(self.agents.keys())
    
    def add_specialist(self, specialty: str):
        """Add a specialist agent to the team"""
        agent = ResearchAgentFactory.create_specialist_agent(specialty)
        self.agents[f"{specialty}_specialist"] = agent

# Export classes and functions
__all__ = [
    "ResearchAgentFactory",
    "ResearchTeam"
] 