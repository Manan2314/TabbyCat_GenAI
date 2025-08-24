import os
import json
import re
import google.generativeai as genai

class AIIntegration:
    def __init__(self):
        # Retrieve API key from environment variables
        self.gemini_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        # Configure the Gemini API client
        genai.configure(api_key=self.gemini_api_key)
        self.client = genai.GenerativeModel("gemini-1.5-pro")  # ✅ FIXED MODEL NAME

    def _call_gemini_ai(self, prompt_text, max_tokens=150, temperature=0.7):
        """Helper to call Gemini AI with a prompt string."""
        try:
            response = self.client.generate_content(
                prompt_text,
                generation_config=genai.GenerationConfig(  # ✅ FIXED config
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            return response
        except Exception as e:
            print(f"An error occurred with the Gemini API: {e}")
            return {"error": str(e)}

    def _extract_content(self, response):
        """Extracts content from Gemini response, handling errors."""
        if isinstance(response, dict) and response.get("error"):
            return f"AI Error: {response['error']}"
        try:
            # ✅ Safer extraction (handles different SDK return structures)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "candidates") and response.candidates:
                parts = response.candidates[0].content.parts
                if parts and hasattr(parts[0], "text"):
                    return parts[0].text.strip()
            return "No valid text returned from AI."
        except Exception as e:
            return f"Failed to extract content: {e}"

    def _parse_ai_feedback_output(self, ai_response_string):
        """Parses the AI's string output into a dictionary."""
        general_feedback_match = re.search(r'general_feedback: "(.*?)"', ai_response_string, re.DOTALL)
        improvement_advice_match = re.search(r'improvement_advice: "(.*?)"', ai_response_string, re.DOTALL)

        return {
            "general_feedback": general_feedback_match.group(1).strip() if general_feedback_match else "No general feedback generated.",
            "improvement_advice": improvement_advice_match.group(1).strip() if improvement_advice_match else "No improvement advice generated."
        }

    def generate_speaker_feedback(self, speaker_data):
        """Generates concise, refined speaker feedback based on judge comments."""
        name = speaker_data.get('name', 'N/A')
        role = speaker_data.get('role', 'N/A')
        score = speaker_data.get('score', 'N/A')

        existing_general_feedback = speaker_data.get('feedback', {}).get('general_feedback', '')
        existing_improvement_advice = speaker_data.get('feedback', {}).get('improvement_advice', '')

        combined_judge_comment = f"General: {existing_general_feedback}. Improvement: {existing_improvement_advice}."

        prompt_text = f"""You are an AI assistant helping students improve at debating by refining judge feedback.
You will be given a speaker's name, role, and the raw comment from the adjudicator.
Rewrite the feedback in a short, crisp, and logical way:

- Summarize what went well
- Give clear improvement advice
- Keep the tone constructive and student-friendly

Format your output like this:
general_feedback: "..."
improvement_advice: "..."

Input:
{{
"name": "{name}",
"role": "{role}",
"score": {score},
"judge_comment": "{combined_judge_comment}"
}}
"""
        response_obj = self._call_gemini_ai(prompt_text, max_tokens=150, temperature=0.5)
        ai_raw_content = self._extract_content(response_obj)
        return self._parse_ai_feedback_output(ai_raw_content)

    def generate_team_insights_realtime(self, team_data):
        """Analyzes team performance data."""
        team_name = team_data.get('team_name', 'N/A')
        members = ", ".join(team_data.get('members', []))
        rounds_summary = []
        for r in team_data.get('rounds', []):
            rounds_summary.append(
                f"Round {r.get('round')}: Average Score {r.get('average_score')}, Feedback: {r.get('team_feedback', 'N/A')}"
            )

        prompt_text = f"""Analyze the performance of team {team_name} with members {members}.
Summary of rounds: {'; '.join(rounds_summary)}.
Provide a concise overall assessment of their strengths, weaknesses, and one key area for improvement. Keep it to 3-4 sentences."""

        response_obj = self._call_gemini_ai(prompt_text, max_tokens=150, temperature=0.6)
        return self._extract_content(response_obj)

    def analyze_judge_comprehensive(self, judge_data):
        """Analyzes a judge's patterns and provides insights."""
        judge_name = judge_data.get('judge_name', 'N/A')
        judge_style = judge_data.get('judge_style', 'N/A')
        overall_insight = judge_data.get('overall_judging_insight', 'N/A')

        rounds_scored_summary = []
        for r in judge_data.get('rounds', []):
            speakers_scores = ", ".join([f"{s.get('name')}: {s.get('score')}" for s in r.get('speakers_scored', [])])
            rounds_scored_summary.append(f"Round {r.get('round')}: Speakers scored: {speakers_scores}.")

        prompt_text = f"""Analyze the judging patterns of {judge_name}.
Judge Style: {judge_style}.
Overall Insight: {overall_insight}.
Rounds Scored Summary: {'; '.join(rounds_scored_summary)}.

Provide a concise 2-3 sentence summary of their judging tendencies, including any biases or notable patterns. Focus on constructive observations for teams debating in front of this judge."""

        response_obj = self._call_gemini_ai(prompt_text, max_tokens=120, temperature=0.6)
        return self._extract_content(response_obj)
