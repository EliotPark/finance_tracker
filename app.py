
from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

DATA_FILE = 'data.json'
EMPTY_STATE = {
    "users": [],
    "expenses": [],
    "transactions": [],
    "recurring": [],
}


def load():
    if not os.path.exists(DATA_FILE):
        return dict({k: list(v) for k, v in EMPTY_STATE.items()})
    with open(DATA_FILE) as f:
        data = json.load(f)
    # Back-fill any keys added in later versions
    for key, default in EMPTY_STATE.items():
        if key not in data:
            data[key] = list(default)
    return data


def dump(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)



@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(load())


@app.route('/api/state', methods=['POST'])
def post_state():
    data = request.get_json(force=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'expected JSON object'}), 400
    dump(data)
    return jsonify({'ok': True})



@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)


if __name__ == '__main__':
    print()
    print('  Finance Tracker running at http://localhost:5000')
    print('  Press Ctrl+C to stop.')
    print()
    app.run(debug=False, port=5000)
