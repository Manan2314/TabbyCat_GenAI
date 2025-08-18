// TabbyCat AI - Original JavaScript Recreation
console.log("TabbyCat AI initialized");

// Global variables
let speakersData = [];
let teamsData = {};
let judgesData = {};
let motionsData = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log("Loading dashboard data...");
    loadDashboardData();
    showSection('dashboard');
});

// Load all data for dashboard
async function loadDashboardData() {
    try {
        // Load all data simultaneously
        const [speakers, teams, judges, motions] = await Promise.all([
            fetch('/speakers').then(res => res.json()),
            fetch('/teams').then(res => res.json()),
            fetch('/judges').then(res => res.json()),
            fetch('/motions').then(res => res.json())
        ]);

        speakersData = speakers;
        teamsData = teams;
        judgesData = judges;
        motionsData = motions;

        updateDashboardStats();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

// Update dashboard statistics
function updateDashboardStats() {
    // Update speaker count
    const totalSpeakers = Array.isArray(speakersData) ? speakersData.length : 0;
    document.getElementById('total-speakers').textContent = totalSpeakers;

    // Update team count
    const totalTeams = teamsData && teamsData.members ? 1 : 0;
    document.getElementById('total-teams').textContent = totalTeams;

    // Update judge count
    const totalJudges = judgesData ? 1 : 0;
    document.getElementById('total-judges').textContent = totalJudges;

    // Update motion count
    const totalMotions = Array.isArray(motionsData) ? motionsData.length : 0;
    document.getElementById('total-motions').textContent = totalMotions;
}

// Show specific section
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    // Show selected section
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.style.display = 'block';
        targetSection.classList.add('fade-in');
    }

    // Update navigation
    updateNavigation(sectionName);

    // Load section-specific content
    switch(sectionName) {
        case 'speakers':
            loadSpeakersContent();
            break;
        case 'teams':
            loadTeamsContent();
            break;
        case 'judges':
            loadJudgesContent();
            break;
        case 'motions':
            loadMotionsContent();
            break;
    }
}

// Update navigation active state
function updateNavigation(activeSection) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(activeSection)) {
            link.classList.add('active');
        }
    });
}

// Load speakers content
function loadSpeakersContent() {
    const selectElement = document.getElementById('speaker-select');
    if (!Array.isArray(speakersData) || speakersData.length === 0) {
        selectElement.innerHTML = '<option value="">No speakers available</option>';
        return;
    }

    // Populate dropdown with speaker names
    let options = '<option value="">Choose a speaker...</option>';
    speakersData.forEach((speaker, index) => {
        options += `<option value="${index}">${speaker.name || 'Unknown Speaker'}</option>`;
    });
    selectElement.innerHTML = options;
}

