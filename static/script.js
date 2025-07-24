let speakerData, teamData, judgeData;
let speakerChart, teamChart;

// Define a placeholder for your backend API URL.
// This will be replaced by Render when your static site is deployed.
const API_BASE_URL = 'YOUR_PYTHON_BACKEND_RENDER_URL'; // <<< IMPORTANT: Placeholder!

async function loadData() {
    try {
        // --- MODIFIED: Fetch data from your Python backend endpoints ---
        // Ensure your app.py's endpoints are configured to return data
        // in the format expected by your frontend for these fetches.
        // Also, make sure the JSON filenames in app.py's load_json match
        // the content needed for speakerData, teamData, judgeData.

        // Fetching from backend endpoints
        speakerData = await fetch(`${API_BASE_URL}/speakers`).then(res => res.json());
        teamData = await fetch(`${API_BASE_URL}/teams`).then(res => res.json());
        judgeData = await fetch(`${API_BASE_URL}/judges`).then(res => res.json());
        // --- END MODIFIED ---

        populateDropdowns();
        showSpeakerChart();
        showTeamChart();
        // Ensure judgeData.overall_judging_insight exists in the data returned by /judges
        if (judgeData && judgeData.overall_judging_insight) {
            document.getElementById("judgeInsight").innerText = judgeData.overall_judging_insight;
        } else {
            console.warn("Judge insight not found in data from /judges endpoint.");
            document.getElementById("judgeInsight").innerText = "No overall judge insight available.";
        }
    } catch (err) {
        console.error("Error loading data:", err);
        alert("There was an error loading the data from the server. Please try again later.");
    }
}

function populateDropdowns() {
    const roundDropdown = document.getElementById("roundDropdown");
    const judgeRoundDropdown = document.getElementById("judgeRoundDropdown");
    roundDropdown.innerHTML = "";
    judgeRoundDropdown.innerHTML = "";

    // Ensure speakerData is an array before using forEach
    if (Array.isArray(speakerData)) {
        speakerData.forEach((entry, index) => {
            const opt = document.createElement("option");
            opt.value = index;
            opt.text = entry.round;
            roundDropdown.add(opt);
        });
    } else {
        console.error("speakerData is not an array:", speakerData);
    }

    // Ensure judgeData.rounds is an array before using forEach
    if (judgeData && Array.isArray(judgeData.rounds)) {
        judgeData.rounds.forEach((round, index) => {
            const opt = document.createElement("option");
            opt.value = index;
            opt.text = round.round;
            judgeRoundDropdown.add(opt);
        });
    } else {
        console.error("judgeData.rounds is not an array:", judgeData);
    }

    showSpeakerData();
    showJudgeData();
}

function showSpeakerData() {
    const index = document.getElementById("roundDropdown").value;
    // Ensure speakerData[index] exists before accessing its properties
    const data = speakerData[index];
    if (data) {
        document.getElementById("speakerInfo").innerHTML = `
            <strong>Round:</strong> ${data.round}<br>
            <strong>Score:</strong> ${data.score}<br>
            <strong>Feedback:</strong><br>
            <em>${data.feedback.general_feedback}</em><br>
            <em>${data.feedback.improvement_advice}</em>
        `;
    } else {
        document.getElementById("speakerInfo").innerHTML = "No speaker data available for this round.";
    }
}

function showTeamChart() {
    const ctx = document.getElementById("teamChart").getContext("2d");
    // Ensure teamData and teamData.rounds exist and are arrays
    const rounds = (teamData && Array.isArray(teamData.rounds)) ? teamData.rounds.map(r => r.round) : [];
    const scores = (teamData && Array.isArray(teamData.rounds)) ? teamData.rounds.map(r => r.average_score) : [];

    if (teamChart) teamChart.destroy(); // Clear old chart if exists

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

    // Ensure teamData.rounds exists and has elements
    const latest = (teamData && Array.isArray(teamData.rounds) && teamData.rounds.length > 0) ? teamData.rounds.at(-1) : null;
    if (latest) {
        document.getElementById("teamInfo").innerHTML = `
            <strong>Team:</strong> ${teamData.team_name}<br>
            <strong>Members:</strong> ${teamData.members.join(", ")}<br>
            <strong>Latest Round Feedback:</strong><br>
            ${latest.team_feedback}
        `;
    } else {
        document.getElementById("teamInfo").innerHTML = "No team data available.";
    }
}

function showSpeakerChart() {
    const ctx = document.getElementById("speakerChart").getContext("2d");
    const labels = Array.isArray(speakerData) ? speakerData.map(d => d.round) : [];
    const scores = Array.isArray(speakerData) ? speakerData.map(d => d.score) : [];

    if (speakerChart) speakerChart.destroy(); // Clear old chart if exists

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
}

function showJudgeData() {
    const index = document.getElementById("judgeRoundDropdown").value;
    // Ensure judgeData and judgeData.rounds exist and has elements at index
    const round = (judgeData && Array.isArray(judgeData.rounds) && judgeData.rounds[index]) ? judgeData.rounds[index] : null;
    let html = "";
    if (round) {
        html = `<strong>${round.round}</strong><br>`;
        if (Array.isArray(round.speakers_scored)) {
            round.speakers_scored.forEach(speaker => {
                html += `👤 ${speaker.name}: <strong>${speaker.score}</strong><br>`;
            });
        }
    } else {
        html = "No judge data available for this round.";
    }
    document.getElementById("judgeInfo").innerHTML = html;
}

window.onload = loadData;
