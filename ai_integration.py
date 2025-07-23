# AI Integration Module for TabbyCat
# This module handles integration with various AI APIs

import openai
import requests
import json
import os
import matplotlib
matplotlib.use('Agg')   # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import textstat
import base64
from io import BytesIO

class AIIntegration:
    def __init__(self):
        # Initialize with API keys from environment variables.
        # On Render, these will be set in your Web Service's Environment Variables.
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.sarvam_api_key = os.getenv('SARVAM_API_KEY')

    def generate_speaker_feedback(self, speaker_data):
        """
        Generate AI-powered personalized feedback for speakers
        """
        if self.openai_api_key:
            return self._openai_speaker_analysis(speaker_data)
        elif self.sarvam_api_key:
            return self._sarvam_speaker_analysis(speaker_data)
        else:
            return self._fallback_analysis(speaker_data)

    def generate_motion_strategy(self, motion, side):
        """
        Generate debate strategies for specific motions and sides
        """
        prompt = f"""
        Generate a comprehensive debate strategy for the motion: "{motion}"
        Side: {side}

        Provide:
        1. Key arguments
        2. Potential rebuttals
        3. Stakeholder analysis
        4. Evidence suggestions
        """

        if self.openai_api_key:
            return self._call_openai(prompt)
        elif self.sarvam_api_key:
            return self._call_sarvam(prompt)
        else:
            return self._generate_fallback_strategy(motion, side)

    def analyze_judging_patterns(self, judge_data):
        """
        Analyze judge scoring patterns and provide insights
        """
        prompt = f"""
        Analyze the following judge scoring patterns and provide insights:
        {json.dumps(judge_data, indent=2)}

        Identify:
        1. Scoring tendencies
        2. Potential biases
        3. Consistency patterns
        4. Recommendations for speakers
        """

        if self.openai_api_key:
            return self._call_openai(prompt)
        else:
            return self._analyze_patterns_manually(judge_data)

    def _call_openai(self, prompt):
        """OpenAI API integration"""
        try:
            client = openai.OpenAI(api_key=self.openai_api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"

    def _call_sarvam(self, prompt):
        """Sarvam AI API integration"""
        try:
            if not self.sarvam_api_key:
                return "Sarvam AI API key not found. Please add SARVAM_API_KEY to your Render Environment Variables."

            headers = {
                'Authorization': f'Bearer {self.sarvam_api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'sarvam-2b-instruct',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 500,
                'temperature': 0.7
            }

            response = requests.post(
                'https://api.sarvam.ai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )

            print(f"Sarvam API Status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Sarvam API Error Response: {response.text}")
                return f"Sarvam AI unavailable (Status: {response.status_code}). Using fallback analysis."

        except requests.exceptions.Timeout:
            return "Sarvam AI request timeout. Using fallback analysis."
        except Exception as e:
            print(f"Sarvam AI Error: {str(e)}")
            return f"Sarvam AI Error: {str(e)}. Using fallback analysis."

    def _fallback_analysis(self, data):
        """Fallback analysis when no AI API is available"""
        # Note: You have multiple fallback functions.
        # This one is used by generate_speaker_feedback if both API keys are missing.
        return {
            "analysis": "Basic statistical analysis completed",
            "suggestion": "Consider integrating AI APIs for enhanced insights",
            "note": "Add your OpenAI or Sarvam AI key to Render Environment Variables for advanced features"
        }

    def generate_real_time_speaker_insights(self, speaker_name, recent_scores, motion_context=""):
        """Generate real-time AI insights for speakers with advanced analytics"""

        # Generate statistical analysis
        analytics = self._generate_speaker_analytics(speaker_name, recent_scores)

        prompt = f"""
        Analyze this debater's performance with detailed statistics:

        Speaker: {speaker_name}
        Recent Scores: {recent_scores}
        Motion Context: {motion_context}

        Analytics Summary:
        - Average Score: {analytics['avg_score']:.1f}
        - Score Trend: {analytics['trend']}
        - Consistency Rating: {analytics['consistency']}
        - Performance Percentile: {analytics['percentile']}
        - Improvement Rate: {analytics['improvement_rate']:.1f}%

        Provide:
        1. Data-driven performance analysis
        2. Specific improvement strategies based on score patterns
        3. Comparative insights (how they rank against typical debaters)
        4. Predictive recommendations for next round performance
        5. Confidence and motivation insights

        Format as structured, actionable advice with specific metrics.
        """

        if self.sarvam_api_key:
            ai_insights = self._call_sarvam(prompt)
        else:
            ai_insights = self._fallback_speaker_insights(speaker_name, recent_scores)

        # Combine AI insights with visual analytics
        return {
            "ai_analysis": ai_insights,
            "analytics": analytics,
            "visualizations": self._create_speaker_visualizations(recent_scores, speaker_name)
        }

    def generate_motion_strategy_realtime(self, motion, side, team_strengths=None):
        """Generate real-time motion strategies"""
        strengths_text = f"Team Strengths: {', '.join(team_strengths)}" if team_strengths else ""

        prompt = f"""
        Generate a winning debate strategy for:
        Motion: "{motion}"
        Side: {side}
        {strengths_text}

        Provide:
        1. 3 strongest arguments
        2. Potential opposition rebuttals and counters
        3. Key stakeholders to mention
        4. Timing and structure recommendations

        Format as clear, actionable points.
        """

        if self.sarvam_api_key:
            return self._call_sarvam(prompt)
        else:
            return self._fallback_strategy(motion, side)

    def analyze_judge_patterns_realtime(self, judge_history):
        """Real-time judge pattern analysis"""
        prompt = f"""
        Analyze this judge's scoring patterns:
        {json.dumps(judge_history, indent=2)}

        Identify:
        1. Scoring tendencies (high/low scorer)
        2. Argument preferences (style, content, delivery)
        3. What this judge rewards most
        4. Speaker adaptation recommendations

        Provide specific, actionable insights for debaters.
        """

        if self.sarvam_api_key:
            return self._call_sarvam(prompt)
        else:
            return self._fallback_judge_analysis(judge_history)

    def _fallback_speaker_insights(self, name, scores):
        trend = "improving" if len(scores) > 1 and scores[-1] > scores[0] else "stable"
        return f"{name}'s performance is {trend}. Current average: {sum(scores)/len(scores):.1f}. Focus on consistency and argument depth."

    def _fallback_strategy(self, motion, side):
        return f"For {side} on '{motion}': Focus on clear definitions, strong examples, and stakeholder impact analysis."

    def _fallback_judge_analysis(self, history):
        return "Judge analysis: Look for consistent scoring patterns. Adapt your style to match judge preferences for better results."

    def generate_team_insights_realtime(self, team_data):
        """Generate real-time AI insights for team performance"""
        prompt = f"""
        Analyze this debate team's performance and provide comprehensive insights:

        Team: {team_data.get('team_name', 'Unknown Team')}
        Members: {', '.join(team_data.get('members', []))}

        Round Performance:
        {json.dumps(team_data.get('rounds', []), indent=2)}

        Provide:
        1. Team synergy analysis
        2. Individual member growth patterns
        3. Strategic recommendations for improvement
        4. Coordination and teamwork insights
        4. Preparation tips for next rounds

        Format as actionable, specific advice.
        """

        if self.sarvam_api_key:
            return self._call_sarvam(prompt)
        else:
            return self._fallback_team_analysis(team_data)

    def analyze_judge_comprehensive(self, judge_data):
        """Comprehensive AI analysis of judge patterns"""
        prompt = f"""
        Analyze this judge's scoring patterns and behavioral tendencies:

        Judge: {judge_data.get('judge_name', 'Unknown Judge')}

        Scoring History:
        {json.dumps(judge_data.get('rounds', []), indent=2)}

        Overall Pattern: {judge_data.get('overall_judging_insight', '')}

        Provide detailed analysis:
        1. Scoring consistency and variance
        2. What arguments/styles this judge rewards
        3. Scoring evolution across rounds
        4. Speaker adaptation strategies
        5. Specific tips to score higher with this judge
        6. Judge's potential preferences and biases

        Format as practical advice for debaters.
        """

        if self.sarvam_api_key:
            return self._call_sarvam(prompt)
        else:
            return self._fallback_comprehensive_judge_analysis(judge_data)

    def _fallback_team_analysis(self, team_data):
        rounds = team_data.get('rounds', [])
        if not rounds:
            return "Team analysis: No performance data available."

        latest_avg = rounds[-1].get('average_score', 0)
        trend = "improving" if len(rounds) > 1 and rounds[-1].get('average_score', 0) > rounds[0].get('average_score', 0) else "stable"

        return f"""Team Analysis for {team_data.get('team_name', 'Team')}:

Performance trend: {trend}
Latest average: {latest_avg}
Focus on maintaining consistency and building on member strengths
Work on coordination between speakers for better synergy"""

    def _fallback_comprehensive_judge_analysis(self, judge_data):
        rounds = judge_data.get('rounds', [])
        if not rounds:
            return "Judge analysis: No scoring data available."

        all_scores = []
        for round_data in rounds:
            for speaker in round_data.get('speakers_scored', []):
                all_scores.append(speaker.get('score', 0))

        if all_scores:
            avg_score = sum(all_scores) / len(all_scores)
            return f"""Comprehensive Judge Analysis:

Average scoring: {avg_score:.1f}
Consistency: {'High' if max(all_scores) - min(all_scores) < 10 else 'Moderate'}
Scoring trend: Look for patterns in argument preferences
Adaptation tip: Focus on clear structure and evidence-based arguments"""

        return "Judge analysis: Insufficient data for comprehensive analysis."

    def _generate_speaker_analytics(self, speaker_name, scores):
        """Generate comprehensive speaker analytics"""
        if not scores or len(scores) == 0:
            return {"error": "No scores available"}

        scores_array = np.array(scores)

        # Calculate trends
        if len(scores) > 1:
            slope = np.polyfit(range(len(scores)), scores, 1)[0]
            trend = "improving" if slope > 0.5 else "declining" if slope < -0.5 else "stable"
            improvement_rate = ((scores[-1] - scores[0]) / scores[0]) * 100 if scores[0] != 0 else 0
        else:
            trend = "insufficient_data"
            improvement_rate = 0

        # Statistical measures
        avg_score = np.mean(scores_array)
        std_dev = np.std(scores_array)
        consistency = "high" if std_dev < 3 else "moderate" if std_dev < 6 else "low"

        # Percentile estimation (assuming normal distribution around 75-80)
        percentile = min(95, max(5, ((avg_score - 70) / 20) * 100))

        return {
            "avg_score": avg_score,
            "std_dev": std_dev,
            "trend": trend,
            "consistency": consistency,
            "percentile": percentile,
            "improvement_rate": improvement_rate,
            "score_range": f"{min(scores)}-{max(scores)}",
            "total_rounds": len(scores)
        }

    def _create_speaker_visualizations(self, scores, speaker_name):
        """Create visualizations for speaker performance"""
        try:
            if not scores or len(scores) == 0:
                return {"error": "No scores available for visualization"}

            # Performance trend chart using matplotlib (more reliable)
            rounds = list(range(1, len(scores) + 1))

            fig, ax = plt.subplots(1, 1, figsize=(8, 5))
            ax.plot(rounds, scores, marker='o', color='#e74c3c', linewidth=2, markersize=6)
            ax.set_title(f"{speaker_name}'s Performance Trend", fontsize=14, fontweight='bold')
            ax.set_xlabel("Round")
            ax.set_ylabel("Score")
            ax.grid(True, alpha=0.3)
            ax.set_ylim(min(scores) - 2, max(scores) + 2)

            # Add score labels on points
            for i, score in enumerate(scores):
                ax.annotate(f'{score}', (rounds[i], score), textcoords="offset points",
                               xytext=(0,10), ha='center', fontsize=9)

            plt.tight_layout()

            # Convert to base64 for embedding
            img_buffer = BytesIO()
            plt.savefig(img_buffer, format='png', dpi=120, bbox_inches='tight', facecolor='white')
            img_buffer.seek(0)
            chart_b64 = base64.b64encode(img_buffer.getvalue()).decode()
            plt.close('all')

            return {
                "trend_chart": chart_b64,
                "chart_type": "performance_trend"
            }
        except Exception as e:
            print(f"Visualization error: {str(e)}")
            return {"error": f"Visualization generation failed: {str(e)}"}

    def generate_performance_report(self, speaker_data_list):
        """Generate comprehensive performance report with multiple visualizations"""
        try:
            if not speaker_data_list or len(speaker_data_list) == 0:
                return self._generate_fallback_report("No data available")

            # Create DataFrame
            df = pd.DataFrame(speaker_data_list)

            # Ensure required columns exist
            required_columns = ['score', 'round', 'team', 'name']
            for col in required_columns:
                if col not in df.columns:
                    return self._generate_fallback_report(f"Missing required column: {col}")

            # Create figure with proper size
            fig, axes = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle('TabbyCat Performance Analytics Report', fontsize=16, fontweight='bold')

            # Score distribution
            axes[0, 0].hist(df['score'], bins=10, color='#e74c3c', alpha=0.7, edgecolor='black')
            axes[0, 0].set_title('Score Distribution')
            axes[0, 0].set_xlabel('Score')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].grid(True, alpha=0.3)

            # Round-wise performance
            if 'round' in df.columns:
                round_avg = df.groupby('round')['score'].mean()
                axes[0, 1].plot(range(len(round_avg)), round_avg.values, marker='o', color='#e74c3c', linewidth=2, markersize=6)
                axes[0, 1].set_title('Average Score by Round')
                axes[0, 1].set_xlabel('Round')
                axes[0, 1].set_ylabel('Average Score')
                axes[0, 1].set_xticks(range(len(round_avg)))
                axes[0, 1].set_xticklabels(round_avg.index, rotation=45)
                axes[0, 1].grid(True, alpha=0.3)

            # Team performance comparison
            if 'team' in df.columns:
                team_avg = df.groupby('team')['score'].mean().sort_values(ascending=True)
                axes[1, 0].barh(range(len(team_avg)), team_avg.values, color='#e74c3c', alpha=0.7)
                axes[1, 0].set_title('Team Performance')
                axes[1, 0].set_xlabel('Average Score')
                axes[1, 0].set_yticks(range(len(team_avg)))
                axes[1, 0].set_yticklabels(team_avg.index)
                axes[1, 0].grid(True, alpha=0.3)

            # Speaker performance summary
            if 'name' in df.columns:
                speaker_avg = df.groupby('name')['score'].mean().sort_values(ascending=True)
                colors = ['#27ae60' if x > df['score'].mean() else '#e74c3c' for x in speaker_avg.values]
                axes[1, 1].barh(range(len(speaker_avg)), speaker_avg.values, color=colors, alpha=0.7)
                axes[1, 1].set_title('Speaker Performance')
                axes[1, 1].set_xlabel('Average Score')
                axes[1, 1].set_yticks(range(len(speaker_avg)))
                axes[1, 1].set_yticklabels(speaker_avg.index)
                axes[1, 1].grid(True, alpha=0.3)

            plt.tight_layout()

            # Save to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', facecolor='white')
            buffer.seek(0)
            report_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close('all') # Close all figures to free memory

            return report_b64

        except Exception as e:
            print(f"Performance report error: {str(e)}")
            return self._generate_fallback_report(str(e))

    def _generate_fallback_report(self, error_msg):
        """Generate a simple fallback report when main generation fails"""
        try:
            fig, ax = plt.subplots(1, 1, figsize=(8, 6))
            ax.text(0.5, 0.5, f'Performance Report\n\nError: {error_msg}\n\nPlease check your data and try again.',
                            horizontalalignment='center', verticalalignment='center', fontsize=12,
                            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')

            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', facecolor='white')
            buffer.seek(0)
            report_b64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close('all')

            return report_b64
        except Exception as fallback_error:
            print(f"Fallback report error: {str(fallback_error)}")
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    def _analyze_patterns_manually(self, judge_data):
        """Fallback analysis when no AI API is available"""
        return {
            "analysis": "Basic statistical analysis completed",
            "suggestion": "Consider integrating AI APIs for enhanced insights",
            "note": "Add your OpenAI or Sarvam AI key to Render Environment Variables for advanced features"
        }

# Example usage functions
def enhance_with_ai():
    """
    Example of how to enhance existing data with AI insights
    """
    ai = AIIntegration()

    # Example speaker analysis
    speaker_data = {
        "name": "Manan Chaudhary",
        "scores": [78, 81, 84],
        "feedback_history": ["Good structure", "Better engagement", "Excellent delivery"]
    }

    ai_feedback = ai.generate_speaker_feedback(speaker_data)

    # Example motion strategy
    motion_strategy = ai.generate_motion_strategy("This House Would Ban Zoos", "Government")

    return {
        "ai_feedback": ai_feedback,
        "motion_strategy": motion_strategy
    }
