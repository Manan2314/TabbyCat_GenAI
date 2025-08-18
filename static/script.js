async function sendRequest(endpoint, inputId, outputId) {
    const inputText = document.getElementById(inputId).value;
    const outputBox = document.getElementById(outputId);

    // Show loading
    outputBox.innerHTML = "<em>Analyzing... please wait</em>";

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: inputText })
        });

        const data = await response.json();

        if (data.error) {
            outputBox.innerHTML = `<span style="color:red;">Error: ${data.error}</span>`;
        } else {
            outputBox.innerHTML = `<strong>${data.insight}</strong>`;
        }
    } catch (error) {
        outputBox.innerHTML = `<span style="color:red;">Error: ${error.message}</span>`;
    }
}

// Hooking buttons to functions
document.getElementById("teamBtn").addEventListener("click", () => {
    sendRequest("/team-analysis", "teamInput", "teamOutput");
});

document.getElementById("speakerBtn").addEventListener("click", () => {
    sendRequest("/speaker-analysis", "speakerInput", "speakerOutput");
});

document.getElementById("judgeBtn").addEventListener("click", () => {
    sendRequest("/judge-analysis", "judgeInput", "judgeOutput");
});

document.getElementById("motionBtn").addEventListener("click", () => {
    sendRequest("/motion-analysis", "motionInput", "motionOutput");
});
