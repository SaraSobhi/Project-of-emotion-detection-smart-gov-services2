import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from datetime import datetime, timedelta
from io import BytesIO
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Dummy data for demonstration
DUMMY_FEEDBACKS = [
    {
        'id': '1',
        'feedback': 'The service was excellent! Very satisfied with the experience.',
        'user_id': 'anon1',
        'created_at': datetime.now() - timedelta(days=2, hours=3),
        'sentiment': 'positive',
        'cleaned_text': 'service excellent satisfied experience',
        'processed_text': 'خدمة ممتازة راض تجربة',
        'confidence': 0.92,
        'has_negation': False
    },
    {
        'id': '2',
        'feedback': 'Not happy with the product quality. Expected better.',
        'user_id': 'anon2',
        'created_at': datetime.now() - timedelta(days=1, hours=5),
        'sentiment': 'negative',
        'cleaned_text': 'not happy product quality expected better',
        'processed_text': 'غير راض جودة منتج توقع أفضل',
        'confidence': 0.87,
        'has_negation': True
    },
    {
        'id': '3',
        'feedback': 'The interface is okay, nothing special but works fine.',
        'user_id': 'anon3',
        'created_at': datetime.now() - timedelta(hours=12),
        'sentiment': 'neutral',
        'cleaned_text': 'interface okay nothing special works fine',
        'processed_text': 'واجهة عادية لا شيء مميز يعمل جيد',
        'confidence': 0.78,
        'has_negation': False
    },
    {
        'id': '4',
        'feedback': 'Amazing features! This is exactly what I needed.',
        'user_id': 'anon4',
        'created_at': datetime.now() - timedelta(hours=6),
        'sentiment': 'positive',
        'cleaned_text': 'amazing features exactly needed',
        'processed_text': 'ميزات رائعة بالضبط احتاج',
        'confidence': 0.95,
        'has_negation': False
    },
    {
        'id': '5',
        'feedback': 'Terrible customer support. They did not help at all.',
        'user_id': 'anon5',
        'created_at': datetime.now() - timedelta(hours=3),
        'sentiment': 'negative',
        'cleaned_text': 'terrible customer support not help',
        'processed_text': 'دعم عملاء سيء لم يساعد',
        'confidence': 0.91,
        'has_negation': True
    },
    {
        'id': '6',
        'feedback': 'Good value for money. Recommended!',
        'user_id': 'anon6',
        'created_at': datetime.now() - timedelta(hours=2),
        'sentiment': 'positive',
        'cleaned_text': 'good value money recommended',
        'processed_text': 'قيمة جيدة مقابل المال موصى',
        'confidence': 0.89,
        'has_negation': False
    },
    {
        'id': '7',
        'feedback': 'Average experience. Could be improved in some areas.',
        'user_id': 'anon7',
        'created_at': datetime.now() - timedelta(hours=1),
        'sentiment': 'neutral',
        'cleaned_text': 'average experience improved areas',
        'processed_text': 'تجربة متوسطة تحسين مجالات',
        'confidence': 0.72,
        'has_negation': False
    },
    {
        'id': '8',
        'feedback': 'Fast delivery and great packaging. Very impressed!',
        'user_id': 'anon8',
        'created_at': datetime.now() - timedelta(minutes=30),
        'sentiment': 'positive',
        'cleaned_text': 'fast delivery great packaging impressed',
        'processed_text': 'توصيل سريع تغليف رائع معجب',
        'confidence': 0.94,
        'has_negation': False
    }
]

# Demo admin credentials
DEMO_ADMIN = {
    'username': 'admin',
    'password': 'admin123'
}

# Helper function to check if user is admin
def is_admin():
    return session.get('is_admin', False)

# Helper function to get or create anonymous user
def get_anonymous_user():
    if 'anon_user_id' not in session:
        session['anon_user_id'] = f'anon_{random.randint(1000, 9999)}'
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
        
        # Simulate adding feedback to dummy data
        new_feedback = {
            'id': str(len(DUMMY_FEEDBACKS) + 1),
            'feedback': feedback_text,
            'user_id': user_id,
            'created_at': datetime.now(),
            'sentiment': random.choice(['positive', 'negative', 'neutral']),
            'cleaned_text': feedback_text.lower(),
            'processed_text': 'معالج',
            'confidence': round(random.uniform(0.7, 0.98), 2),
            'has_negation': random.choice([True, False])
        }
        DUMMY_FEEDBACKS.append(new_feedback)
        
        return render_template('feedback.html', success='Thank you for your feedback!')
    
    return render_template('feedback.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == DEMO_ADMIN['username'] and password == DEMO_ADMIN['password']:
            session['is_admin'] = True
            session['username'] = username
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid credentials. Use admin/admin123')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        
        # In demo mode, just show success message
        return render_template('signup.html', success='Demo mode: Account created! Use admin/admin123 to login.')
    
    return render_template('signup.html')

@app.route('/admin')
def admin():
    if not is_admin():
        return redirect(url_for('login'))
    
    return render_template('admin.html', feedbacks=DUMMY_FEEDBACKS, username=session.get('username'))

@app.route('/admin/export')
def export_feedbacks():
    if not is_admin():
        return redirect(url_for('login'))
    
    if not HAS_PANDAS:
        return 'Pandas not installed. Install with: pip install pandas openpyxl', 500
    
    # Convert to DataFrame
    df_data = []
    for fb in DUMMY_FEEDBACKS:
        df_data.append({
            'ID': fb['id'],
            'Feedback': fb['feedback'],
            'User ID': fb['user_id'],
            'Created At': fb['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            'Sentiment': fb['sentiment'],
            'Confidence': fb['confidence'],
            'Has Negation': fb['has_negation'],
            'Cleaned Text': fb['cleaned_text'],
            'Processed Text': fb['processed_text']
        })
    
    df = pd.DataFrame(df_data)
    
    # Create Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Feedbacks')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'feedbacks_demo_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    print("=" * 60)
    print("DEMO MODE - Running with dummy data")
    print("=" * 60)
    print("Login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 60)
    print("Server starting at http://localhost:8000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=8000)
