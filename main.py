from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for Roblox HTTP requests)

# Temporary in-memory storage
verified_users = {}

@app.route('/')
def home():
    return "✅ Roblox Verification API is running!"

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    roblox_id = data.get("roblox_id")
    if not roblox_id:
        return jsonify({"error": "Missing roblox_id"}), 400

    verified_users[roblox_id] = True
    return jsonify({"message": "Verified!"})

@app.route('/is_verified', methods=['GET'])
def is_verified():
    roblox_id = request.args.get("roblox_id")
    if not roblox_id:
        return jsonify({"error": "Missing roblox_id"}), 400

    return jsonify({"verified": verified_users.get(roblox_id, False)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
