import os
import google.generativeai as genai

class AIIntegration:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ Missing GEMINI_API_KEY in environment variables")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    # ---------------- Speaker Feedback ----------------
    def generate_speaker_feedback(self, speaker_data):
        prompt = f"""
        Analyze the following debate speaker data and provide clear, constructive feedback:

        Speaker Info:
        {speaker_data}

        Provide:
        1. Key strengths
        2. Areas for improvement
        3. Suggestions for better debating
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text if response and response.text else "⚠️ No AI feedback available."
        except Exception as e:
            return f"⚠️ Error generating speaker feedback: {str(e)}"

    # ---------------- Team Insights ----------------
    def generate_team_insights_realtime(self, team_data):
        prompt = f"""
        You are an AI debate analyst. Given the following team performance data:

        {team_data}

        Generate:
        1. Overall team strengths
        2. Weaknesses in their approach
        3. Recommended strategies for future debates
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text if response and response.text else "⚠️ No AI insights available."
        except Exception as e:
            return f"⚠️ Error generating team insights: {str(e)}"

    # ---------------- Judge Insights ----------------
    def analyze_judge_comprehensive(self, judge_data):
        prompt = f"""
        Analyze the judge's feedback and decisions:

        {judge_data}

        Provide:
        1. Judge's evaluation style
        2. Key decision-making criteria
        3. Advice for debaters when facing this judge
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text if response and response.text else "⚠️ No AI analysis available."
        except Exception as e:
            return f"⚠️ Error generating judge analysis: {str(e)}"
