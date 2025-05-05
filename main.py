from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
VERIFIED_USERS_FILE = 'verified_users.json'

# Ensure the JSON file exists
if not os.path.exists(VERIFIED_USERS_FILE):
    with open(VERIFIED_USERS_FILE, 'w') as f:
        json.dump({}, f, indent=2)

# Helper functions
def load_verified_users():
    with open(VERIFIED_USERS_FILE, 'r') as f:
        return json.load(f)

def save_verified_users(data):
    with open(VERIFIED_USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    roblox_id = data.get("roblox_id")
    roblox_username = data.get("roblox_username")

    if not roblox_id or not roblox_username:
        return jsonify({"error": "Missing roblox_id or roblox_username"}), 400

    users = load_verified_users()
    users[roblox_id] = {"roblox_username": roblox_username}
    save_verified_users(users)

    return jsonify({"verified": True, "roblox_username": roblox_username}), 200

@app.route('/unverify', methods=['POST'])
def unverify():
    data = request.get_json()
    roblox_id = data.get("roblox_id")

    if not roblox_id:
        return jsonify({"error": "Missing roblox_id"}), 400

    users = load_verified_users()
    if roblox_id in users:
        del users[roblox_id]
        save_verified_users(users)
        return jsonify({"verified": False}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/is_verified', methods=['GET'])
def is_verified():
    roblox_id = request.args.get("roblox_id")
    users = load_verified_users()
    user = users.get(roblox_id)
    return jsonify({
        "verified": bool(user),
        "roblox_username": user.get("roblox_username") if user else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
