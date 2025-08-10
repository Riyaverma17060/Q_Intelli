import sys
import requests
import json

def check_invoke_endpoint(base_url):
    """
    Check if the server accepts requests at /invoke or /invoke/ endpoint.
    Returns the corrected URL or raises an exception.
    """
    possible_urls = [base_url.rstrip('/') + '/invoke', base_url.rstrip('/') + '/invoke/']

    for url in possible_urls:
        try:
            # Use OPTIONS to check availability without side effects
            response = requests.options(url, timeout=3)
            if response.status_code < 400:
                return url
            # Accept 405 Method Not Allowed as endpoint exists but method disallowed
            if response.status_code == 405:
                return url
        except requests.RequestException:
            pass

    raise RuntimeError(
        f"Server not responding correctly at /invoke endpoint. Tried URLs:\n"
        + "\n".join(possible_urls)
        + "\nPlease check your server URL and endpoint path."
    )

if len(sys.argv) != 5:
    print("Usage: python q_client.py <server_url> <eta> <api_key> <tool_name>")
    print("Example: python q_client.py http://localhost:8080/invoke 10 testkey123 my_tool")
    sys.exit(1)

server_url = sys.argv[1]
eta = sys.argv[2]
api_key = sys.argv[3]
tool_name = sys.argv[4]

try:
    invoke_url = check_invoke_endpoint(server_url)
    print(f"[DEBUG] Using invoke endpoint URL: {invoke_url}")
except RuntimeError as e:
    print("ERROR:", e)
    sys.exit(1)

payload = {
    "tool": tool_name,
    "action": "reserve",
    "payload": {
        "eta_min": eta
    }
}

headers = {
    "X-API-KEY": api_key,
    "Content-Type": "application/json"
}

print(f"[DEBUG] Sending POST request to: {invoke_url}")
print(f"[DEBUG] Payload: {json.dumps(payload)}")
print(f"[DEBUG] Headers: {headers}")

try:
    response = requests.post(invoke_url, json=payload, headers=headers)
except requests.RequestException as e:
    print(f"ERROR: Failed to send POST request: {e}")
    sys.exit(1)

print(f"[DEBUG] HTTP Status: {response.status_code}")
print(f"[DEBUG] Response text: {response.text}")

if response.status_code == 404:
    print("ERROR: 404 Not Found - The server endpoint was not found. Please verify your server URL and endpoint path.")
    sys.exit(1)
elif response.status_code >= 400:
    print(f"ERROR: Server returned HTTP status {response.status_code}. Response:\n{response.text}")
    sys.exit(1)
else:
    print("Request successful.")
