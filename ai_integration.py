# AI Integration Module for TabbyCat (Sarvam-only)
# Handles Sarvam AI calls + analytics utilities

import requests
import json
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base64
from io import BytesIO

class AIIntegration:
    def __init__(self):
        # On Render, set in Environment Variables
        self.sarvam_api_key = os.getenv('SARVAM_API_KEY')

    # ---------------------------
    # Core Sarvam caller (fixed)
    # ---------------------------
    def _call_sarvam(self, prompt, max_tokens=700, temperature=0.7):
        """Sarvam AI API integration"""
        try:
            if not self.sarvam_api_key:
                return "Sarvam API key missing. Set SARVAM_API_KEY in environment."

            headers = {
                'Authorization': f'Bearer {self.sarvam_api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                # 🔧 Fix per your logs: model must be 'sarvam-m'
                'model': 'sarvam-m',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': max_tokens,
                'temperature': temperature
            }

            resp = requests.post(
                'https://api.sarvam.ai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            print(f"Sarvam API Status: {resp.status_code}")

            if resp.status_code == 200:
                result = resp.json()
                return result['choices'][0]['message']['content']
            else:
                print(f"Sarvam API Error Response: {resp.text}")
                return f"Sarvam Error ({resp.status_code}): {resp.text}"
        except requests.exceptions.Timeout:
            return "Sarvam request timeout."
        except Exception as e:
            print(f"Sarvam AI Error: {str(e)}")
            return f"Sarvam exception: {str(e)}"

    # ---------------------------
    # Existing: Speaker feedback
    # ---------------------------
    def generate_speaker_feedback(self, speaker_data: dict):
        """
        Input example:
        {
          "name": "Alice",
          "scores": [78, 81, 84],
          "feedback_history": ["Good structure", "Better engagement"]
        }
        """
        if not speaker_data:
            return {"error": "No speaker data provided"}

        name = speaker_data.get("name", "Speaker")
        scores = speaker_data.get("scores", [])
        analytics = self._generate_speaker_analytics(name, scores)

        prompt = f"""
        You are a debate coach AI. Using the analytics below, write precise, actionable feedback.

        Speaker: {name}
        Scores: {scores}
        Analytics:
        - Average Score: {analytics.get('avg_score')}
        - Trend: {analytics.get('trend')}
        - Consistency: {analytics.get('consistency')}
        - Percentile: {analytics.get('percentile')}
        - Improvement Rate: {analytics.get('improvement_rate')}%
        Prior Feedback: {speaker_data.get('feedback_history', [])}

        Output:
        1) 3-5 bullet improvement points
        2) A 2-sentence motivational note
        3) 1 drill to practice before next round
        """
        if self.sarvam_api_key:
            ai_text = self._call_sarvam(prompt)
        else:
            ai_text = self._fallback_speaker_insights(name, scores)

        return {
            "ai_feedback": ai_text,
            "analytics": analytics,
            "visualizations": self._create_speaker_visualizations(scores, name)
        }

    # ---------------------------
    # NEW: Motion → Strategy
    # ---------------------------
    def generate_motion_strategy(self, motion: str, side: str, motion_meta: dict | None = None):
        """
        Returns AI strategy suggestions for a motion/side.
        motion_meta can include prior win rates or tags like {"win_rate_gov":0.56,"themes":["ethics","safety"]}
        """
        meta_blob = json.dumps(motion_meta, indent=2) if motion_meta else "{}"
        prompt = f"""
        Motion: "{motion}"
        Side: {side}
        Context/Meta: {meta_blob}

        Task: Produce a crisp, tournament-grade strategy.
        Include:
        - 3 strongest arguments (with warrants & examples)
        - Likely opp rebuttals + your counters
        - Stakeholders to emphasize
        - Suggested 7-minute structure (time splits)
        - 2 zinger lines for summary

        Keep it concise and practical.
        """
        if self.sarvam_api_key:
            return {"strategy": self._call_sarvam(prompt)}
        return {"strategy": self._fallback_strategy(motion, side)}

    # ---------------------------------
    # NEW: Judge → Adaptation Guide
    # ---------------------------------
    def build_judge_adaptation_guide(self, judge_data: dict):
        """
        judge_data example structure (from your json):
        {
          "judge_name": "J1",
          "rounds": [...],
          "overall_judging_insight": "prefers structure"
        }
        """
        quick = self._quick_judge_stats(judge_data)
        prompt = f"""
        Judge profile:
        {json.dumps(judge_data, indent=2)}

        Quick stats:
        {json.dumps(quick, indent=2)}

        Task: Give a practical adaptation guide for speakers judged by this person.
        Include:
        - What they reward/penalize (bullets)
        - How to frame arguments for them
        - Style tips (signposting, weighing, comparatives)
        - 3 do's and 3 don'ts
        """
        if self.sarvam_api_key:
            text = self._call_sarvam(prompt)
        else:
            text = self._fallback_comprehensive_judge_analysis(judge_data)
        return {"adaptation_guide": text, "quick_stats": quick}

    # -----------------------------------
    # NEW: Round Report Card (One-click)
    # -----------------------------------
    def build_round_report(self, team_data: dict, speaker_list: list, judge_data: dict, motion: str, side: str):
        """
        Bundles everything for a post-round recap.
        """
        # Speaker mini-analytics
        sp_analytics = []
        for s in speaker_list or []:
            name = s.get("name","Speaker")
            scores = s.get("scores", [])
            sp_analytics.append({
                "name": name,
                "analytics": self._generate_speaker_analytics(name, scores)
            })

        # Simple team delta (last vs first)
        team_delta = self._simple_team_delta(team_data)

        # AI summary
        summary_prompt = f"""
        Build a concise post-round report.

        Motion: "{motion}" | Side: {side}

        Team:
        {json.dumps(team_data, indent=2)}

        Speaker Analytics:
        {json.dumps(sp_analytics, indent=2)}

        Judge:
        {json.dumps(judge_data, indent=2)}

        Include:
        - What went well / what to fix
        - 3 targeted drills for next round
        - 5-line narrative summary for coaches
        - 2 key risks for the next matchup
        """
        if self.sarvam_api_key:
            summary = self._call_sarvam(summary_prompt, max_tokens=900)
        else:
            summary = "Round report (fallback): solid structure, improve weighing and time mgmt."

        # One simple chart (scores over rounds if available)
        chart_b64 = self._team_chart(team_data)

        return {
            "summary": summary,
            "speakers": sp_analytics,
            "team_delta": team_delta,
            "chart_b64": chart_b64
        }

    # ---------------------------
    # Existing fallbacks
    # ---------------------------
    def _fallback_speaker_insights(self, name, scores):
        trend = "improving" if len(scores) > 1 and scores[-1] > scores[0] else "stable"
        avg = sum(scores)/len(scores) if scores else 0
        return f"{name}'s performance is {trend}. Average {avg:.1f}. Focus on consistency and impact weighing."

    def _fallback_strategy(self, motion, side):
        return f"For {side} on '{motion}': define terms tight, run 3 prongs with clear impact calc, pre-empt opp with short blocks."

    def _fallback_comprehensive_judge_analysis(self, judge_data):
        rounds = judge_data.get('rounds', [])
        if not rounds:
            return "Judge analysis: No scoring data available."
        all_scores = []
        for r in rounds:
            for sp in r.get('speakers_scored', []):
                all_scores.append(sp.get('score', 0))
        if not all_scores:
            return "Judge analysis: Insufficient data."
        avg_score = sum(all_scores)/len(all_scores)
        return f"Judge tends to average {avg_score:.1f}. Prefer structured, comparative analysis and crisp weighing."

    # ---------------------------
    # Analytics helpers
    # ---------------------------
    def _generate_speaker_analytics(self, speaker_name, scores):
        if not scores:
            return {"error": "No scores"}
        arr = np.array(scores)
        if len(scores) > 1:
            slope = np.polyfit(range(len(scores)), scores, 1)[0]
            trend = "improving" if slope > 0.5 else "declining" if slope < -0.5 else "stable"
            improvement_rate = ((scores[-1] - scores[0]) / scores[0]) * 100 if scores[0] else 0
        else:
            trend = "insufficient_data"
            improvement_rate = 0
        avg_score = float(np.mean(arr))
        std_dev = float(np.std(arr))
        consistency = "high" if std_dev < 3 else "moderate" if std_dev < 6 else "low"
        percentile = float(min(95, max(5, ((avg_score - 70) / 20) * 100)))
        return {
            "avg_score": round(avg_score,2),
            "std_dev": round(std_dev,2),
            "trend": trend,
            "consistency": consistency,
            "percentile": round(percentile,1),
            "improvement_rate": round(improvement_rate,1),
            "score_range": f"{min(scores)}-{max(scores)}",
            "total_rounds": len(scores)
        }

    def _create_speaker_visualizations(self, scores, speaker_name):
        try:
            if not scores:
                return {"error": "No scores for visualization"}
            rounds = list(range(1, len(scores)+1))
            fig, ax = plt.subplots(figsize=(8,5))
            ax.plot(rounds, scores, marker='o', linewidth=2)
            ax.set_title(f"{speaker_name} – Performance Trend")
            ax.set_xlabel("Round"); ax.set_ylabel("Score")
            ax.grid(True, alpha=0.3)
            for i, sc in enumerate(scores):
                ax.annotate(f'{sc}', (rounds[i], sc), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
            buf = BytesIO(); plt.tight_layout(); plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            b64 = base64.b64encode(buf.getvalue()).decode()
            plt.close('all')
            return {"trend_chart": b64, "chart_type":"performance_trend"}
        except Exception as e:
            print("Visualization error:", e)
            return {"error": f"viz failed: {e}"}

    def _quick_judge_stats(self, judge_data):
        rounds = judge_data.get('rounds', [])
        scores = []
        for r in rounds:
            for sp in r.get('speakers_scored', []):
                if isinstance(sp, dict):
                    scores.append(sp.get('score', 0))
        if not scores:
            return {"avg": None, "spread": None, "tendency": "unknown"}
        avg = sum(scores)/len(scores)
        spread = max(scores) - min(scores)
        tendency = "low-scorer" if avg < 72 else "mid-scorer" if avg < 78 else "high-scorer"
        return {"avg": round(avg,1), "spread": spread, "tendency": tendency}

    def _simple_team_delta(self, team_data):
        """Compare first and last round averages if present."""
        rounds = team_data.get('rounds', [])
        if not rounds:
            return {"delta": 0, "start": None, "end": None}
        start = rounds[0].get('average_score', None)
        end = rounds[-1].get('average_score', None)
        if isinstance(start, (int,float)) and isinstance(end, (int,float)):
            return {"delta": round(end - start, 2), "start": start, "end": end}
        return {"delta": 0, "start": start, "end": end}

    def _team_chart(self, team_data):
        """Simple chart: team avg per round (if available) -> base64"""
        rounds = team_data.get('rounds', [])
        if not rounds:
            return None
        xs, ys = [], []
        for i, r in enumerate(rounds, start=1):
            xs.append(i)
            ys.append(r.get('average_score', None))
        if not any(isinstance(y,(int,float)) for y in ys):
            return None
        fig, ax = plt.subplots(figsize=(7,4))
        ax.plot(xs, ys, marker='o', linewidth=2)
        ax.set_title("Team Average by Round"); ax.set_xlabel("Round"); ax.set_ylabel("Avg Score")
        ax.grid(True, alpha=0.3)
        buf = BytesIO(); plt.tight_layout(); plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        b64 = base64.b64encode(buf.getvalue()).decode()
        plt.close('all')
        return b64
