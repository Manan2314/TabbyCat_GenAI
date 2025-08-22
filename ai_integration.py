# TabbyCat GenAI - Gemini AI Integration
# Replace Sarvam AI with Google Gemini AI

import google.generativeai as genai
import os
import json
import pandas as pd
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiAIService:
    """
    Service class for Google Gemini AI integration
    Replaces the previous Sarvam AI implementation
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini AI service
        
        Args:
            api_key (str): Google AI API key. If None, tries to get from environment
        """
        self.api_key = api_key or os.getenv('GOOGLE_AI_API_KEY')
        if not self.api_key:
            raise ValueError("Google AI API key is required. Set GOOGLE_AI_API_KEY environment variable or pass api_key parameter.")
        
        # Configure Gemini AI
        genai.configure(api_key=self.api_key)
        
        # Initialize the model (using Gemini Pro)
        self.model = genai.GenerativeModel('gemini-pro')
        
        logger.info("Gemini AI service initialized successfully")
    
    def analyze_speaker_performance(self, speaker_data: Dict) -> Dict:
        """
        Analyze speaker performance using Gemini AI
        
        Args:
            speaker_data (Dict): Speaker performance data including scores, speeches, etc.
            
        Returns:
            Dict: Analysis results with insights and recommendations
        """
        try:
            # Prepare the prompt for speaker analysis
            prompt = f"""
            Analyze the following speaker performance data for a debate tournament:
            
            Speaker Name: {speaker_data.get('name', 'Unknown')}
            Average Score: {speaker_data.get('avg_score', 0)}
            Speeches Given: {speaker_data.get('speech_count', 0)}
            Scores: {speaker_data.get('scores', [])}
            Speech Texts (sample): {speaker_data.get('speech_samples', [])}
            
            Please provide:
            1. Performance Trends Analysis
            2. Strengths and Weaknesses
            3. Consistency Rating (1-10)
            4. Percentile Ranking Analysis
            5. Specific Improvement Recommendations
            6. Speaking Style Assessment
            
            Format the response as a structured analysis with clear sections.
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse and structure the response
            analysis = {
                'speaker_name': speaker_data.get('name', 'Unknown'),
                'ai_analysis': response.text,
                'performance_score': speaker_data.get('avg_score', 0),
                'trends': self._extract_trends(response.text),
                'recommendations': self._extract_recommendations(response.text),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in speaker performance analysis: {str(e)}")
            return {'error': str(e)}
    
    def generate_team_strategy(self, team_data: Dict, motion: str) -> Dict:
        """
        Generate team strategy using Gemini AI
        
        Args:
            team_data (Dict): Team performance data
            motion (str): Debate motion
            
        Returns:
            Dict: Strategy recommendations and analysis
        """
        try:
            prompt = f"""
            Generate a comprehensive team strategy for the following debate scenario:
            
            Motion: {motion}
            Team Information:
            - Team Name: {team_data.get('name', 'Unknown')}
            - Average Team Score: {team_data.get('avg_score', 0)}
            - Previous Performance: {team_data.get('performance_history', [])}
            - Speaker Strengths: {team_data.get('speaker_strengths', {})}
            - Side: {team_data.get('side', 'Unknown')}
            
            Please provide:
            1. Core Arguments Strategy
            2. Speaker Role Assignments
            3. Coordination Recommendations
            4. Potential Counter-Arguments to Prepare For
            5. Tactical Approach
            6. Time Management Strategy
            7. Specific Preparation Points
            
            Make the strategy actionable and specific to this motion and team composition.
            """
            
            response = self.model.generate_content(prompt)
            
            strategy = {
                'team_name': team_data.get('name', 'Unknown'),
                'motion': motion,
                'strategy_analysis': response.text,
                'key_points': self._extract_key_points(response.text),
                'coordination_insights': self._extract_coordination_insights(response.text),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            return strategy
            
        except Exception as e:
            logger.error(f"Error in team strategy generation: {str(e)}")
            return {'error': str(e)}
    
    def analyze_judge_patterns(self, judge_data: Dict) -> Dict:
        """
        Analyze judge scoring patterns using Gemini AI
        
        Args:
            judge_data (Dict): Judge scoring history and patterns
            
        Returns:
            Dict: Judge pattern analysis and adaptation strategies
        """
        try:
            prompt = f"""
            Analyze the following judge's scoring patterns and preferences:
            
            Judge Name: {judge_data.get('name', 'Unknown')}
            Rounds Judged: {judge_data.get('rounds_judged', 0)}
            Average Scores Given: {judge_data.get('avg_scores', {})}
            Scoring History: {judge_data.get('scoring_history', [])}
            Motion Types Judged: {judge_data.get('motion_types', [])}
            Feedback Patterns: {judge_data.get('feedback_patterns', [])}
            
            Please provide:
            1. Scoring Pattern Analysis
            2. Preferred Argument Types
            3. Speaking Style Preferences
            4. Consistency in Scoring
            5. Adaptation Strategies for Teams
            6. Key Factors This Judge Values
            7. Common Feedback Themes
            
            Focus on actionable insights that teams can use to adapt their approach.
            """
            
            response = self.model.generate_content(prompt)
            
            analysis = {
                'judge_name': judge_data.get('name', 'Unknown'),
                'pattern_analysis': response.text,
                'adaptation_strategies': self._extract_adaptation_strategies(response.text),
                'scoring_insights': self._extract_scoring_insights(response.text),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in judge pattern analysis: {str(e)}")
            return {'error': str(e)}
    
    def generate_motion_strategy(self, motion: str, side: str, context: Dict = None) -> Dict:
        """
        Generate motion-specific strategy using Gemini AI
        
        Args:
            motion (str): The debate motion
            side (str): Side of the debate (Gov/Prop or Opp)
            context (Dict): Additional context about the tournament, format, etc.
            
        Returns:
            Dict: Motion strategy and analysis
        """
        try:
            context_info = context or {}
            
            prompt = f"""
            Generate a comprehensive debate strategy for the following motion:
            
            Motion: {motion}
            Side: {side}
            Tournament Context: {context_info.get('tournament_type', 'Standard BP')}
            Round Type: {context_info.get('round_type', 'Regular')}
            Additional Context: {context_info.get('additional_info', 'None')}
            
            Please provide:
            1. Motion Analysis and Key Issues
            2. Core Arguments for {side} side
            3. Potential Opposition Arguments
            4. Evidence and Examples to Use
            5. Framing Strategy
            6. Rebuttal Preparation
            7. Extension Opportunities (if applicable)
            8. Common Pitfalls to Avoid
            
            Make the strategy specific to this motion and provide concrete argument lines.
            """
            
            response = self.model.generate_content(prompt)
            
            strategy = {
                'motion': motion,
                'side': side,
                'strategy_analysis': response.text,
                'core_arguments': self._extract_core_arguments(response.text),
                'counter_strategies': self._extract_counter_strategies(response.text),
                'timestamp': pd.Timestamp.now().isoformat()
            }
            
            return strategy
            
        except Exception as e:
            logger.error(f"Error in motion strategy generation: {str(e)}")
            return {'error': str(e)}
    
    def generate_feedback(self, performance_data: Dict, feedback_type: str = "general") -> Dict:
        """
        Generate AI-powered feedback for performance improvement
        
        Args:
            performance_data (Dict): Performance data to analyze
            feedback_type (str): Type of feedback (speaker, team, judge)
            
        Returns:
            Dict: Generated feedback and recommendations
        """
        try:
            if feedback_type == "speaker":
                return self.analyze_speaker_performance(performance_data)
            elif feedback_type == "team":
                motion = performance_data.get('motion', 'General Strategy')
                return self.generate_team_strategy(performance_data, motion)
            elif feedback_type == "judge":
                return self.analyze_judge_patterns(performance_data)
            else:
                # General feedback
                prompt = f"""
                Provide general debate performance feedback based on the following data:
                {json.dumps(performance_data, indent=2)}
                
                Focus on actionable improvements and insights.
                """
                
                response = self.model.generate_content(prompt)
                
                return {
                    'feedback_type': feedback_type,
                    'analysis': response.text,
                    'timestamp': pd.Timestamp.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error in feedback generation: {str(e)}")
            return {'error': str(e)}
    
    # Helper methods for extracting specific information from AI responses
    
    def _extract_trends(self, text: str) -> List[str]:
        """Extract performance trends from AI response"""
        # Simple extraction logic - can be enhanced with NLP
        trends = []
        lines = text.split('\n')
        for line in lines:
            if 'trend' in line.lower() or 'pattern' in line.lower():
                trends.append(line.strip())
        return trends
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from AI response"""
        recommendations = []
        lines = text.split('\n')
        for line in lines:
            if 'recommend' in line.lower() or 'suggest' in line.lower() or 'improve' in line.lower():
                recommendations.append(line.strip())
        return recommendations
    
    def _extract_key_points(self, text: str) -> List[str]:
        """Extract key strategic points from AI response"""
        key_points = []
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')):
                key_points.append(line.strip())
        return key_points
    
    def _extract_coordination_insights(self, text: str) -> List[str]:
        """Extract coordination insights from AI response"""
        insights = []
        lines = text.split('\n')
        for line in lines:
            if 'coordinat' in line.lower() or 'teamwork' in line.lower() or 'collabor' in line.lower():
                insights.append(line.strip())
        return insights
    
    def _extract_adaptation_strategies(self, text: str) -> List[str]:
        """Extract adaptation strategies from AI response"""
        strategies = []
        lines = text.split('\n')
        for line in lines:
            if 'adapt' in line.lower() or 'adjust' in line.lower() or 'strategy' in line.lower():
                strategies.append(line.strip())
        return strategies
    
    def _extract_scoring_insights(self, text: str) -> List[str]:
        """Extract scoring insights from AI response"""
        insights = []
        lines = text.split('\n')
        for line in lines:
            if 'scor' in line.lower() or 'point' in line.lower() or 'mark' in line.lower():
                insights.append(line.strip())
        return insights
    
    def _extract_core_arguments(self, text: str) -> List[str]:
        """Extract core arguments from AI response"""
        arguments = []
        lines = text.split('\n')
        for line in lines:
            if 'argument' in line.lower() or 'case' in line.lower() or 'claim' in line.lower():
                arguments.append(line.strip())
        return arguments
    
    def _extract_counter_strategies(self, text: str) -> List[str]:
        """Extract counter strategies from AI response"""
        strategies = []
        lines = text.split('\n')
        for line in lines:
            if 'counter' in line.lower() or 'opposition' in line.lower() or 'rebutt' in line.lower():
                strategies.append(line.strip())
        return strategies


