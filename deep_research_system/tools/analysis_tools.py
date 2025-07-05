"""
Analysis tools for data processing and visualization
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import json
import re
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class TextAnalysisTool(BaseTool):
    """Tool for analyzing text content"""
    name = "text_analysis"
    description = "Analyze text content for insights, sentiment, and key information"
    
    class InputSchema(BaseModel):
        text: str = Field(description="Text to analyze")
        analysis_type: str = Field(default="all", description="Type of analysis: sentiment, keywords, summary, or all")
    
    def _run(self, text: str, analysis_type: str = "all") -> Dict[str, Any]:
        results = {}
        
        if analysis_type in ["sentiment", "all"]:
            results["sentiment"] = self._analyze_sentiment(text)
        
        if analysis_type in ["keywords", "all"]:
            results["keywords"] = self._extract_keywords(text)
        
        if analysis_type in ["summary", "all"]:
            results["summary"] = self._generate_summary(text)
        
        if analysis_type in ["stats", "all"]:
            results["statistics"] = self._text_statistics(text)
        
        return results
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis"""
        # Simple rule-based sentiment analysis
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'positive', 'beneficial', 'successful']
        negative_words = ['bad', 'terrible', 'awful', 'negative', 'harmful', 'failed', 'problem', 'issue']
        
        words = word_tokenize(text.lower())
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total_words = len(words)
        if total_words == 0:
            return {"sentiment": "neutral", "score": 0.0}
        
        sentiment_score = (positive_count - negative_count) / total_words
        
        if sentiment_score > 0.1:
            sentiment = "positive"
        elif sentiment_score < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": sentiment_score,
            "positive_words": positive_count,
            "negative_words": negative_count
        }
    
    def _extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, Any]]:
        """Extract keywords from text"""
        # Tokenize and clean text
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        
        # Filter and lemmatize words
        filtered_words = [
            lemmatizer.lemmatize(word) for word in words 
            if word.isalnum() and word not in stop_words and len(word) > 2
        ]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        
        # Return top keywords
        keywords = []
        for word, freq in word_freq.most_common(top_n):
            keywords.append({
                "word": word,
                "frequency": freq,
                "percentage": (freq / len(filtered_words)) * 100
            })
        
        return keywords
    
    def _generate_summary(self, text: str, max_sentences: int = 3) -> str:
        """Generate a summary of the text"""
        sentences = sent_tokenize(text)
        
        if len(sentences) <= max_sentences:
            return text
        
        # Simple extractive summarization (first few sentences)
        summary_sentences = sentences[:max_sentences]
        return " ".join(summary_sentences)
    
    def _text_statistics(self, text: str) -> Dict[str, Any]:
        """Calculate text statistics"""
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "average_sentence_length": len(words) / len(sentences) if sentences else 0,
            "unique_words": len(set(words)),
            "lexical_diversity": len(set(words)) / len(words) if words else 0
        }

class DataVisualizationTool(BaseTool):
    """Tool for creating data visualizations"""
    name = "data_visualization"
    description = "Create charts and visualizations from data"
    
    class InputSchema(BaseModel):
        data: str = Field(description="Data in JSON format or pandas DataFrame")
        chart_type: str = Field(description="Type of chart: bar, line, scatter, pie, histogram")
        title: str = Field(default="", description="Chart title")
        x_column: str = Field(default="", description="X-axis column name")
        y_column: str = Field(default="", description="Y-axis column name")
    
    def _run(self, data: str, chart_type: str, title: str = "", x_column: str = "", y_column: str = "") -> Dict[str, Any]:
        try:
            # Parse data
            if isinstance(data, str):
                data_dict = json.loads(data)
                df = pd.DataFrame(data_dict)
            else:
                df = data
            
            # Create visualization
            if chart_type == "bar":
                fig = px.bar(df, x=x_column, y=y_column, title=title)
            elif chart_type == "line":
                fig = px.line(df, x=x_column, y=y_column, title=title)
            elif chart_type == "scatter":
                fig = px.scatter(df, x=x_column, y=y_column, title=title)
            elif chart_type == "pie":
                fig = px.pie(df, values=y_column, names=x_column, title=title)
            elif chart_type == "histogram":
                fig = px.histogram(df, x=x_column, title=title)
            else:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            # Convert to HTML
            html_content = fig.to_html(include_plotlyjs=True, full_html=True)
            
            return {
                "success": True,
                "chart_type": chart_type,
                "html_content": html_content,
                "data_shape": df.shape,
                "columns": list(df.columns)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "chart_type": chart_type
            }

