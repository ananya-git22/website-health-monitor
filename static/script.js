
// Get website monitoring data from Flask
async function loadWebsites() {

    const checkButton = document.getElementById("checkBtn");

    try {

        const response = await fetch("/api/websites");

        if (!response.ok) {
            throw new Error("Failed to fetch website data");
        }

        const data = await response.json();

        // Update statistics
        document.getElementById("total").textContent = data.total;

        document.getElementById("online").textContent = data.online;

        document.getElementById("offline").textContent = data.offline;

        document.getElementById("average").textContent =
            data.average_response + " ms";

        // Update website table
        const table = document.getElementById("websiteTable");

        table.innerHTML = "";

        data.websites.forEach(site => {

            const row = document.createElement("tr");

            const statusClass =
                site.status === "ONLINE" ? "online" : "offline";

            row.innerHTML = `
                <td>
                    <div class="website-name">${escapeHTML(site.name)}</div>
                    <div class="website-url">${escapeHTML(site.url)}</div>
                </td>

                <td>
                    <span class="status ${statusClass}">
                        ${site.status}
                    </span>
                </td>

                <td>${site.status_code}</td>

                <td>${site.response_time} ms</td>

                <td>${site.last_checked}</td>
            `;

            table.appendChild(row);

        });

        document.getElementById("lastUpdated").textContent =
            "Last dashboard update: " + new Date().toLocaleTimeString();

    } catch (error) {

        showMessage("Unable to load website data. Please try again.", true);

        console.error(error);

    }
}


// Escape website information before inserting it into HTML
function escapeHTML(value) {

    return String(value).replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[character]);

}


// Show messages
function showMessage(message, isError = false) {

    const messageElement = document.getElementById("message");

    messageElement.textContent = message;

    messageElement.style.color = isError ? "#f87171" : "#4ade80";

}


// Add a new website
async function addWebsite() {

    const input = document.getElementById("websiteInput");

    const addButton = document.getElementById("addBtn");

    const url = input.value.trim();

    if (!url) {
        showMessage("Please enter a website URL.", true);
        return;
    }

    addButton.disabled = true;

    try {

        const response = await fetch("/api/add", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to add website");
        }

        input.value = "";

        showMessage("Website added successfully!");

        // Immediately refresh website data
        await loadWebsites();

    } catch (error) {

        showMessage(error.message, true);

    } finally {

        addButton.disabled = false;

    }

}


// Manually check all websites
async function checkNow() {

    const button = document.getElementById("checkBtn");

    button.disabled = true;

    button.textContent = "Checking...";

    try {

        await loadWebsites();

    } finally {

        button.disabled = false;

        button.textContent = "↻ Check Now";

    }

}


// Connect buttons
document.getElementById("addBtn").addEventListener(
    "click",
    addWebsite
);

document.getElementById("checkBtn").addEventListener(
    "click",
    checkNow
);


// Automatically refresh every 30 seconds
loadWebsites();

setInterval(loadWebsites, 30000);
