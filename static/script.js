// This script now fetches data from the Flask API routes instead of static JSON files.

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
 * Fetches data from a Flask API endpoint and returns it.
 * @param {string} endpoint The API endpoint (e.g., "/speakers").
 * @returns {Promise<Object>} The parsed JSON data.
 */
async function fetchData(endpoint) {
    try {
        const response = await fetch(endpoint);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} from ${endpoint}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Could not fetch data from ${endpoint}:`, error);
        return null; // Return null on error
    }
}

/**
 * Populates the dashboard with data from the Flask API endpoints.
 */
async function populateDashboard() {
    const loadingMessage = document.getElementById('loading-message');
    loadingMessage.textContent = 'Loading dashboard data...';
    
    // Fetch from Flask endpoints
    const fetchPromises = [
        fetchData('/speakers'),
        fetchData('/teams'),
        fetchData('/judges'),
        fetchData('/motions')
    ];

    try {
        const [speakerData, teamData, judgeData, motionData] = await Promise.all(fetchPromises);
        
        loadingMessage.style.display = 'none';

        // ✅ Speakers (Flask returns a list)
        if (speakerData && Array.isArray(speakerData)) {
            document.getElementById('total-speakers').textContent = speakerData.length;
            populateSpeakers(speakerData);
        } else {
            console.error("Speaker data not found or invalid.");
        }

        // ✅ Teams (Flask returns a dict, not wrapped in {teams: [...]})
        if (teamData) {
            document.getElementById('total-teams').textContent = 1;
            populateTeams([teamData]);
        } else {
            console.error("Team data not found or invalid.");
        }

        // ✅ Judges (Flask returns a dict, not wrapped in {judges: [...]})
        if (judgeData) {
            document.getElementById('total-judges').textContent = 1;
            populateJudges([judgeData]);
        } else {
            console.error("Judge data not found or invalid.");
        }
        
        // ✅ Motions (Flask returns a list)
        if (motionData && Array.isArray(motionData)) {
            document.getElementById('total-motions').textContent = motionData.length;
            populateMotions(motionData);
        } else {
            console.error("Motion data not found or invalid.");
        }
    } catch (error) {
        console.error("An error occurred during data fetching:", error);
        loadingMessage.textContent = 'Failed to load data. Please check the console for more details.';
    }
}

/**
 * Populates the 'Speakers' section with data.
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
                    <p class="text-info"><strong>AI Insight:</strong> ${selectedSpeaker.ai_insights}</p>
                </div>
            `;
        } else {
            displayArea.innerHTML = `<p class="text-muted text-center mt-4">Please select a speaker to view their feedback.</p>`;
        }
    });
}

/**
 * Populates the 'Teams' section with data.
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
                <p class="text-info"><strong>AI Insight:</strong> ${team.ai_insights}</p>
                <div class="progress" style="height: 15px;">
                    <div class="progress-bar" role="progressbar" style="width: ${team.score}%; background-color: ${team.color || '#007bff'};"></div>
                </div>
            </div>
        `;
        teamsContent.innerHTML += teamHtml;
    });
}

/**
 * Populates the 'Judges' section with data.
 */
function populateJudges(judges) {
    const judgesContent = document.getElementById('judges-content');
    judgesContent.innerHTML = '';
    judges.forEach(judge => {
        const judgeHtml = `
            <div class="judge-card p-4 mb-3 fade-in">
                <h5>${judge.name || "Judge"} <span class="badge rounded-pill bg-info">${judge.style || "N/A"}</span></h5>
                <p><strong>Bias Prediction:</strong> ${judge.bias || "Unknown"}</p>
                <p><strong>AI Insight:</strong> ${judge.ai_insights || "No insights"}</p>
            </div>
        `;
        judgesContent.innerHTML += judgeHtml;
    });
}

/**
 * Populates the 'Motions' section with data.
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
    populateDashboard();
});
