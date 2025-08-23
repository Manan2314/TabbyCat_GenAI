import os
import json
import requests
import re # Import the regular expression module

class AIIntegration:
    def __init__(self):
        # Retrieve API key from environment variables
        self.sarvam_api_key = os.getenv("SARVAM_API_KEY")
        if not self.sarvam_api_key:
            raise ValueError("SARVAM_API_KEY environment variable not set.")

        self.sarvam_api_url = "https://sarvam-ai-api.azurewebsites.net/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.sarvam_api_key}",
            "Content-Type": "application/json",
        }

    def _call_sarvam_ai(self, prompt_messages, max_tokens=150, temperature=0.7):
        """Helper to call Sarvam AI with structured messages."""
        data = {
            "messages": prompt_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        try:
            response = requests.post(self.sarvam_api_url, headers=self.headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - {response.text}")
            return {"error": f"HTTP error: {http_err}", "details": response.text}
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            return {"error": f"Connection error: {conn_err}"}
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            return {"error": f"Timeout error: {timeout_err}"}
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
            return {"error": f"Request error: {req_err}"}
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err} - Response: {response.text}")
            return {"error": f"JSON decode error: {json_err}", "details": response.text}

    def _extract_content(self, response):
        """Extracts content from AI response, handling errors."""
        if isinstance(response, dict) and response.get("error"):
            return f"AI Error: {response['error']}. Details: {response.get('details', 'N/A')}"
        try:
            return response.get("choices", [])[0].get("message", {}).get("content", "No content generated.")
        except (IndexError, AttributeError):
            return "Failed to extract content from AI response."

    # 🔹 NEW HELPER FUNCTION TO PARSE AI'S CONCISE FEEDBACK 🔹
    def _parse_ai_feedback_output(self, ai_response_string):
        """Parses the AI's string output into a dictionary."""
        general_feedback_match = re.search(r'general_feedback: "(.*?)"', ai_response_string, re.DOTALL)
        improvement_advice_match = re.search(r'improvement_advice: "(.*?)"', ai_response_string, re.DOTALL)

        return {
            "general_feedback": general_feedback_match.group(1).strip() if general_feedback_match else "No general feedback generated.",
            "improvement_advice": improvement_advice_match.group(1).strip() if improvement_advice_match else "No improvement advice generated."
        }

    def generate_speaker_feedback(self, speaker_data):
        """
        Generates concise, refined speaker feedback based on judge comments.
        The AI refines existing feedback, not a raw judge_comment from outside.
        """
        name = speaker_data.get('name', 'N/A')
        role = speaker_data.get('role', 'N/A')
        score = speaker_data.get('score', 'N/A')

        # Combine existing general feedback and improvement advice for the AI to refine
        existing_general_feedback = speaker_data.get('feedback', {}).get('general_feedback', '')
        existing_improvement_advice = speaker_data.get('feedback', {}).get('improvement_advice', '')

        # Construct the judge_comment by combining existing feedback
        # This is what the AI will 'rewrite'
        combined_judge_comment = f"General: {existing_general_feedback}. Improvement: {existing_improvement_advice}."

        # 🔹 YOUR NEW PROMPT IS HERE 🔹
        prompt_text = f"""You are an AI assistant helping students improve at debating by refining judge feedback.
You will be given a speaker's name, role, and the raw comment from the adjudicator.
Your job is to rewrite the judge's verdict in a short, crisp, and logical way that:

- Summarizes what went well
- Gives clear improvement advice
- Keeps the tone constructive and helpful

Format your output like this:
general_feedback: "..."
improvement_advice: "..."

Make sure both lines are concise (1-2 sentences max). Do not repeat points across sections. Keep the language simple and student-friendly.

Input:
{{
"name": "{name}",
"role": "{role}",
"score": {score},
"judge_comment": "{combined_judge_comment}"
}}
"""
        messages = [{"role": "user", "content": prompt_text}]

        response_json = self._call_sarvam_ai(messages, max_tokens=150, temperature=0.5) # Adjusted max_tokens and temp for conciseness
        ai_raw_content = self._extract_content(response_json)

        # 🔹 Parse the AI's specific output format 🔹
        parsed_feedback = self._parse_ai_feedback_output(ai_raw_content)
        return parsed_feedback

    def generate_team_insights_realtime(self, team_data):
        """Analyzes team performance data."""
        team_name = team_data.get('team_name', 'N/A')
        members = ", ".join(team_data.get('members', []))
        rounds_summary = []
        for r in team_data.get('rounds', []):
            rounds_summary.append(f"Round {r.get('round')}: Average Score {r.get('average_score')}, Feedback: {r.get('team_feedback', 'N/A')}")

        prompt_text = f"""Analyze the performance of team {team_name} with members {members}.
        Summary of rounds: {'; '.join(rounds_summary)}.
        Provide a concise overall assessment of their strengths, weaknesses, and a key area for improvement based on their trends. Keep it to 3-4 sentences."""

        messages = [{"role": "user", "content": prompt_text}]
        response_json = self._call_sarvam_ai(messages, max_tokens=150, temperature=0.6)
        return self._extract_content(response_json)

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

        Provide a concise, 2-3 sentence summary of their judging tendencies, including any biases or notable patterns. Focus on constructive observations for teams debating in front of this judge."""

        messages = [{"role": "user", "content": prompt_text}]
        response_json = self._call_sarvam_ai(messages, max_tokens=120, temperature=0.6)
        return self._extract_content(response_json)

# Example usage (for testing locally, remove when deploying)
if __name__ == "__main__":
    # Ensure SARVAM_API_KEY is set in your environment
    # os.environ["SARVAM_API_KEY"] = "YOUR_SARVAM_API_KEY" # <--- Set your actual API Key for local testing

    try:
        ai = AIIntegration()

        # Test Speaker Feedback
        test_speaker_data = {
            "name": "Arjun Verma",
            "team": "GD A",
            "role": "Closing Government - 1st Speaker",
            "round": "Round 1",
            "score": 78,
            "feedback": {
                "general_feedback": "Your arguments were novel and well-structured.",
                "improvement_advice": "Try to back your claims with stronger data and clearer links to the motion."
            }
        }
        speaker_feedback = ai.generate_speaker_feedback(test_speaker_data)
        print("\n--- Speaker Feedback ---")
        print(f"General Feedback: {speaker_feedback['general_feedback']}")
        print(f"Improvement Advice: {speaker_feedback['improvement_advice']}")

        # Test Team Insights
        test_team_data = {
            "team_name": "GD A",
            "members": ["Arjun Verma", "Aarav Mehta"],
            "rounds": [\
                {"round": "Round 1", "average_score": 79, "team_feedback": "Strong opening, good teamwork."},\
                {"round": "Round 2", "average_score": 81, "team_feedback": "Improved rebuttals, struggled with POIs."},\
            ]
        }
        team_insights = ai.generate_team_insights_realtime(test_team_data)
        print("\n--- Team Insights ---")
        print(team_insights)

        # Test Judge Analysis
        test_judge_data = {
            "judge_name": "Arjun Mehta",
            "judge_style": "Strict, focuses on logical consistency",
            "overall_judging_insight": "Tends to reward clear argumentation over rhetoric.",
            "rounds": [\
                {"round": "Round 1", "speakers_scored": [{"name": "Speaker A", "score": 75}, {"name": "Speaker B", "score": 80}]},\
                {"round": "Round 2", "speakers_scored": [{"name": "Speaker C", "score": 78}, {"name": "Speaker D", "score": 82}]},\
            ]
        }
        judge_insights = ai.analyze_judge_comprehensive(test_judge_data)
        print("\n--- Judge Insights ---")
        print(judge_insights)

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during AI integration test: {e}")

