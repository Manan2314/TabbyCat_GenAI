let speakerData, teamData, judgeData;
let speakerChart, teamChart;

// Define your backend API URL.
// This should be the URL of your Render deployed Flask app.
const API_BASE_URL = 'https://tabbycat-genai.onrender.com'; 

async function loadData() {
    try {
        // Fetching from backend endpoints.
        // These now directly receive the expected data structures.
        speakerData = await fetch(`${API_BASE_URL}/speakers`).then(res => res.json());
        teamData = await fetch(`${API_BASE_URL}/teams`).then(res => res.json());
        judgeData = await fetch(`${API_BASE_URL}/judges`).then(res => res.json());

        // Log fetched data for debugging
        console.log("Fetched speakerData:", speakerData);
        console.log("Fetched teamData:", teamData);
        console.log("Fetched judgeData:", judgeData);

        populateDropdowns();
        showSpeakerChart();
        showTeamChart();
        
        // Ensure judgeData and its ai_insights exist
        const judgeInsightElement = document.getElementById("judgeInsight");
        if (judgeInsightElement) {
            if (judgeData && judgeData.ai_insights) {
                judgeInsightElement.innerText = judgeData.ai_insights;
            } else if (judgeData && judgeData.overall_judging_insight) {
                judgeInsightElement.innerText = judgeData.overall_judging_insight;
            } else {
                console.warn("Judge insight not found in data from /judges endpoint.");
                judgeInsightElement.innerText = "No overall judge insight available.";
            }
        }

        // 🔹 Handle Motion Data Display 🔹
        const motionDataResponse = await fetch(`${API_BASE_URL}/motions`).then(res => res.json());
        const motionAnalysisElement = document.getElementById("motionData");
        if (motionAnalysisElement && Array.isArray(motionDataResponse)) {
            let motionHtml = "<h4>Available Motions:</h4><ul>";
            motionDataResponse.forEach(motion => {
                motionHtml += `<li><strong>${motion.motion}</strong>: Gov Win Rate: ${motion.gov_win_rate}%, Opp Win Rate: ${motion.opp_win_rate}% - <em>${motion.insight}</em></li>`;
            });
            motionHtml += "</ul>";
            motionAnalysisElement.innerHTML = motionHtml;
        } else if (motionAnalysisElement) {
            motionAnalysisElement.innerHTML = "<p>No motion data available or invalid format.</p>";
        }


    } catch (err) {
        console.error("Error loading data:", err);
        displayMessageBox("Error", "There was an error loading the data from the server. Please try again later.");
    }
}

function populateDropdowns() {
    const roundDropdown = document.getElementById("roundDropdown");
    const judgeRoundDropdown = document.getElementById("judgeRoundDropdown");
    roundDropdown.innerHTML = "";
    judgeRoundDropdown.innerHTML = "";

    // speakerData is now directly an array of combined speaker round objects
    if (Array.isArray(speakerData)) {
        const uniqueRounds = [...new Set(speakerData.map(entry => entry.round))];
        uniqueRounds.forEach((roundName, index) => {
            const opt = document.createElement("option");
            opt.value = roundName; // Use roundName as value for easier lookup
            opt.text = roundName;
            roundDropdown.add(opt);
        });
    } else {
        console.error("speakerData is not an array:", speakerData);
    }

    // judgeData is now the full judge object, and judgeData.rounds should be an array
    if (judgeData && Array.isArray(judgeData.rounds)) {
        judgeData.rounds.forEach((round, index) => {
            const opt = document.createElement("option");
            opt.value = index;
            opt.text = round.round;
            judgeRoundDropdown.add(opt);
        });
    } else {
        console.error("judgeData or judgeData.rounds is not an array:", judgeData);
    }

    // Trigger display of initial data
    showSpeakerData();
    showJudgeData();
}

