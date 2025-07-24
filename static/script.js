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
        // The overall_judging_insight is part of the raw data, and ai_insights is the AI-generated one.
        // You might want to display both or choose one.
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

    } catch (err) {
        console.error("Error loading data:", err);
        // Use a custom message box instead of alert() for better UX
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
        // Use a Set to get unique rounds if a speaker has multiple entries
        const uniqueRounds = [...new Set(speakerData.map(entry => entry.round))];
        uniqueRounds.forEach((roundName, index) => {
            const opt = document.createElement("option");
            opt.value = index; // Use index or actual round name if unique
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
    const selectedRoundName = dropdown.options[dropdown.selectedIndex].text; // Get the text of the selected option
    
    // Find the speaker data for the selected round
    // speakerData is an array of { original_speaker_data_for_round, ai_insights }
    const dataForSelectedRound = speakerData.find(item => item.round === selectedRoundName);

    const speakerInfoElement = document.getElementById("speakerInfo");
    if (speakerInfoElement) {
        if (dataForSelectedRound) {
            // Access original data and AI insights
            const originalData = dataForSelectedRound; // Since we combined it directly
            const aiInsights = dataForSelectedRound.ai_insights;

            speakerInfoElement.innerHTML = `
                <strong>Round:</strong> ${originalData.round}<br>
                <strong>Score:</strong> ${originalData.score}<br>
                <strong>Feedback:</strong><br>
                <em>${originalData.feedback.general_feedback || 'N/A'}</em><br>
                <em>${originalData.feedback.improvement_advice || 'N/A'}</em><br>
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
    const ctx = document.getElementById("teamChart").getContext("2d");
    // teamData is now directly the team object
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
        // Clear canvas if no data
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        // Optionally display a message on the canvas or below it
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.fillText("No team chart data available.", ctx.canvas.width / 2, ctx.canvas.height / 2);
    }

    const teamInfoElement = document.getElementById("teamInfo");
    if (teamInfoElement) {
        const latest = (teamData && Array.isArray(teamData.rounds) && teamData.rounds.length > 0) ? teamData.rounds.at(-1) : null;
        if (teamData && teamData.team_name) { // Check if teamData has basic info
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
    const ctx = document.getElementById("speakerChart").getContext("2d");
    // speakerData is now directly an array of combined speaker round objects
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
        // Clear canvas if no data
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        // Optionally display a message on the canvas or below it
        ctx.font = "16px Arial";
        ctx.textAlign = "center";
        ctx.fillText("No speaker chart data available.", ctx.canvas.width / 2, ctx.canvas.height / 2);
    }
}

function showJudgeData() {
    const index = document.getElementById("judgeRoundDropdown").value;
    // judgeData is now the full judge object
    const round = (judgeData && Array.isArray(judgeData.rounds) && judgeData.rounds[index]) ? judgeData.rounds[index] : null;
    let html = "";
    if (round) {
        html = `<strong>${round.round}</strong><br>`;
        if (Array.isArray(round.speakers_scored)) {
            round.speakers_scored.forEach(speaker => {
                html += `👤 ${speaker.name || 'N/A'}: <strong>${speaker.score || 'N/A'}</strong><br>`;
            });
        }
        // Display AI insights for the judge
        html += `<br><strong>AI Insights:</strong><br><em>${judgeData.ai_insights || 'No AI insights available for judge.'}</em>`;

    } else {
        html = "No judge data available for this round.";
    }
    document.getElementById("judgeInfo").innerHTML = html;
}

// Utility for displaying messages (replaces alert)
function displayMessageBox(title, message) {
    // Implement a simple modal or div to show messages
    // For now, let's just log to console if no modal is set up
    console.log(`Message Box - ${title}: ${message}`);
    // In a real app, you'd create/show a div like:
    // const msgBox = document.getElementById('messageBox');
    // msgBox.querySelector('.title').innerText = title;
    // msgBox.querySelector('.content').innerText = message;
    // msgBox.style.display = 'block'; // Show the modal
}

window.onload = loadData;
