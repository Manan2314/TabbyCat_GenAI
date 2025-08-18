
// script.js
let speakerData, teamData, judgeData, motionData;

async function loadData() {
  try {
    speakerData = await fetch("/speakers").then(res => res.json());
    teamData = await fetch("/teams").then(res => res.json());
    judgeData = await fetch("/judges").then(res => res.json());
    motionData = await fetch("/motions").then(res => res.json());
    
    populateDropdowns();
    showSpeakerChart();
    await showTeamChart();
    showMotionData();
    
    // Enhanced judge insight with AI
    const judgeInsightElement = document.getElementById("judgeInsight");
    judgeInsightElement.innerHTML = `
      ${judgeData.overall_judging_insight}
      <div class="ai-insights-section" style="margin-top: 15px;">
        <h4>AI Judge Pattern Analysis <span class="loading">Generating...</span></h4>
        <div id="aiOverallJudgeInsights" class="ai-insights">Loading overall judge insights...</div>
      </div>
    `;
    
    // Generate overall AI judge insights
    const overallInsights = await getAIJudgeComprehensive(judgeData);
    document.getElementById("aiOverallJudgeInsights").innerHTML = overallInsights;
    document.querySelector("#judgeInsight .loading").style.display = "none";
  } catch (error) {
    console.error('Error loading data:', error);
    document.body.innerHTML = '<div class="error">Error loading data. Please refresh the page.</div>';
  }
}

function populateDropdowns() {
  const roundDropdown = document.getElementById("roundDropdown");
  const judgeRoundDropdown = document.getElementById("judgeRoundDropdown");
  
  speakerData.forEach((entry, index) => {
    const opt = document.createElement("option");
    opt.value = index;
    opt.text = entry.round;
    roundDropdown.add(opt);
  });
  
  judgeData.rounds.forEach((round, index) => {
    const opt = document.createElement("option");
    opt.value = index;
    opt.text = round.round;
    judgeRoundDropdown.add(opt);
  });
  
  showSpeakerData();
  showJudgeData();
}

async function showSpeakerData() {
  const index = document.getElementById("roundDropdown").value;
  const data = speakerData[index];
  const scores = speakerData.map(d => d.score);
  
  document.getElementById("speakerInfo").innerHTML = `
    <div class="info-card">
      <h3>${data.name} - ${data.team}</h3>
      <div class="info-row">
        <span class="label">Round:</span>
        <span class="value">${data.round}</span>
      </div>
      <div class="info-row">
        <span class="label">Role:</span>
        <span class="value">${data.role}</span>
      </div>
      <div class="info-row">
        <span class="label">Score:</span>
        <span class="value score">${data.score}</span>
      </div>
      <div class="feedback-section">
        <h4>Feedback</h4>
        <div class="feedback-item positive">
          <strong>General:</strong> ${data.feedback.general_feedback}
        </div>
        <div class="feedback-item improvement">
          <strong>Improvement:</strong> ${data.feedback.improvement_advice}
        </div>
      </div>
      <div class="ai-insights-section">
        <h4>AI Insights <span class="loading">Generating...</span></h4>
        <div id="aiSpeakerInsights" class="ai-insights">Loading AI insights...</div>
      </div>
      <div class="analytics-controls">
        <button onclick="generateLiveStrategy('${data.name}')" class="ai-button">
          Generate AI Strategy
        </button>
        <button onclick="generatePerformanceReport()" class="analytics-btn">
          Performance Report
        </button>
      </div>
    </div>
  `;
  
  // Generate AI insights
  const aiInsights = await getAISpeakerInsights(data.name, scores);
  document.getElementById("aiSpeakerInsights").innerHTML = aiInsights;
  document.querySelector(".loading").style.display = "none";
}

