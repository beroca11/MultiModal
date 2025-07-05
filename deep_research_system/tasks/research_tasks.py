"""
Research tasks for the Deep Research System
"""
from crewai import Task
from typing import List, Dict, Any
from deep_research_system.config import Config

class ResearchTaskFactory:
    """Factory for creating research tasks"""
    
    @staticmethod
    def create_planning_task(manager_agent, topic: str, research_depth: str = "comprehensive") -> Task:
        """Create the initial planning task"""
        return Task(
            description=f"""
            As the Research Project Manager, your first task is to create a comprehensive research plan for the topic: "{topic}"
            
            Research Depth: {research_depth}
            
            Your planning should include:
            1. **Research Objectives**: Define clear, specific objectives for this research
            2. **Key Research Questions**: Identify 5-7 critical questions that need to be answered
            3. **Research Scope**: Define what should and should not be included in the research
            4. **Methodology**: Outline the research approach and data collection strategies
            5. **Timeline**: Create a realistic timeline for different research phases
            6. **Resource Requirements**: Identify what tools, sources, and expertise will be needed
            7. **Quality Criteria**: Define what constitutes high-quality research for this topic
            8. **Risk Assessment**: Identify potential challenges and mitigation strategies
            
            Consider the complexity and scope of the topic when creating this plan. The plan should be detailed enough to guide the entire research process while remaining flexible enough to adapt to findings.
            
            Output your plan in a structured format that can be easily shared with the research team.
            """,
            agent=manager_agent,
            expected_output="A comprehensive research plan with objectives, questions, methodology, timeline, and quality criteria",
            context=[f"Research topic: {topic}", f"Research depth: {research_depth}"]
        )
    
    @staticmethod
    def create_initial_research_task(researcher_agent, topic: str, research_plan: str) -> Task:
        """Create the initial research task"""
        return Task(
            description=f"""
            As the Primary Research Specialist, conduct comprehensive initial research on the topic: "{topic}"
            
            Use the research plan provided to guide your investigation:
            {research_plan}
            
            Your research should include:
            1. **Broad Information Gathering**: Collect information from multiple sources including:
               - Web searches for current information
               - Academic databases for scholarly articles
               - Industry reports and white papers
               - News articles and recent developments
            
            2. **Source Evaluation**: Assess the credibility and relevance of each source
            
            3. **Key Findings Identification**: Identify the most important insights and discoveries
            
            4. **Gap Analysis**: Identify areas where information is lacking or contradictory
            
            5. **Trend Analysis**: Identify current trends, patterns, and emerging developments
            
            Focus on gathering diverse perspectives and high-quality information. Document all sources and findings systematically.
            
            Provide a comprehensive research summary that includes:
            - Key findings and insights
            - Important sources and references
            - Identified gaps in knowledge
            - Emerging trends and patterns
            - Recommendations for further investigation
            """,
            agent=researcher_agent,
            expected_output="Comprehensive research findings with sources, insights, gaps, and recommendations",
            context=[f"Research topic: {topic}", f"Research plan: {research_plan}"]
        )
    
    @staticmethod
    def create_deep_dive_task(researcher_agent, topic: str, initial_findings: str, specific_areas: List[str]) -> Task:
        """Create deep dive research tasks for specific areas"""
        areas_text = "\n".join([f"- {area}" for area in specific_areas])
        
        return Task(
            description=f"""
            As the Primary Research Specialist, conduct deep-dive research on specific areas identified from the initial research.
            
            Topic: {topic}
            
            Initial Findings Summary:
            {initial_findings}
            
            Focus Areas for Deep Dive:
            {areas_text}
            
            For each focus area, conduct:
            1. **Detailed Investigation**: Use specialized search strategies and sources
            2. **Expert Opinion Research**: Find and analyze expert perspectives
            3. **Comparative Analysis**: Compare different viewpoints and findings
            4. **Evidence Evaluation**: Assess the strength and reliability of evidence
            5. **Contextual Analysis**: Understand the broader context and implications
            
            Use advanced search techniques and explore:
            - Academic databases and peer-reviewed sources
            - Industry-specific publications
            - Expert blogs and thought leadership content
            - Case studies and real-world examples
            - Statistical data and reports
            
            Provide detailed findings for each focus area with:
            - Comprehensive analysis
            - Supporting evidence and sources
            - Expert opinions and perspectives
            - Implications and conclusions
            - Recommendations for further research
            """,
            agent=researcher_agent,
            expected_output="Detailed research findings for each focus area with analysis, evidence, and recommendations",
            context=[f"Research topic: {topic}", f"Initial findings: {initial_findings}", f"Focus areas: {specific_areas}"]
        )
    
    @staticmethod
    def create_data_analysis_task(analyst_agent, research_data: str) -> Task:
        """Create data analysis task"""
        return Task(
            description=f"""
            As the Data Analysis Specialist, analyze the research data and findings to extract meaningful insights.
            
            Research Data:
            {research_data}
            
            Your analysis should include:
            1. **Pattern Recognition**: Identify recurring themes, patterns, and trends
            2. **Statistical Analysis**: Perform quantitative analysis where applicable
            3. **Sentiment Analysis**: Analyze the tone and sentiment of findings
            4. **Correlation Analysis**: Identify relationships between different factors
            5. **Data Visualization**: Create charts and graphs to illustrate key findings
            6. **Insight Generation**: Extract actionable insights from the data
            7. **Anomaly Detection**: Identify unusual or unexpected findings
            8. **Predictive Analysis**: Identify potential future trends or developments
            
            Use appropriate analytical tools and techniques:
            - Text analysis for qualitative data
            - Statistical analysis for quantitative data
            - Visualization tools for data presentation
            - Trend analysis for temporal patterns
            
            Provide a comprehensive analysis report that includes:
            - Key patterns and trends identified
            - Statistical findings and significance
            - Visual representations of data
            - Insights and implications
            - Recommendations based on analysis
            """,
            agent=analyst_agent,
            expected_output="Comprehensive data analysis with patterns, statistics, visualizations, and insights",
            context=[f"Research data: {research_data}"]
        )
    
    @staticmethod
    def create_content_editing_task(editor_agent, research_content: str, quality_criteria: str) -> Task:
        """Create content editing task"""
        return Task(
            description=f"""
            As the Content Editor and Quality Assurance Specialist, review and enhance the research content for quality, clarity, and professionalism.
            
            Research Content:
            {research_content}
            
            Quality Criteria:
            {quality_criteria}
            
            Your editing responsibilities include:
            1. **Content Review**: Assess the overall quality and completeness of the research
            2. **Clarity Enhancement**: Improve clarity, readability, and flow of the content
            3. **Accuracy Verification**: Check for factual accuracy and consistency
            4. **Structure Improvement**: Organize content in a logical and coherent structure
            5. **Language Refinement**: Enhance language quality and professional tone
            6. **Citation Review**: Ensure proper attribution and citation of sources
            7. **Completeness Check**: Identify and fill any gaps in the research
            8. **Quality Assurance**: Ensure the content meets the specified quality criteria
            
            Focus on:
            - Improving readability and comprehension
            - Ensuring logical flow and organization
            - Maintaining academic/professional standards
            - Enhancing the overall impact of the research
            - Ensuring consistency in style and format
            
            Provide an enhanced version of the research content that meets or exceeds the quality criteria.
            """,
            agent=editor_agent,
            expected_output="Enhanced research content that meets quality criteria with improved clarity, structure, and professionalism",
            context=[f"Research content: {research_content}", f"Quality criteria: {quality_criteria}"]
        )
    
    @staticmethod
    def create_report_generation_task(reporter_agent, research_findings: str, analysis_results: str, target_audience: str = "general") -> Task:
        """Create report generation task"""
        return Task(
            description=f"""
            As the Research Report Generator, synthesize all research findings and analysis into a comprehensive, well-structured report.
            
            Research Findings:
            {research_findings}
            
            Analysis Results:
            {analysis_results}
            
            Target Audience: {target_audience}
            
            Create a professional research report that includes:
            1. **Executive Summary**: Concise overview of key findings and recommendations
            2. **Introduction**: Background, objectives, and methodology
            3. **Literature Review**: Summary of existing knowledge and research
            4. **Methodology**: Detailed description of research approach and methods
            5. **Findings**: Comprehensive presentation of research results
            6. **Analysis**: Detailed analysis and interpretation of findings
            7. **Discussion**: Implications, significance, and broader context
            8. **Conclusions**: Summary of key insights and conclusions
            9. **Recommendations**: Actionable recommendations based on findings
            10. **References**: Complete list of sources and citations
            11. **Appendices**: Supporting data, charts, and additional information
            
            Structure the report appropriately for the target audience:
            - Use clear, accessible language
            - Include relevant visualizations and charts
            - Provide actionable insights and recommendations
            - Ensure professional presentation and formatting
            
            The report should be comprehensive yet accessible, providing valuable insights for decision-making and further research.
            """,
            agent=reporter_agent,
            expected_output="Comprehensive research report with executive summary, findings, analysis, conclusions, and recommendations",
            context=[f"Research findings: {research_findings}", f"Analysis results: {analysis_results}", f"Target audience: {target_audience}"]
        )
    
    @staticmethod
    def create_final_review_task(manager_agent, final_report: str, original_objectives: str) -> Task:
        """Create final review task"""
        return Task(
            description=f"""
            As the Research Project Manager, conduct a final comprehensive review of the research report to ensure it meets all objectives and quality standards.
            
            Final Report:
            {final_report}
            
            Original Research Objectives:
            {original_objectives}
            
            Your final review should assess:
            1. **Objective Achievement**: Verify that all research objectives have been met
            2. **Quality Standards**: Ensure the report meets professional quality standards
            3. **Completeness**: Check that all required sections are present and complete
            4. **Accuracy**: Verify factual accuracy and proper citation of sources
            5. **Clarity**: Ensure the report is clear, well-structured, and accessible
            6. **Coherence**: Check for logical flow and consistency throughout
            7. **Impact**: Assess the overall impact and value of the research
            8. **Recommendations**: Evaluate the quality and feasibility of recommendations
            
            Provide a final assessment that includes:
            - Overall quality rating
            - Achievement of objectives
            - Strengths and areas for improvement
            - Final recommendations for publication or use
            - Any necessary revisions or additions
            
            If the report meets all criteria, approve it for final delivery. If not, provide specific guidance for improvements.
            """,
            agent=manager_agent,
            expected_output="Final review assessment with quality rating, objective achievement, and approval/revision recommendations",
            context=[f"Final report: {final_report}", f"Original objectives: {original_objectives}"]
        )

# Export the factory
__all__ = ["ResearchTaskFactory"] 