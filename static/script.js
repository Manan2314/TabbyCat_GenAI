// This script now fetches data from the JSON files.

/**
 * Toggles the visibility of different content sections.
 * @param {string} sectionId The ID of the section to show.
 */
function showSection(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
    }
}

/**
 * Fetches data from a JSON file and returns it.
 * @param {string} filePath The path to the JSON file.
 * @returns {Promise<Object>} The parsed JSON data.
 */
async function fetchData(filePath) {
    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Could not fetch data from ${filePath}:`, error);
        return null; // Return null on error
    }
}

/**
 * Populates the dashboard with data from the JSON files.
 * This function is now dynamic and relies on data from the JSON files.
 */
async function populateDashboard() {
    // Fetch data for all sections
    const speakerData = await fetchData('static/speaker_feedback.json');
    const teamData = await fetchData('static/team_summary.json');
    const judgeData = await fetchData('static/judge_insights.json');
    const motionData = await fetchData('static/motion_data.json');

    // Update the dashboard with the counts from the fetched data
    if (speakerData) {
        document.getElementById('total-speakers').textContent = speakerData.speakers.length;
        populateSpeakers(speakerData.speakers);
    }
    if (teamData) {
        document.getElementById('total-teams').textContent = teamData.teams.length;
        populateTeams(teamData.teams);
    }
    if (judgeData) {
        document.getElementById('total-judges').textContent = judgeData.judges.length;
        populateJudges(judgeData.judges);
    }
    if (motionData) {
        document.getElementById('total-motions').textContent = motionData.motions.length;
        populateMotions(motionData.motions);
    }
}

/**
 * Populates the 'Speakers' section with data.
 * @param {Array<Object>} speakers The array of speaker data.
 */
function populateSpeakers(speakers) {
    const speakerSelect = document.getElementById('speaker-select');
    speakerSelect.innerHTML = '<option value="">Choose a speaker...</option>';
    
    speakers.forEach(speaker => {
        const option = document.createElement('option');
        option.value = speaker.name;
        option.textContent = speaker.name;
        speakerSelect.appendChild(option);
    });

    speakerSelect.addEventListener('change', (event) => {
        const selectedSpeakerName = event.target.value;
        const selectedSpeaker = speakers.find(s => s.name === selectedSpeakerName);
        const displayArea = document.getElementById('speaker-feedback-display');
        
        if (selectedSpeaker) {
            displayArea.innerHTML = `
                <div class="card mt-4 p-4 fade-in">
                    <h5 class="card-title">${selectedSpeaker.name}</h5>
                    <div class="d-flex align-items-center mb-3">
                        <span class="speaker-score me-3">${selectedSpeaker.score}</span>
                        <div class="progress flex-grow-1" style="height: 10px;">
                            <div class="progress-bar" role="progressbar" style="width: ${selectedSpeaker.score * 10}%; background: linear-gradient(135deg, #11998e, #38ef7d);"></div>
                        </div>
                    </div>
                    <p class="card-text">${selectedSpeaker.feedback}</p>
                </div>
            `;
        } else {
            displayArea.innerHTML = `<p class="text-muted text-center mt-4">Please select a speaker to view their feedback.</p>`;
        }
    });
}

/**
 * Populates the 'Teams' section with data.
 * @param {Array<Object>} teams The array of team data.
 */
function populateTeams(teams) {
    const teamsContent = document.getElementById('teams-content');
    teamsContent.innerHTML = '';
    teams.forEach(team => {
        const teamHtml = `
            <div class="team-section fade-in">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h5>${team.name}</h5>
                    <span class="fw-bold">${team.score} points</span>
                </div>
                <div class="progress" style="height: 15px;">
                    <div class="progress-bar" role="progressbar" style="width: ${team.score}%; background-color: ${team.color};"></div>
                </div>
            </div>
        `;
        teamsContent.innerHTML += teamHtml;
    });
}

/**
 * Populates the 'Judges' section with data.
 * @param {Array<Object>} judges The array of judge data.
 */
function populateJudges(judges) {
    const judgesContent = document.getElementById('judges-content');
    judgesContent.innerHTML = '';
    judges.forEach(judge => {
        const judgeHtml = `
            <div class="judge-card p-4 mb-3 fade-in">
                <h5>${judge.name} <span class="badge rounded-pill bg-info">${judge.style}</span></h5>
                <p><strong>Bias Prediction:</strong> ${judge.bias}</p>
                <p><strong>AI Insight:</strong> ${judge.insights}</p>
            </div>
        `;
        judgesContent.innerHTML += judgeHtml;
    });
}

/**
 * Populates the 'Motions' section with data.
 * @param {Array<Object>} motions The array of motion data.
 */
function populateMotions(motions) {
    const motionsContent = document.getElementById('motions-content');
    motionsContent.innerHTML = '';
    motions.forEach(motion => {
        const motionHtml = `
            <div class="motion-card p-4 mb-3 fade-in">
                <div class="d-flex justify-content-between align-items-center">
                    <h5 class="motion-text">${motion.title}</h5>
                    <span class="badge rounded-pill bg-secondary">${motion.challenge}</span>
                </div>
                <p class="mb-2"><strong>Popularity:</strong> ${motion.popularity}%</p>
                <div class="progress" style="height: 10px;">
                    <div class="progress-bar" role="progressbar" style="width: ${motion.popularity}%; background: linear-gradient(to right, #667eea, #764ba2);"></div>
                </div>
            </div>
        `;
        motionsContent.innerHTML += motionHtml;
    });
}

// Initial setup when the page loads
document.addEventListener('DOMContentLoaded', () => {
    showSection('dashboard');
    // Call the main function to fetch all data and populate the dashboard
    populateDashboard();
});