async function showTeamChart() {
  const ctx = document.getElementById("teamChart").getContext("2d");
  const rounds = teamData.rounds.map(r => r.round);
  const scores = teamData.rounds.map(r => r.average_score);
  
  new Chart(ctx, {
    type: "line",
    data: {
      labels: rounds,
      datasets: [{
        label: "Team Average Score",
        data: scores,
        borderColor: "#3498db",
        backgroundColor: "rgba(52, 152, 219, 0.1)",
        fill: true,
        tension: 0.4,
        pointBackgroundColor: "#3498db",
        pointBorderColor: "#2980b9",
        pointHoverBackgroundColor: "#2980b9",
        pointHoverBorderColor: "#1f5582"
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 70,
          max: 90
        }
      }
    }
  });
  
  const latest = teamData.rounds.at(-1);
  document.getElementById("teamInfo").innerHTML = `
    <div class="info-card">
      <h3>${teamData.team_name}</h3>
      <div class="info-row">
        <span class="label">Members:</span>
        <span class="value">${teamData.members.join(", ")}</span>
      </div>
      <div class="info-row">
        <span class="label">Latest Average:</span>
        <span class="value score">${latest.average_score}</span>
      </div>
      <div class="feedback-section">
        <h4>Latest Team Feedback</h4>
        <div class="feedback-item">${latest.team_feedback}</div>
      </div>
      <div class="ai-insights-section">
        <h4>AI Team Analysis <span class="loading">Generating...</span></h4>
        <div id="aiTeamInsights" class="ai-insights">Loading AI team insights...</div>
      </div>
      <button onclick="generateTeamStrategy()" class="ai-button">
        Generate Team Strategy
      </button>
    </div>
  `;
  
  // Generate AI team insights
  const aiInsights = await getAITeamInsights(teamData);
  document.getElementById("aiTeamInsights").innerHTML = aiInsights;
  document.querySelector("#teamInfo .loading").style.display = "none";
}

function showSpeakerChart() {
  const ctx = document.getElementById("speakerChart").getContext("2d");
  const labels = speakerData.map(d => d.round);
  const scores = speakerData.map(d => d.score);
  
  new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Speaker Score",
        data: scores,
        borderColor: "#e74c3c",
        backgroundColor: "rgba(231, 76, 60, 0.1)",
        fill: true,
        tension: 0.4,
        pointBackgroundColor: "#e74c3c",
        pointBorderColor: "#c0392b",
        pointHoverBackgroundColor: "#c0392b",
        pointHoverBorderColor: "#a93226"
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: false,
          min: 70,
          max: 90
        }
      }
    }
  });
}

async function showJudgeData() {
  const index = document.getElementById("judgeRoundDropdown").value;
  const round = judgeData.rounds[index];
  
  let html = `
    <div class="info-card">
      <h3>${judgeData.judge_name} - ${round.round}</h3>
      <div class="speakers-scored">
  `;
  
  round.speakers_scored.forEach(speaker => {
    html += `
      <div class="speaker-score">
        <span class="speaker-name">${speaker.name}</span>
        <span class="score">${speaker.score}</span>
      </div>
    `;
  });
  
  html += `
      </div>
      <div class="ai-insights-section">
        <h4>AI Judge Analysis <span class="loading">Generating...</span></h4>
        <div id="aiJudgeInsights" class="ai-insights">Loading comprehensive judge insights...</div>
      </div>
      <button onclick="generateJudgeStrategy()" class="ai-button">
        Judge Adaptation Tips
      </button>
    </div>
  `;
  
  document.getElementById("judgeInfo").innerHTML = html;
  
  // Generate AI judge insights
  const aiInsights = await getAIJudgeComprehensive(judgeData);
  document.getElementById("aiJudgeInsights").innerHTML = aiInsights;
  document.querySelector("#judgeInfo .loading").style.display = "none";
}

function showMotionData() {
  const motionSection = document.getElementById("motionData");
  let html = '<div class="motions-container">';
  
  motionData.forEach(motion => {
    const govAdvantage = motion.gov_win_rate > 55;
    const balanceClass = Math.abs(motion.gov_win_rate - motion.opp_win_rate) < 10 ? 'balanced' : 
                        govAdvantage ? 'gov-favored' : 'opp-favored';
    
    html += `
      <div class="motion-card ${balanceClass}">
        <h4>${motion.motion}</h4>
        <div class="motion-stats">
          <div class="win-rates">
            <div class="win-rate gov">
              <span class="label">Government:</span>
              <div class="percentage-bar">
                <div class="bar gov-bar" style="width: ${motion.gov_win_rate}%"></div>
                <span class="percentage">${motion.gov_win_rate}%</span>
              </div>
            </div>
            <div class="win-rate opp">
              <span class="label">Opposition:</span>
              <div class="percentage-bar">
                <div class="bar opp-bar" style="width: ${motion.opp_win_rate}%"></div>
                <span class="percentage">${motion.opp_win_rate}%</span>
              </div>
            </div>
          </div>
          <div class="motion-difficulty">
            <span class="difficulty-label">Balance Score:</span>
            <span class="difficulty-score ${balanceClass}">
              ${Math.abs(motion.gov_win_rate - motion.opp_win_rate) < 10 ? 'Well Balanced' : 
                govAdvantage ? 'Gov Favored' : 'Opp Favored'}
            </span>
          </div>
        </div>
        <div class="insight">
          <strong>Strategic Insight:</strong> ${motion.insight}
        </div>
        <div class="ai-suggestion">
          <strong>AI Enhancement Ready:</strong> 
          <em>This motion can benefit from AI-generated debate strategies and argument frameworks.</em>
        </div>
      </div>
    `;
  });
  
  html += '</div>';
  motionSection.innerHTML = html;
}

