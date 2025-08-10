from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

API_KEY = "supersecret123"  # Change this to your actual API key

def generate_token(length=8):
    """Generate an uppercase alphanumeric token (letters + numbers)."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

@app.route('/invoke', methods=['POST'])
@app.route('/invoke/invoke', methods=['POST'])
def invoke():
    # API key validation
    api_key = request.headers.get('X-API-KEY')
    if api_key != API_KEY:
        return jsonify({"ok": False, "error": "Invalid API key"}), 403

    data = request.get_json()

    # Basic payload validation
    if not data or "tool" not in data or "action" not in data:
        return jsonify({"ok": False, "error": "Invalid payload"}), 400

    tool = data["tool"]
    action = data["action"]
    payload = data.get("payload", {})

    # Simulate reservation action
    if action == "reserve":
        eta_min = int(payload.get("eta_min", 0))
        token = generate_token()
        return jsonify({
            "eta_min": eta_min,
            "ok": True,
            "token": token,
            "type": "reservation"
        })

    return jsonify({"ok": False, "error": "Unknown action"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
