"""
Main Deep Research System using Crew AI
"""
import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from crewai import Crew, Process
from deep_research_system.config import Config
from deep_research_system.agents.research_agents import ResearchTeam, ResearchAgentFactory
from deep_research_system.tasks.research_tasks import ResearchTaskFactory
from deep_research_system.tools.search_tools import SearchResult

class DeepResearchSystem:
    """
    Comprehensive deep research system using multiple specialized agents
    """
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """
        Initialize the Deep Research System
        
        Args:
            api_keys: Dictionary of API keys (OpenAI, Anthropic, Google, etc.)
        """
        self.config = Config()
        self._setup_api_keys(api_keys)
        self._validate_config()
        self._display_provider_info()
        self.research_history = []
        
    def _setup_api_keys(self, api_keys: Optional[Dict[str, str]]):
        """Setup API keys from environment or provided dictionary"""
        if api_keys:
            for key, value in api_keys.items():
                os.environ[key] = value
                
        # Validate required API keys
        available_providers = self.config.get_available_providers()
        if not any(available_providers.values()):
            raise ValueError("At least one AI provider API key is required (OpenAI, Anthropic, or Google). Please set the appropriate API key in environment variables or provide in api_keys parameter.")
    
    def _validate_config(self):
        """Validate configuration and report any issues"""
        issues = self.config.validate_config()
        if issues:
            print("Configuration warnings:")
            for key, message in issues.items():
                print(f"  - {key}: {message}")
    
    def _display_provider_info(self):
        """Display information about the current AI provider configuration"""
        provider_info = self.config.get_provider_info()
        available = provider_info["available_providers"]
        
        print("🤖 AI Provider Configuration:")
        print(f"  Preferred Provider: {provider_info['preferred_provider'].upper()}")
        print(f"  Current Model: {provider_info['current_model']}")
        print(f"  Temperature: {provider_info['current_temperature']}")
        print(f"  Max Tokens: {provider_info['current_max_tokens']}")
        
        print("  Available Providers:")
        for provider, is_available in available.items():
            status = "✅" if is_available else "❌"
            print(f"    {status} {provider.upper()}")
    
    def conduct_research(
        self,
        topic: str,
        research_depth: str = "comprehensive",
        target_audience: str = "general",
        max_iterations: int = None,
        output_format: str = "markdown",
        save_results: bool = True
    ) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a given topic
        
        Args:
            topic: Research topic
            research_depth: Level of research depth ("basic", "comprehensive", "expert")
            target_audience: Target audience for the report
            max_iterations: Maximum number of research iterations
            output_format: Output format ("markdown", "pdf", "html", "json")
            save_results: Whether to save results to file
            
        Returns:
            Dictionary containing research results
        """
        print(f"🚀 Starting Deep Research on: {topic}")
        print(f"📊 Research Depth: {research_depth}")
        print(f"👥 Target Audience: {target_audience}")
        print(f"🤖 AI Provider: {self.config.PREFERRED_AI_PROVIDER.upper()}")
        
        start_time = time.time()
        
        try:
            # Create research team
            research_team = ResearchTeam(topic, research_depth)
            agents = research_team.get_agents()
            
            print(f"👨‍💼 Research Team Created: {len(agents)} agents")
            for role in research_team.get_agent_roles():
                print(f"  - {role}")
            
            # Create tasks
            tasks = self._create_research_tasks(
                research_team, topic, research_depth, target_audience
            )
            
            # Create and run crew
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )
            
            print("🔄 Starting Research Process...")
            result = crew.kickoff()
            
            # Process and format results
            research_results = self._process_results(
                result, topic, research_depth, target_audience, start_time
            )
            
            # Save results if requested
            if save_results:
                self._save_results(research_results, output_format)
            
            # Add to history
            self.research_history.append({
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "results": research_results
            })
            
            print(f"✅ Research Completed Successfully!")
            print(f"⏱️  Total Time: {time.time() - start_time:.2f} seconds")
            
            return research_results
            
        except Exception as e:
            print(f"❌ Research failed: {str(e)}")
            raise
    
    def _create_research_tasks(
        self,
        research_team: ResearchTeam,
        topic: str,
        research_depth: str,
        target_audience: str
    ) -> List:
        """Create the sequence of research tasks"""
        tasks = []
        
        # Get agents
        manager_agent = research_team.get_agent("manager")
        researcher_agent = research_team.get_agent("researcher")
        analyst_agent = research_team.get_agent("analyst")
        editor_agent = research_team.get_agent("editor")
        reporter_agent = research_team.get_agent("reporter")
        
        # Task 1: Planning
        planning_task = ResearchTaskFactory.create_planning_task(
            manager_agent, topic, research_depth
        )
        tasks.append(planning_task)
        
        # Task 2: Initial Research
        initial_research_task = ResearchTaskFactory.create_initial_research_task(
            researcher_agent, topic, "Research plan from previous task"
        )
        tasks.append(initial_research_task)
        
        # Task 3: Deep Dive Research (if comprehensive or expert depth)
        if research_depth in ["comprehensive", "expert"]:
            deep_dive_task = ResearchTaskFactory.create_deep_dive_task(
                researcher_agent, topic, "Initial findings from previous task", 
                ["Key areas identified from initial research"]
            )
            tasks.append(deep_dive_task)
        
        # Task 4: Data Analysis
        analysis_task = ResearchTaskFactory.create_data_analysis_task(
            analyst_agent, "Research findings from previous tasks"
        )
        tasks.append(analysis_task)
        
        # Task 5: Content Editing
        editing_task = ResearchTaskFactory.create_content_editing_task(
            editor_agent, "Research content from previous tasks", 
            "Quality criteria from planning phase"
        )
        tasks.append(editing_task)
        
        # Task 6: Report Generation
        report_task = ResearchTaskFactory.create_report_generation_task(
            reporter_agent, "Research findings from previous tasks",
            "Analysis results from previous tasks", target_audience
        )
        tasks.append(report_task)
        
        # Task 7: Final Review
        final_review_task = ResearchTaskFactory.create_final_review_task(
            manager_agent, "Final report from previous task",
            "Original objectives from planning phase"
        )
        tasks.append(final_review_task)
        
        return tasks
    
    def _process_results(
        self,
        crew_result: Any,
        topic: str,
        research_depth: str,
        target_audience: str,
        start_time: float
    ) -> Dict[str, Any]:
        """Process and structure the research results"""
        return {
            "topic": topic,
            "research_depth": research_depth,
            "target_audience": target_audience,
            "ai_provider": self.config.PREFERRED_AI_PROVIDER,
            "ai_model": self.config.get_agent_config("manager")["model"],
            "timestamp": datetime.now().isoformat(),
            "execution_time": time.time() - start_time,
            "results": crew_result,
            "summary": self._extract_summary(crew_result),
            "key_findings": self._extract_key_findings(crew_result),
            "recommendations": self._extract_recommendations(crew_result),
            "sources": self._extract_sources(crew_result)
        }
    
    def _extract_summary(self, result: Any) -> str:
        """Extract executive summary from results"""
        if hasattr(result, 'raw') and result.raw:
            return str(result.raw)
        return str(result)
    
    def _extract_key_findings(self, result: Any) -> List[str]:
        """Extract key findings from results"""
        # This would need to be implemented based on the actual result structure
        return ["Key findings extracted from research results"]
    
    def _extract_recommendations(self, result: Any) -> List[str]:
        """Extract recommendations from results"""
        # This would need to be implemented based on the actual result structure
        return ["Recommendations extracted from research results"]
    
    def _extract_sources(self, result: Any) -> List[Dict[str, str]]:
        """Extract sources from results"""
        # This would need to be implemented based on the actual result structure
        return [{"title": "Source", "url": "URL", "type": "web"}]
    
    def _save_results(self, results: Dict[str, Any], output_format: str):
        """Save research results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_safe = "".join(c for c in results["topic"] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        topic_safe = topic_safe.replace(' ', '_')
        
        # Create output directory
        os.makedirs("research_outputs", exist_ok=True)
        
        filename = f"research_outputs/{topic_safe}_{timestamp}"
        
        if output_format == "json":
            with open(f"{filename}.json", "w") as f:
                json.dump(results, f, indent=2)
        elif output_format == "markdown":
            with open(f"{filename}.md", "w") as f:
                f.write(self._format_markdown(results))
        elif output_format == "html":
            with open(f"{filename}.html", "w") as f:
                f.write(self._format_html(results))
        
        print(f"💾 Results saved to: {filename}.{output_format}")
    
    def _format_markdown(self, results: Dict[str, Any]) -> str:
        """Format results as markdown"""
        md = f"""# Deep Research Report: {results['topic']}

## Executive Summary
{results['summary']}

## Research Details
- **Topic**: {results['topic']}
- **Research Depth**: {results['research_depth']}
- **Target Audience**: {results['target_audience']}
- **AI Provider**: {results['ai_provider'].upper()}
- **AI Model**: {results['ai_model']}
- **Timestamp**: {results['timestamp']}
- **Execution Time**: {results['execution_time']:.2f} seconds

## Key Findings
"""
        for finding in results['key_findings']:
            md += f"- {finding}\n"
        
        md += "\n## Recommendations\n"
        for rec in results['recommendations']:
            md += f"- {rec}\n"
        
        md += "\n## Sources\n"
        for source in results['sources']:
            md += f"- [{source['title']}]({source['url']}) ({source['type']})\n"
        
        return md
    
    def _format_html(self, results: Dict[str, Any]) -> str:
        """Format results as HTML"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Deep Research Report: {results['topic']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .summary {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
        .details {{ background-color: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        ul {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>Deep Research Report: {results['topic']}</h1>
    
    <h2>Executive Summary</h2>
    <div class="summary">{results['summary']}</div>
    
    <h2>Research Details</h2>
    <div class="details">
        <p><strong>Topic:</strong> {results['topic']}</p>
        <p><strong>Research Depth:</strong> {results['research_depth']}</p>
        <p><strong>Target Audience:</strong> {results['target_audience']}</p>
        <p><strong>AI Provider:</strong> {results['ai_provider'].upper()}</p>
        <p><strong>AI Model:</strong> {results['ai_model']}</p>
        <p><strong>Timestamp:</strong> {results['timestamp']}</p>
        <p><strong>Execution Time:</strong> {results['execution_time']:.2f} seconds</p>
    </div>
    
    <h2>Key Findings</h2>
    <ul>
"""
        for finding in results['key_findings']:
            html += f"        <li>{finding}</li>\n"
        
        html += """    </ul>
    
    <h2>Recommendations</h2>
    <ul>
"""
        for rec in results['recommendations']:
            html += f"        <li>{rec}</li>\n"
        
        html += """    </ul>
    
    <h2>Sources</h2>
    <ul>
"""
        for source in results['sources']:
            html += f'        <li><a href="{source["url"]}">{source["title"]}</a> ({source["type"]})</li>\n'
        
        html += """    </ul>
</body>
</html>"""
        
        return html
    
    def get_research_history(self) -> List[Dict[str, Any]]:
        """Get research history"""
        return self.research_history
    
    def export_research_history(self, filename: str = "research_history.json"):
        """Export research history to file"""
        with open(filename, "w") as f:
            json.dump(self.research_history, f, indent=2)
        print(f"📚 Research history exported to: {filename}")
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get current AI provider information"""
        return self.config.get_provider_info()

# Export the main class
__all__ = ["DeepResearchSystem"] 