// Real-time AI integration functions
async function generateAIInsights(endpoint, data) {
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
    return await response.json();
  } catch (error) {
    console.error('AI API Error:', error);
    return null;
  }
}

async function getAISpeakerInsights(speakerName, scores, motion = '') {
  const aiResponse = await generateAIInsights('/ai/analyze-speaker', {
    speaker_name: speakerName,
    scores: scores,
    motion: motion
  });
  
  if (aiResponse && aiResponse.status === 'success') {
    // Display enhanced insights with analytics
    if (aiResponse.insights.analytics) {
      return formatEnhancedInsights(aiResponse.insights);
    }
    return aiResponse.insights;
  }
  return 'AI insights temporarily unavailable';
}

function formatEnhancedInsights(insights) {
  const analytics = insights.analytics;
  const aiAnalysis = insights.ai_analysis;
  
  return `
    <div class="enhanced-insights">
      <div class="analytics-summary">
        <h5>Performance Analytics</h5>
        <div class="analytics-grid">
          <div class="metric">
            <span class="metric-label">Average Score:</span>
            <span class="metric-value">${analytics.avg_score.toFixed(1)}</span>
          </div>
          <div class="metric">
            <span class="metric-label">Trend:</span>
            <span class="metric-value trend-${analytics.trend}">${analytics.trend.toUpperCase()}</span>
          </div>
          <div class="metric">
            <span class="metric-label">Consistency:</span>
            <span class="metric-value">${analytics.consistency.toUpperCase()}</span>
          </div>
          <div class="metric">
            <span class="metric-label">Percentile:</span>
            <span class="metric-value">${analytics.percentile.toFixed(0)}th</span>
          </div>
        </div>
      </div>
      <div class="ai-analysis">
        <h5>AI Analysis</h5>
        <p>${aiAnalysis}</p>
      </div>
    </div>
  `;
}

async function generatePerformanceReport() {
  const button = event.target;
  const originalText = button.innerHTML;
  
  try {
    button.innerHTML = "Generating Report...";
    button.disabled = true;
    
    const response = await fetch('/ai/performance-report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        speaker_data: speakerData
      })
    });
    
    const data = await response.json();
    
    if (data && data.status === 'success' && data.report_chart) {
      displayPerformanceReport(data.report_chart);
    } else {
      console.error('Performance report failed:', data);
      showErrorMessage(`Failed to generate performance report: ${data.error || 'Unknown error'}`);
    }
  } catch (error) {
    console.error('Failed to generate performance report:', error);
    showErrorMessage('Network error while generating report. Please check your connection.');
  } finally {
    button.innerHTML = originalText;
    button.disabled = false;
  }
}

function showErrorMessage(message) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.innerHTML = `
    <div class="error-content">
      <span class="error-icon">Warning</span>
      <span class="error-text">${message}</span>
      <button onclick="this.parentElement.parentElement.remove()" class="error-close">×</button>
    </div>
  `;
  document.body.appendChild(errorDiv);
  
  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (errorDiv.parentElement) {
      errorDiv.remove();
    }
  }, 5000);
}

function displayPerformanceReport(chartBase64) {
  const reportSection = document.createElement('div');
  reportSection.className = 'performance-report-section';
  reportSection.innerHTML = `
    <h3>Performance Analytics Report</h3>
    <div class="report-chart">
      <img src="data:image/png;base64,${chartBase64}" alt="Performance Report" style="max-width: 100%; height: auto;">
    </div>
    <button onclick="downloadReport('${chartBase64}')" class="download-btn">
      Download Report
    </button>
  `;
  
  document.getElementById('main-content').appendChild(reportSection);
}

