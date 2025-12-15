import uuid
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Create Users Table
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                 (id TEXT PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
    # Create Feedbacks Table
    # Dropping table to apply new schema for development
    cur.execute('''CREATE TABLE IF NOT EXISTS feedbacks
                 (id TEXT PRIMARY KEY, feedback TEXT, user_id TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  sentiment TEXT,
                  cleaned_text TEXT,
                  processed_text TEXT,
                  confidence FLOAT,
                  has_negation BOOLEAN,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    role = data.get('role')
    user_id = str(uuid.uuid4())
    
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        if role == 'anonymous':
            cur.execute("INSERT INTO users (id, role) VALUES (%s, %s)", (user_id, 'anonymous'))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"user_id": user_id, "role": "anonymous"}), 201
        
        elif role == 'admin':
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                cur.close()
                conn.close()
                return jsonify({"error": "Username and password required for admin"}), 400
                
            # Check if admin exists
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user:
                cur.close()
                conn.close()
                return jsonify({"error": "Admin already exists"}), 400
                
            cur.execute("INSERT INTO users (id, username, password, role) VALUES (%s, %s, %s, %s)",
                      (user_id, username, password, 'admin'))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"message": "Admin created successfully", "username": username}), 201
        
        else:
            cur.close()
            conn.close()
            return jsonify({"error": "Invalid role. Must be 'admin' or 'anonymous'"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
        
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if user:
            return jsonify({"message": "Login successful"}), 200
        
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import requests
import datetime

ML_API_URL = os.getenv('ML_API_URL', 'http://localhost:5001/predict')

@app.route('/api/feedbacks', methods=['POST'])
def create_feedback():
    data = request.get_json()
    feedback_text = data.get('feedback')
    user_id = data.get('user_id')
    
    if not feedback_text or not user_id:
        return jsonify({"error": "Missing feedback or user_id"}), 400
    
    feedback_id = str(uuid.uuid4())
    created_at = datetime.datetime.now()
    
    # Call ML API
    sentiment = None
    cleaned_text = None
    processed_text = None
    confidence = None
    has_negation = None

    try:
        # Assuming ML API runs on port 5001 or specified in ENV
        # And accepts 'text' for prediction
        ml_response = requests.post(ML_API_URL, json={"text": feedback_text}, timeout=5)
        if ml_response.status_code == 200:
            result = ml_response.json()
            # Expected response: { "sentiment": ..., "cleaned_text": ..., "processed_text": ..., "confidence": ..., "has_negation": ... }
            sentiment = result.get('sentiment')
            cleaned_text = result.get('cleaned_text')
            processed_text = result.get('processed_text')
            confidence = result.get('confidence')
            has_negation = result.get('has_negation')
        else:
            print(f"ML API Error: {ml_response.status_code}")
    except Exception as e:
        print(f"ML Service Exception: {str(e)}")

    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            INSERT INTO feedbacks 
            (id, feedback, user_id, created_at, sentiment, cleaned_text, processed_text, confidence, has_negation) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (feedback_id, feedback_text, user_id, created_at, sentiment, cleaned_text, processed_text, confidence, has_negation))
        conn.commit()
        
        # Verify and return created obj
        cur.execute("SELECT * FROM feedbacks WHERE id = %s", (feedback_id,))
        created = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(created), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM feedbacks")
        feedbacks = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(feedbacks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedbacks/<feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM feedbacks WHERE id = %s", (feedback_id,))
        feedback = cur.fetchone()
        cur.close()
        conn.close()
        
        if not feedback:
            return jsonify({"error": "Feedback not found"}), 404
        return jsonify(feedback), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedbacks/<feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM feedbacks WHERE id = %s", (feedback_id,))
        feedback = cur.fetchone()
        if not feedback:
            cur.close()
            conn.close()
            return jsonify({"error": "Feedback not found"}), 404
        
        # Update fields if provided
        query = "UPDATE feedbacks SET "
        params = []
        updates = []
        
        if 'feedback' in data:
            updates.append("feedback = %s")
            params.append(data['feedback'])
            
        if not updates:
            cur.close()
            conn.close()
            return jsonify(feedback), 200
            
        query += ", ".join(updates) + " WHERE id = %s"
        params.append(feedback_id)
        
        cur.execute(query, tuple(params))
        conn.commit()
        
        cur.execute("SELECT * FROM feedbacks WHERE id = %s", (feedback_id,))
        updated_feedback = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(updated_feedback), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedbacks/<feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM feedbacks WHERE id = %s", (feedback_id,))
        conn.commit()
        deleted_count = cur.rowcount
        cur.close()
        conn.close()
        
        if deleted_count == 0:
            return jsonify({"error": "Feedback not found"}), 404
            
        return jsonify({"message": "Feedback deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"Database init failed: {e}")
    app.run(debug=True, host='0.0.0.0', port=5000)
