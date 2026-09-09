const form = document.getElementById("requestForm");

const decisionBox = document.getElementById("decisionBox");

const resultTool = document.getElementById("resultTool");
const resultRisk = document.getElementById("resultRisk");
const resultSource = document.getElementById("resultSource");

const logs = document.getElementById("logs");

let total = 24;
let allowed = 16;
let denied = 5;
let escalated = 3;


form.addEventListener("submit", function(event) {

    event.preventDefault();

    const request =
        document.getElementById("request").value.trim();

    const tool =
        document.getElementById("tool").value;

    const risk =
        document.getElementById("risk").value;

    const source =
        document.getElementById("source").value;


    if (!request) {
        alert("Please enter an agent request.");
        return;
    }


    /*
       SIMPLE DEMO AUTHORIZATION ENGINE

       In the real project this logic will be
       handled by your Python/Java backend.
    */

    let decision;
    let reason;
    let icon;


    // High-risk actions from untrusted sources
    if (
        (source === "Website" ||
         source === "Document" ||
         source === "Email" ||
         source === "Tool")
        &&
        (risk === "High" || risk === "Critical")
    ) {

        decision = "DENY";

        icon = "✕";

        reason =
            "The requested action originates from an untrusted source and has high security impact.";

    }


    // Critical actions require human approval
    else if (risk === "Critical") {

        decision = "ESCALATE";

        icon = "!";

        reason =
            "This is a critical operation. User authorization is required before execution.";

    }


    // High-risk API or command operation
    else if (
        risk === "High" &&
        (tool === "Command" || tool === "API")
    ) {

        decision = "ESCALATE";

        icon = "!";

        reason =
            "High-impact tool operation requires additional authorization.";

    }


    // Normal user requests
    else {

        decision = "ALLOW";

        icon = "✓";

        reason =
            "The action is within the permitted scope and no significant authorization conflict was detected.";

    }


    showDecision(
        decision,
        reason,
        icon,
        tool,
        risk,
        source
    );


    addLog(
        request,
        tool,
        risk,
        source,
        decision
    );


    updateStatistics(decision);

});


function showDecision(
    decision,
    reason,
    icon,
    tool,
    risk,
    source
) {

    decisionBox.className =
        "decision " + decision.toLowerCase();

    decisionBox.innerHTML = `

        <div class="decision-icon">
            ${icon}
        </div>

        <h2>${decision}</h2>

        <p>${reason}</p>

    `;


    resultTool.textContent = tool;
    resultRisk.textContent = risk;
    resultSource.textContent = source;
}


function addLog(
    request,
    tool,
    risk,
    source,
    decision
) {

    const time =
        new Date().toLocaleTimeString();


    const row =
        document.createElement("tr");


    row.innerHTML = `

        <td>${time}</td>

        <td>${escapeHTML(request)}</td>

        <td>${tool}</td>

        <td>
            <span class="risk ${risk.toLowerCase()}">
                ${risk}
            </span>
        </td>

        <td>${source}</td>

        <td>
            <span class="decision-tag ${decision.toLowerCase()}">
                ${decision}
            </span>
        </td>

    `;


    logs.prepend(row);
}


function updateStatistics(decision) {

    total++;

    if (decision === "ALLOW") {
        allowed++;
    }

    if (decision === "DENY") {
        denied++;
    }

    if (decision === "ESCALATE") {
        escalated++;
    }


    document.getElementById(
        "totalRequests"
    ).textContent = total;

    document.getElementById(
        "allowedCount"
    ).textContent = allowed;

    document.getElementById(
        "deniedCount"
    ).textContent = denied;

    document.getElementById(
        "escalatedCount"
    ).textContent = escalated;
}


function clearLogs() {

    logs.innerHTML = "";

}


function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}