function showSpeakerData() {
    const dropdown = document.getElementById("roundDropdown");
    // Check if dropdown has options before trying to access selectedIndex
    if (!dropdown || dropdown.options.length === 0) {
        document.getElementById("speakerInfo").innerHTML = "No rounds available for speaker data.";
        return;
    }
    const selectedRoundName = dropdown.options[dropdown.selectedIndex].value; // Use value (which is now roundName)
    
    const dataForSelectedRound = speakerData.find(item => item.round === selectedRoundName);

    const speakerInfoElement = document.getElementById("speakerInfo");
    if (speakerInfoElement) {
        if (dataForSelectedRound) {
            const originalData = dataForSelectedRound;
            const aiInsights = dataForSelectedRound.ai_insights;

            speakerInfoElement.innerHTML = `
                <strong>Round:</strong> ${originalData.round || 'N/A'}<br>
                <strong>Score:</strong> ${originalData.score || 'N/A'}<br>
                <strong>Feedback:</strong><br>
                <em>${originalData.feedback?.general_feedback || 'N/A'}</em><br>
                <em>${originalData.feedback?.improvement_advice || 'N/A'}</em><br>
                <br>
                <strong>AI Insights:</strong><br>
                <em>${aiInsights || 'No AI insights available.'}</em>
            `;
        } else {
            speakerInfoElement.innerHTML = "No speaker data available for this round.";
        }
    }
}

function showTeamChart() {
    const ctxElement = document.getElementById("teamChart");
    if (!ctxElement) { // 🔹 Defensive check for canvas element
        console.error("Team chart canvas element not found.");
        return;
    }
    const ctx = ctxElement.getContext("2d");

    const rounds = (teamData && Array.isArray(teamData.rounds)) ? teamData.rounds.map(r => r.round) : [];
    const scores = (teamData && Array.isArray(teamData.rounds)) ? teamData.rounds.map(r => r.average_score) : [];

    if (teamChart) teamChart.destroy(); // Clear old chart if exists

    if (rounds.length > 0 && scores.length > 0) {
        teamChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: rounds,
                datasets: [{
                    label: "Team Average Score",
                    data: scores,
                    borderColor: "#2980b9",
                    fill: false
                }]
            }
        });
    } else {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.fillText("No team chart data available.", ctx.canvas.width / 2, ctx.canvas.height / 2);
    }

    const teamInfoElement = document.getElementById("teamInfo");
    if (teamInfoElement) {
        const latest = (teamData && Array.isArray(teamData.rounds) && teamData.rounds.length > 0) ? teamData.rounds.at(-1) : null;
        if (teamData && teamData.team_name) {
            teamInfoElement.innerHTML = `
                <strong>Team:</strong> ${teamData.team_name || 'N/A'}<br>
                <strong>Members:</strong> ${teamData.members ? teamData.members.join(", ") : 'N/A'}<br>
                ${latest ? `<strong>Latest Round Feedback:</strong><br>${latest.team_feedback || 'N/A'}` : 'No recent round feedback.'}
                <br>
                <strong>AI Insights:</strong><br>
                <em>${teamData.ai_insights || 'No AI insights available.'}</em>
            `;
        } else {
            teamInfoElement.innerHTML = "No team data available.";
        }
    }
}

function showSpeakerChart() {
    const ctxElement = document.getElementById("speakerChart");
    if (!ctxElement) { // 🔹 Defensive check for canvas element
        console.error("Speaker chart canvas element not found.");
        return;
    }
    const ctx = ctxElement.getContext("2d");

    const labels = Array.isArray(speakerData) ? speakerData.map(d => d.round) : [];
    const scores = Array.isArray(speakerData) ? speakerData.map(d => d.score) : [];

    if (speakerChart) speakerChart.destroy(); // Clear old chart if exists

    if (labels.length > 0 && scores.length > 0) {
        speakerChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Speaker Score",
                    data: scores,
                    borderColor: "#e67e22",
                    fill: false
                }]
            }
        });
    } else {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.fillText("No speaker chart data available.", ctx.canvas.width / 2, ctx.canvas.height / 2);
    }
}

function showJudgeData() {
    const index = document.getElementById("judgeRoundDropdown").value;
    const round = (judgeData && Array.isArray(judgeData.rounds) && judgeData.rounds[index]) ? judgeData.rounds[index] : null;
    let html = "";
    if (round) {
        html = `<strong>${round.round}</strong><br>`;
        if (Array.isArray(round.speakers_scored)) {
            round.speakers_scored.forEach(speaker => {
                html += `👤 ${speaker.name || 'N/A'}: <strong>${speaker.score || 'N/A'}</strong><br>`;
            });
        }
        html += `<br><strong>AI Insights:</strong><br><em>${judgeData.ai_insights || 'No AI insights available for judge.'}</em>`;

    } else {
        html = "No judge data available for this round.";
    }
    document.getElementById("judgeInfo").innerHTML = html;
}

// Utility for displaying messages (replaces alert)
function displayMessageBox(title, message) {
    console.log(`Message Box - ${title}: ${message}`);
}

window.onload = loadData;