class StatisticalAnalysisTool(BaseTool):
    """Tool for statistical analysis"""
    name = "statistical_analysis"
    description = "Perform statistical analysis on data"
    
    class InputSchema(BaseModel):
        data: str = Field(description="Data in JSON format or pandas DataFrame")
        analysis_type: str = Field(default="descriptive", description="Type of analysis: descriptive, correlation, or regression")
    
    def _run(self, data: str, analysis_type: str = "descriptive") -> Dict[str, Any]:
        try:
            # Parse data
            if isinstance(data, str):
                data_dict = json.loads(data)
                df = pd.DataFrame(data_dict)
            else:
                df = data
            
            results = {}
            
            if analysis_type == "descriptive":
                results = self._descriptive_statistics(df)
            elif analysis_type == "correlation":
                results = self._correlation_analysis(df)
            elif analysis_type == "regression":
                results = self._regression_analysis(df)
            else:
                raise ValueError(f"Unsupported analysis type: {analysis_type}")
            
            return {
                "success": True,
                "analysis_type": analysis_type,
                "results": results,
                "data_shape": df.shape
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis_type": analysis_type
            }
    
    def _descriptive_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate descriptive statistics"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        stats = {}
        for col in numeric_cols:
            stats[col] = {
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "count": int(df[col].count())
            }
        
        return stats
    
    def _correlation_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate correlations between numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            return {"error": "Need at least 2 numeric columns for correlation analysis"}
        
        correlation_matrix = numeric_df.corr()
        
        return {
            "correlation_matrix": correlation_matrix.to_dict(),
            "high_correlations": self._find_high_correlations(correlation_matrix)
        }
    
    def _find_high_correlations(self, corr_matrix: pd.DataFrame, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find high correlations above threshold"""
        high_corr = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    high_corr.append({
                        "variable1": corr_matrix.columns[i],
                        "variable2": corr_matrix.columns[j],
                        "correlation": float(corr_value)
                    })
        
        return high_corr
    
    def _regression_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Perform simple linear regression"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return {"error": "Need at least 2 numeric columns for regression analysis"}
        
        # Use first two numeric columns for regression
        x_col = numeric_cols[0]
        y_col = numeric_cols[1]
        
        # Remove rows with missing values
        clean_df = df[[x_col, y_col]].dropna()
        
        if len(clean_df) < 3:
            return {"error": "Insufficient data for regression analysis"}
        
        # Calculate regression coefficients
        x = clean_df[x_col]
        y = clean_df[y_col]
        
        n = len(x)
        sum_x = x.sum()
        sum_y = y.sum()
        sum_xy = (x * y).sum()
        sum_x2 = (x ** 2).sum()
        
        # Calculate slope and intercept
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Calculate R-squared
        y_pred = slope * x + intercept
        ss_res = ((y - y_pred) ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        r_squared = 1 - (ss_res / ss_tot)
        
        return {
            "independent_variable": x_col,
            "dependent_variable": y_col,
            "slope": float(slope),
            "intercept": float(intercept),
            "r_squared": float(r_squared),
            "equation": f"y = {slope:.4f}x + {intercept:.4f}"
        }

# Tool instances
text_analysis_tool = TextAnalysisTool()
data_visualization_tool = DataVisualizationTool()
statistical_analysis_tool = StatisticalAnalysisTool()

# Export all tools
__all__ = [
    "TextAnalysisTool",
    "DataVisualizationTool",
    "StatisticalAnalysisTool",
    "text_analysis_tool",
    "data_visualization_tool",
    "statistical_analysis_tool"
] 