function downloadReport(chartBase64) {
  const link = document.createElement('a');
  link.href = 'data:image/png;base64,' + chartBase64;
  link.download = 'performance-report.png';
  link.click();
}

async function getAIMotionStrategy(motion, side, teamStrengths = []) {
  const aiResponse = await generateAIInsights('/ai/motion-strategy', {
    motion: motion,
    side: side,
    team_strengths: teamStrengths
  });
  
  if (aiResponse && aiResponse.status === 'success') {
    return aiResponse.strategy;
  }
  return 'AI strategy generation temporarily unavailable';
}

async function getAIJudgeInsights(judgeHistory) {
  const aiResponse = await generateAIInsights('/ai/judge-insights', {
    judge_history: judgeHistory
  });
  
  if (aiResponse && aiResponse.status === 'success') {
    return aiResponse.insights;
  }
  return 'AI judge analysis temporarily unavailable';
}

async function getAITeamInsights(teamData) {
  const aiResponse = await generateAIInsights('/ai/team-insights', {
    team_data: teamData
  });
  
  if (aiResponse && aiResponse.status === 'success') {
    return aiResponse.insights;
  }
  return 'AI team analysis temporarily unavailable';
}

async function getAIJudgeComprehensive(judgeData) {
  const aiResponse = await generateAIInsights('/ai/judge-comprehensive', {
    judge_data: judgeData
  });
  
  if (aiResponse && aiResponse.status === 'success') {
    return aiResponse.insights;
  }
  return 'AI comprehensive judge analysis temporarily unavailable';
}

async function generateLiveStrategy(speakerName) {
  const button = event.target;
  button.innerHTML = "Generating...";
  button.disabled = true;
  
  // Get current motion (simplified - you can enhance this)
  const motions = motionData;
  const randomMotion = motions[Math.floor(Math.random() * motions.length)];
  
  const strategy = await getAIMotionStrategy(
    randomMotion.motion, 
    "Government", 
    ["Strong argumentation", "Good delivery"]
  );
  
  // Display strategy in a modal or popup
  showStrategyModal(strategy, randomMotion.motion);
  
  button.innerHTML = "Generate AI Strategy";
  button.disabled = false;
}

function showStrategyModal(strategy, title, subtitle = '') {
  const modal = document.createElement('div');
  modal.className = 'strategy-modal';
  modal.innerHTML = `
    <div class="modal-content">
      <div class="modal-header">
        <h3>${title}</h3>
        <span class="close" onclick="this.parentElement.parentElement.parentElement.remove()">&times;</span>
      </div>
      <div class="modal-body">
        ${subtitle ? `<h4>${subtitle}</h4>` : ''}
        <div class="strategy-content">${strategy}</div>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
}

async function generateTeamStrategy() {
  const button = event.target;
  button.innerHTML = "Generating...";
  button.disabled = true;
  
  const teamInsights = await getAITeamInsights(teamData);
  showStrategyModal(teamInsights, "AI Team Strategy", `Team: ${teamData.team_name}`);
  
  button.innerHTML = "Generate Team Strategy";
  button.disabled = false;
}

async function generateJudgeStrategy() {
  const button = event.target;
  button.innerHTML = "Generating...";
  button.disabled = true;
  
  const judgeInsights = await getAIJudgeComprehensive(judgeData);
  showStrategyModal(judgeInsights, "AI Judge Adaptation Strategy", `Judge: ${judgeData.judge_name}`);
  
  button.innerHTML = "Judge Adaptation Tips";
  button.disabled = false;
}

// Add real-time AI features to motion data
async function enhanceMotionWithAI() {
  const motionCards = document.querySelectorAll('.motion-card');
  motionCards.forEach(async (card, index) => {
    const motion = motionData[index];
    const aiButton = document.createElement('button');
    aiButton.className = 'ai-strategy-btn';
    aiButton.innerHTML = 'Get AI Strategy';
    aiButton.onclick = async () => {
      aiButton.innerHTML = 'Loading...';
      const strategy = await getAIMotionStrategy(motion.motion, 'Government');
      showStrategyModal(strategy, motion.motion);
      aiButton.innerHTML = 'Get AI Strategy';
    };
    card.appendChild(aiButton);
  });
}

window.onload = async () => {
  await loadData();
  enhanceMotionWithAI();
};