// Show individual speaker feedback
function showSpeakerFeedback() {
    const selectElement = document.getElementById('speaker-select');
    const selectedIndex = selectElement.value;
    const displayContainer = document.getElementById('speaker-feedback-display');

    if (!selectedIndex || selectedIndex === '') {
        displayContainer.innerHTML = '<p class="text-muted text-center">Please select a speaker to view their feedback.</p>';
        return;
    }

    const speaker = speakersData[parseInt(selectedIndex)];
    if (!speaker) {
        displayContainer.innerHTML = '<p class="text-danger text-center">Speaker data not found.</p>';
        return;
    }

    const aiInsights = speaker.ai_insights || {};
    const generalFeedback = aiInsights.general_feedback || 'AI analysis in progress...';
    const improvementAdvice = aiInsights.improvement_advice || 'Generating improvement suggestions...';

    const html = `
        <div class="card">
            <div class="card-header">
                <h4 class="mb-0">${speaker.name || 'Unknown Speaker'}</h4>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <p><strong>Team:</strong> ${speaker.team || 'No Team'}</p>
                        <p><strong>Role:</strong> ${speaker.role || 'Speaker'}</p>
                        <p><strong>Round:</strong> ${speaker.round || 'N/A'}</p>
                    </div>
                    <div class="col-md-6 text-end">
                        <div class="speaker-score">${speaker.score || 'N/A'}</div>
                        <small class="text-muted">Score</small>
                    </div>
                </div>
                
                <hr>
                
                <div class="ai-insights">
                    <h6><i class="fas fa-brain me-2"></i>AI Performance Analysis</h6>
                    <div class="mb-3">
                        <strong>General Feedback:</strong>
                        <p>${generalFeedback}</p>
                    </div>
                    <div>
                        <strong>Improvement Advice:</strong>
                        <p>${improvementAdvice}</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    displayContainer.innerHTML = html;
}

// Load teams content
function loadTeamsContent() {
    const container = document.getElementById('teams-content');
    if (!teamsData || !teamsData.team_name) {
        container.innerHTML = '<p class="text-center">No team data available.</p>';
        return;
    }

    const aiInsights = teamsData.ai_insights || 'AI team analysis in progress...';
    
    let html = `
        <div class="team-section">
            <div class="row">
                <div class="col-lg-8">
                    <h3>${teamsData.team_name}</h3>
                    <p class="text-muted mb-3">Team Members: ${teamsData.members ? teamsData.members.join(', ') : 'No members listed'}</p>
                    
                    <div class="ai-insights mb-4">
                        <h6><i class="fas fa-brain me-2"></i>AI Team Analysis</h6>
                        <p>${aiInsights}</p>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0">Performance Overview</h6>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <span class="small text-muted">Average Performance</span>
                                <div class="performance-bar">
                                    <div class="performance-fill" style="width: 78%"></div>
                                </div>
                                <span class="small">78%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add rounds data if available
    if (teamsData.rounds && teamsData.rounds.length > 0) {
        html += '<div class="row">';
        teamsData.rounds.forEach(round => {
            html += `
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h6>${round.round || 'Round'}</h6>
                            <p class="mb-2">Average Score: <strong>${round.average_score || 'N/A'}</strong></p>
                            <p class="small text-muted">${round.team_feedback || 'No feedback available'}</p>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    }

    container.innerHTML = html;
}

// Load judges content
function loadJudgesContent() {
    const container = document.getElementById('judges-content');
    if (!judgesData || !judgesData.judge_name) {
        container.innerHTML = '<p class="text-center">No judge data available.</p>';
        return;
    }

    const aiInsights = judgesData.ai_insights || 'AI judge analysis in progress...';

    let html = `
        <div class="judge-card">
            <div class="row">
                <div class="col-lg-8">
                    <h3>${judgesData.judge_name}</h3>
                    <span class="judge-style-badge">${judgesData.judge_style || 'Style Unknown'}</span>
                    
                    <div class="mt-3">
                        <h6>Judging Insight</h6>
                        <p class="text-muted">${judgesData.overall_judging_insight || 'No insights available'}</p>
                    </div>
                    
                    <div class="ai-insights mt-3">
                        <h6><i class="fas fa-brain me-2"></i>AI Judge Pattern Analysis</h6>
                        <p>${aiInsights}</p>
                    </div>
                </div>
                <div class="col-lg-4">
                    <div class="card">
                        <div class="card-header">
                            <h6 class="mb-0">Judging Statistics</h6>
                        </div>
                        <div class="card-body">
                            <p class="mb-2">Rounds Judged: <strong>${judgesData.rounds ? judgesData.rounds.length : 0}</strong></p>
                            <p class="mb-0">Style: <strong>${judgesData.judge_style || 'Unknown'}</strong></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add rounds judged if available
    if (judgesData.rounds && judgesData.rounds.length > 0) {
        html += '<div class="row mt-4">';
        judgesData.rounds.forEach(round => {
            html += `
                <div class="col-md-6 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h6>${round.round || 'Round'}</h6>
                            <div class="small">
                                ${round.speakers_scored ? round.speakers_scored.map(s => 
                                    `<span class="badge bg-secondary me-1">${s.name}: ${s.score}</span>`
                                ).join('') : 'No speakers scored'}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';
    }

    container.innerHTML = html;
}

// Load motions content with predictions
function loadMotionsContent() {
    const container = document.getElementById('motions-content');
    if (!Array.isArray(motionsData) || motionsData.length === 0) {
        container.innerHTML = '<p class="text-center">No motion data available.</p>';
        return;
    }

    let html = '';
    motionsData.forEach((motion, index) => {
        // Generate random but realistic win probabilities for demonstration
        const govWinProb = Math.floor(Math.random() * 30) + 35; // 35-65%
        const oppWinProb = 100 - govWinProb;
        
        html += `
            <div class="card mb-4">
                <div class="card-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Motion ${index + 1}</h5>
                        <span class="badge bg-info">${motion.round || 'Round'}</span>
                    </div>
                </div>
                <div class="card-body">
                    <div class="motion-text mb-4">
                        <strong>Motion:</strong> ${motion.motion || 'Motion text not available'}
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <h6><i class="fas fa-chart-bar me-2"></i>Win Probability</h6>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>Government</span>
                                    <strong>${govWinProb}%</strong>
                                </div>
                                <div class="progress mb-2">
                                    <div class="progress-bar bg-success" style="width: ${govWinProb}%"></div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <div class="d-flex justify-content-between">
                                    <span>Opposition</span>
                                    <strong>${oppWinProb}%</strong>
                                </div>
                                <div class="progress">
                                    <div class="progress-bar bg-danger" style="width: ${oppWinProb}%"></div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="ai-insights">
                                <h6><i class="fas fa-brain me-2"></i>AI Complexity Analysis</h6>
                                <p><strong>Complexity Level:</strong> ${motion.complexity || 'Medium'}</p>
                                <p class="small">
                                    ${getComplexityAnalysis(motion.complexity, motion.motion)}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

// Generate complexity analysis based on motion
function getComplexityAnalysis(complexity, motionText) {
    const analyses = {
        'High': 'This motion requires deep knowledge of complex issues and sophisticated argumentation. Teams should focus on nuanced analysis and expert-level evidence.',
        'Medium': 'This motion balances accessibility with intellectual rigor. Teams can leverage both common knowledge and specialized insights.',
        'Low': 'This motion is accessible to most debaters and focuses on fundamental principles. Clear, logical argumentation will be key.',
        'Unknown': 'This motion presents moderate complexity. Teams should prepare for both principled and pragmatic arguments.'
    };
    
    return analyses[complexity] || analyses['Unknown'];
}

// Utility function to show loading state
function showLoading() {
    const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
    loadingModal.show();
    setTimeout(() => loadingModal.hide(), 2000);
}

// Add smooth scrolling for navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        showLoading();
    });
});