# Flask integration example
class TabbyCatGeminiIntegration:
    """
    Main integration class for TabbyCat with Gemini AI
    """
    
    def __init__(self, api_key: str = None):
        self.ai_service = GeminiAIService(api_key)
    
    def get_speaker_analysis(self, speaker_id: int, tournament_data: Dict) -> Dict:
        """Get AI-powered speaker analysis"""
        # Extract speaker data from tournament data
        speaker_data = self._prepare_speaker_data(speaker_id, tournament_data)
        return self.ai_service.analyze_speaker_performance(speaker_data)
    
    def get_team_strategy(self, team_id: int, motion: str, tournament_data: Dict) -> Dict:
        """Get AI-powered team strategy"""
        team_data = self._prepare_team_data(team_id, tournament_data)
        return self.ai_service.generate_team_strategy(team_data, motion)
    
    def get_judge_analysis(self, judge_id: int, tournament_data: Dict) -> Dict:
        """Get AI-powered judge pattern analysis"""
        judge_data = self._prepare_judge_data(judge_id, tournament_data)
        return self.ai_service.analyze_judge_patterns(judge_data)
    
    def get_motion_strategy(self, motion: str, side: str, context: Dict = None) -> Dict:
        """Get AI-powered motion strategy"""
        return self.ai_service.generate_motion_strategy(motion, side, context)
    
    def _prepare_speaker_data(self, speaker_id: int, tournament_data: Dict) -> Dict:
        """Prepare speaker data for AI analysis"""
        # This would extract relevant speaker data from your tournament database
        # Placeholder implementation
        return {
            'name': f'Speaker_{speaker_id}',
            'avg_score': 75.5,
            'speech_count': 6,
            'scores': [74, 76, 75, 77, 73, 78],
            'speech_samples': ['Sample speech text...']
        }
    
    def _prepare_team_data(self, team_id: int, tournament_data: Dict) -> Dict:
        """Prepare team data for AI analysis"""
        # This would extract relevant team data from your tournament database
        # Placeholder implementation
        return {
            'name': f'Team_{team_id}',
            'avg_score': 150.5,
            'performance_history': [148, 152, 149, 153],
            'speaker_strengths': {'speaker1': 'Logic', 'speaker2': 'Delivery'}
        }
    
    def _prepare_judge_data(self, judge_id: int, tournament_data: Dict) -> Dict:
        """Prepare judge data for AI analysis"""
        # This would extract relevant judge data from your tournament database
        # Placeholder implementation
        return {
            'name': f'Judge_{judge_id}',
            'rounds_judged': 12,
            'avg_scores': {'gov': 75.2, 'opp': 74.8},
            'scoring_history': [74, 76, 73, 77, 75],
            'motion_types': ['Policy', 'Value', 'Fact'],
            'feedback_patterns': ['Focus on logic', 'Values clear structure']
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize with your Google AI API key
    # Make sure to set GOOGLE_AI_API_KEY environment variable
    
    try:
        # Initialize the integration
        tabbycat_ai = TabbyCatGeminiIntegration()
        
        # Test speaker analysis
        print("Testing Speaker Analysis...")
        speaker_analysis = tabbycat_ai.get_speaker_analysis(1, {})
        print("Speaker Analysis:", speaker_analysis)
        
        # Test team strategy
        print("\nTesting Team Strategy...")
        team_strategy = tabbycat_ai.get_team_strategy(
            1, 
            "This house believes that social media companies should be held liable for mental health issues caused by their platforms",
            {}
        )
        print("Team Strategy:", team_strategy)
        
        # Test judge analysis
        print("\nTesting Judge Analysis...")
        judge_analysis = tabbycat_ai.get_judge_analysis(1, {})
        print("Judge Analysis:", judge_analysis)
        
        # Test motion strategy
        print("\nTesting Motion Strategy...")
        motion_strategy = tabbycat_ai.get_motion_strategy(
            "This house believes that artificial intelligence will ultimately benefit humanity",
            "Government",
            {"tournament_type": "BP", "round_type": "Final"}
        )
        print("Motion Strategy:", motion_strategy)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set your GOOGLE_AI_API_KEY environment variable")
