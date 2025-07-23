let speakerData, teamData, judgeData;
let speakerChart, teamChart;

async function loadData() {
  try {
    speakerData = await fetch("./speaker.json").then(res => res.json());
    teamData = await fetch("./team.json").then(res => res.json());
    judgeData = await fetch("./judge.json").then(res => res.json());

    populateDropdowns();
    showSpeakerChart();
    showTeamChart();
    document.getElementById("judgeInsight").innerText = judgeData.overall_judging_insight;
  } catch (err) {
    console.error("Error loading data:", err);
    alert("There was an error loading the data files. Please check if they exist and are in the correct location.");
  }
}

function populateDropdowns() {
  const roundDropdown = document.getElementById("roundDropdown");
  const judgeRoundDropdown = document.getElementById("judgeRoundDropdown");
  roundDropdown.innerHTML = "";
  judgeRoundDropdown.innerHTML = "";

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

function showSpeakerData() {
  const index = document.getElementById("roundDropdown").value;
  const data = speakerData[index];
  document.getElementById("speakerInfo").innerHTML = `
    <strong>Round:</strong> ${data.round}<br>
    <strong>Score:</strong> ${data.score}<br>
    <strong>Feedback:</strong><br>
    <em>${data.feedback.general_feedback}</em><br>
    <em>${data.feedback.improvement_advice}</em>
  `;
}

function showTeamChart() {
  const ctx = document.getElementById("teamChart").getContext("2d");
  const rounds = teamData.rounds.map(r => r.round);
  const scores = teamData.rounds.map(r => r.average_score);

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

  const latest = teamData.rounds.at(-1);
  document.getElementById("teamInfo").innerHTML = `
    <strong>Team:</strong> ${teamData.team_name}<br>
    <strong>Members:</strong> ${teamData.members.join(", ")}<br>
    <strong>Latest Round Feedback:</strong><br>
    ${latest.team_feedback}
  `;
}

function showSpeakerChart() {
  const ctx = document.getElementById("speakerChart").getContext("2d");
  const labels = speakerData.map(d => d.round);
  const scores = speakerData.map(d => d.score);

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
  const round = judgeData.rounds[index];
  let html = `<strong>${round.round}</strong><br>`;
  round.speakers_scored.forEach(speaker => {
    html += `👤 ${speaker.name}: <strong>${speaker.score}</strong><br>`;
  });
  document.getElementById("judgeInfo").innerHTML = html;
}

window.onload = loadData;
