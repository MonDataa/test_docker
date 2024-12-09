from flask import Flask, request, jsonify
import hashlib
import sqlite3

app = Flask(__name__)

# Database initialization
DB_FILE = '/data/checksums.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checksums (
            id INTEGER PRIMARY KEY,
            input TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            checksum TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/checksum', methods=['POST'])
def calculate_checksum():
    data = request.json
    input_text = data.get('input')
    algorithm = data.get('algorithm', 'sha256')

    # Calculate checksum
    if algorithm not in hashlib.algorithms_available:
        return jsonify({'error': 'Algorithm not supported'}), 400

    checksum = hashlib.new(algorithm, input_text.encode()).hexdigest()

    # Save to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO checksums (input, algorithm, checksum) VALUES (?, ?, ?)",
                   (input_text, algorithm, checksum))
    conn.commit()
    conn.close()

    return jsonify({'input': input_text, 'algorithm': algorithm, 'checksum': checksum})

@app.route('/checksums', methods=['GET'])
def list_checksums():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT input, algorithm, checksum FROM checksums")
    results = cursor.fetchall()
    conn.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
