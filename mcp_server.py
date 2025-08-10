from flask import Flask, request, jsonify, render_template_string
import time, os, json, uuid

app = Flask(__name__)

USAGE_FILE = "mcp_usage.json"
if not os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump({"calls": [], "counts": {}}, f)

# API key settings
# Set environment variable MCP_API_KEY to a secure value before running.
DEFAULT_API_KEY = "testkey123"  # change this for production / demo
API_KEY = os.environ.get("MCP_API_KEY", DEFAULT_API_KEY)

def load_usage():
    with open(USAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_usage(data):
    with open(USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "ts": int(time.time())})

def require_api_key(req):
    header = req.headers.get("X-API-KEY", "")
    return header == API_KEY

@app.route("/invoke", methods=["POST"])
def invoke():
    # protect with API key
    if not require_api_key(request):
        return jsonify({"ok": False, "error": "invalid api key"}), 401

    data = request.json or {}
    tool = data.get("tool", "q_intelli")
    action = data.get("action", "advice")
    payload = data.get("payload", {})

    usage = load_usage()
    usage["calls"].append({"ts": int(time.time()), "tool": tool, "action": action})
    usage["counts"][tool] = usage["counts"].get(tool, 0) + 1
    save_usage(usage)

    if action == "reserve":
        token = str(uuid.uuid4())[:8].upper()
        eta_min = int(payload.get("eta_min", 15))
        return jsonify({"ok": True, "type": "reservation", "token": token, "eta_min": eta_min})
    elif action == "advice":
        domain = payload.get("domain", "general")
        suggestions = {
            "hospital": "If urgent: use emergency gate or call reception; else book online.",
            "bank": "Use ATM/online banking or VIP counters where available.",
            "train": "Check next trains and ask staff for a faster option.",
            "traffic": "Try alternate routes or call emergency services if needed.",
        }
        return jsonify({"ok": True, "type": "advice", "advice": suggestions.get(domain, "Try booking or rescheduling.")})
    else:
        return jsonify({"ok": False, "error": "unknown action"}), 400

LEADER_HTML = """
<html><head><title>MCP Tool Leaderboard</title></head><body>
<h2>MCP Usage Leaderboard</h2>
<table border="1" cellpadding="8">
<tr><th>Tool</th><th>Calls</th></tr>
{% for t,c in counts.items() %}
<tr><td>{{t}}</td><td>{{c}}</td></tr>
{% endfor %}
</table>
<p>Recent calls (latest 10):</p>
<pre>{{calls}}</pre>
</body></html>
"""

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    usage = load_usage()
    counts = usage.get("counts", {})
    calls = usage.get("calls", [])[-10:]
    return render_template_string(LEADER_HTML, counts=counts, calls=json.dumps(calls, indent=2))

@app.route("/", methods=["GET"])
def index():
    return jsonify({"service":"mcp-mock","endpoints":["/health","/invoke (api-key protected)","/leaderboard"]})

if __name__ == "__main__":
    # Run on 8080 (ngrok friendly). To change API key for demo:
    # Windows (PowerShell): $env:MCP_API_KEY = 'mysecretkey'; python mcp_server.py
    print("Using API_KEY:", API_KEY)
    app.run(host="0.0.0.0", port=8080, debug=True)
