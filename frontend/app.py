import os
import requests
from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from datetime import datetime
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Backend API configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

# Helper function to check if user is admin
def is_admin():
    return session.get('is_admin', False)

# Helper function to get or create anonymous user
def get_anonymous_user():
    if 'anon_user_id' not in session:
        try:
            response = requests.post(f'{BACKEND_URL}/api/users/register', json={'role': 'anonymous'})
            if response.status_code == 201:
                data = response.json()
                session['anon_user_id'] = data['user_id']
            else:
                return None
        except Exception as e:
            print(f"Error creating anonymous user: {e}")
            return None
    return session.get('anon_user_id')

@app.route('/')
def index():
    return render_template('feedback.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        
        # Get or create anonymous user
        user_id = get_anonymous_user()
        
        if not user_id:
            return render_template('feedback.html', error='Failed to create user session')
        
        # Submit feedback to backend
        try:
            response = requests.post(
                f'{BACKEND_URL}/api/feedbacks',
                json={'feedback': feedback_text, 'user_id': user_id}
            )
            
            if response.status_code == 201:
                return render_template('feedback.html', success='Thank you for your feedback!')
            else:
                return render_template('feedback.html', error='Failed to submit feedback')
        except Exception as e:
            print(f"Error submitting feedback: {e}")
            return render_template('feedback.html', error='Connection error')
    
    return render_template('feedback.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            response = requests.post(
                f'{BACKEND_URL}/api/users/login',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                session['is_admin'] = True
                session['username'] = username
                return redirect(url_for('admin'))
            else:
                return render_template('login.html', error='Invalid credentials')
        except Exception as e:
            print(f"Login error: {e}")
            return render_template('login.html', error='Connection error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        
        try:
            response = requests.post(
                f'{BACKEND_URL}/api/users/register',
                json={'role': 'admin', 'username': username, 'password': password}
            )
            
            if response.status_code == 201:
                return render_template('signup.html', success='Account created! Please login.')
            else:
                error_msg = response.json().get('error', 'Registration failed')
                return render_template('signup.html', error=error_msg)
        except Exception as e:
            print(f"Signup error: {e}")
            return render_template('signup.html', error='Connection error')
    
    return render_template('signup.html')

@app.route('/admin')
def admin():
    if not is_admin():
        return redirect(url_for('login'))
    
    try:
        response = requests.get(f'{BACKEND_URL}/api/feedbacks')
        if response.status_code == 200:
            feedbacks = response.json()
            # Convert date strings to datetime objects
            from dateutil import parser
            for fb in feedbacks:
                if fb.get('created_at'):
                    try:
                        fb['created_at'] = parser.parse(fb['created_at'])
                    except:
                        fb['created_at'] = None
            
            return render_template('admin.html', feedbacks=feedbacks, username=session.get('username'))
        else:
            return render_template('admin.html', feedbacks=[], error='Failed to load feedbacks')
    except Exception as e:
        print(f"Admin error: {e}")
        return render_template('admin.html', feedbacks=[], error='Connection error')

@app.route('/admin/export')
def export_feedbacks():
    if not is_admin():
        return redirect(url_for('login'))
    
    try:
        response = requests.get(f'{BACKEND_URL}/api/feedbacks')
        if response.status_code == 200:
            feedbacks = response.json()
            
            # Convert to DataFrame
            df = pd.DataFrame(feedbacks)
            
            # Create Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Feedbacks')
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=f'feedbacks_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            )
        else:
            return 'Failed to export', 500
    except Exception as e:
        print(f"Export error: {e}")
        return 'Export error', 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
