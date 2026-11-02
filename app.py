
from flask import Flask, render_template, jsonify, request
import requests
import time
from datetime import datetime

app = Flask(__name__)

# Default websites
websites = [
    {"name": "Google", "url": "https://google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Wikipedia", "url": "https://wikipedia.org"},
    {"name": "Microsoft", "url": "https://microsoft.com"}
]


# Check website health
def check_website(website):

    start_time = time.time()

    try:
        response = requests.get(
            website["url"],
            timeout=8,
            headers={"User-Agent": "WebsiteHealthMonitor/1.0"}
        )

        response_time = round(
            (time.time() - start_time) * 1000, 2
        )

        status_code = response.status_code

        return {
            "name": website["name"],
            "url": website["url"],
            "status": "ONLINE" if status_code < 400 else "OFFLINE",
            "status_code": status_code,
            "response_time": response_time,
            "last_checked": datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )
        }

    except requests.RequestException:

        response_time = round(
            (time.time() - start_time) * 1000, 2
        )

        return {
            "name": website["name"],
            "url": website["url"],
            "status": "OFFLINE",
            "status_code": "N/A",
            "response_time": response_time,
            "last_checked": datetime.now().strftime(
                "%d-%m-%Y %I:%M:%S %p"
            )
        }


# Check all websites
def get_monitoring_data():

    results = [check_website(site) for site in websites]

    total = len(results)

    online = sum(
        1 for site in results
        if site["status"] == "ONLINE"
    )

    offline = total - online

    average_response = round(
        sum(site["response_time"] for site in results) / total, 2
    ) if total else 0

    return {
        "websites": results,
        "total": total,
        "online": online,
        "offline": offline,
        "average_response": average_response
    }


# Main dashboard
@app.route("/")
def home():
    return render_template("index.html")


# API to get website monitoring results
@app.route("/api/websites")
def api_websites():
    return jsonify(get_monitoring_data())


# API to add a website
@app.route("/api/add", methods=["POST"])
def add_website():

    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Enter a valid HTTP or HTTPS URL"}), 400

    if any(site["url"] == url for site in websites):
        return jsonify({"error": "Website already exists"}), 400

    name = url.split("//", 1)[1].split("/")[0]

    websites.append({
        "name": name,
        "url": url
    })

    return jsonify({
        "message": "Website added successfully"
    }), 201


# Start application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
