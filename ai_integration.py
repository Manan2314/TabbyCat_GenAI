import os
import re
import google.generativeai as genai


class AIIntegration:
    def __init__(self):
        # Get Gemini API key from environment variables
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        # Configure Gemini
        genai.configure(api_key=self.gemini_api_key)

        # Use Gemini-Pro model
        self.model = genai.GenerativeModel("gemini-pro")

    def _call_gemini(self, prompt, max_output_tokens=300, temperature=0.6):
        """Helper to call Gemini with a simple text prompt."""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_output_tokens,
                    "temperature": temperature,
                },
            )
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return f"AI Error: {e}"

    def _parse_ai_feedback_output(self, ai_response_string):
        """Parses the AI's string output into a dictionary with 2 fields."""
        general_feedback_match = re.search(
            r'general_feedback:\s*"(.*?)"', ai_response_string, re.DOTALL
        )
        improvement_advice_match = re.search(
            r'improvement_advice:\s*"(.*?)"', ai_response_string, re.DOTALL
        )

        return {
            "general_feedback": general_feedback_match.group(1).strip()
            if general_feedback_match
            else "No general feedback generated.",
            "improvement_advice": improvement_advice_match.group(1).strip()
            if improvement_advice_match
            else "No improvement advice generated.",
        }

    def generate_speaker_feedback(self, speaker_data):
        """Generate concise, refined speaker feedback."""
        name = speaker_data.get("name", "N/A")
        role = speaker_data.get("role", "N/A")
        score = speaker_data.get("score", "N/A")

        existing_general_feedback = speaker_data.get("feedback", {}).get(
            "general_feedback", ""
        )
        existing_improvement_advice = speaker_data.get("feedback", {}).get(
            "improvement_advice", ""
        )

        combined_judge_comment = (
            f"General: {existing_general_feedback}. "
            f"Improvement: {existing_improvement_advice}."
        )

        prompt = f"""
You are an AI assistant helping students improve at debating by refining judge feedback.
You will be given a speaker's name, role, and raw adjudicator comments.
Rewrite the feedback in a short, crisp, and logical way:

- Summarize what went well
- Give clear improvement advice
- Keep the tone constructive and helpful

Format your output exactly like this:
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
        ai_response = self._call_gemini(prompt, max_output_tokens=150, temperature=0.5)
        return self._parse_ai_feedback_output(ai_response)

    def generate_team_insights_realtime(self, team_data):
        """Analyze team performance data."""
        team_name = team_data.get("team_name", "N/A")
        members = ", ".join(team_data.get("members", []))
        rounds_summary = [
            f"Round {r.get('round')}: Avg Score {r.get('average_score')}, Feedback: {r.get('team_feedback', 'N/A')}"
            for r in team_data.get("rounds", [])
        ]

        prompt = f"""
Analyze the performance of team {team_name} with members {members}.
Summary of rounds: {'; '.join(rounds_summary)}.
Provide a concise overall assessment of their strengths, weaknesses,
and a key area for improvement. Keep it to 3-4 sentences.
"""
        return self._call_gemini(prompt, max_output_tokens=150, temperature=0.6)

    def analyze_judge_comprehensive(self, judge_data):
        """Analyze judge’s patterns and tendencies."""
        judge_name = judge_data.get("judge_name", "N/A")
        judge_style = judge_data.get("judge_style", "N/A")
        overall_insight = judge_data.get("overall_judging_insight", "N/A")

        rounds_summary = [
            f"Round {r.get('round')}: " +
            ", ".join([f"{s.get('name')}: {s.get('score')}" for s in r.get("speakers_scored", [])])
            for r in judge_data.get("rounds", [])
        ]

        prompt = f"""
Analyze the judging patterns of {judge_name}.
Judge Style: {judge_style}.
Overall Insight: {overall_insight}.
Rounds Summary: {'; '.join(rounds_summary)}.

Provide a concise, 2-3 sentence summary of their judging tendencies,
including biases or notable patterns. Keep it constructive.
"""
        return self._call_gemini(prompt, max_output_tokens=120, temperature=0.6)
