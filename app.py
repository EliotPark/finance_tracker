
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
    # If we added a new field (like "recurring") after someone already has a data.json,
    # this makes sure their file doesn't break — it just fills in the missing key as empty
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
    # The frontend always sends the entire state at once — we just overwrite the file.
    # There's no partial update; whoever saves last wins.
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
    # Serves tracker.html, analytics.html, style.css, etc. straight from the project folder —
    # no separate static directory needed
    return send_from_directory('.', path)


if __name__ == '__main__':
    print()
    print('  Finance Tracker running at http://localhost:5000')
    print('  Press Ctrl+C to stop.')
    print()
    app.run(debug=False, port=5000)
