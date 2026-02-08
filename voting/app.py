import os
from flask import Flask, render_template, request, redirect, url_for, Response
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- STAV APLIKACE (v paměti) ---
poll = {
    "question": "Který text vytvořila AI?",
    "options": ["Text 1", "Text 2"],
    "votes": [0, 0],
    "is_open": False
}

# --- HTTP AUTH DEKORÁTOR ---
def check_auth(username, password):
    return username == os.getenv('ADMIN_USER') and password == os.getenv('ADMIN_PASS')

def authenticate():
    return Response('Nutno se přihlásit.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html', poll=poll)

@app.route('/vote/<int:option_id>', methods=['POST'])
def vote(option_id):
    if poll['is_open'] and 0 <= option_id < len(poll['options']):
        poll['votes'][option_id] += 1
    return redirect(url_for('index'))

@app.route('/admin')
@requires_auth
def admin():
    total_votes = sum(poll['votes'])
    stats = []
    for i, count in enumerate(poll['votes']):
        percent = (count / total_votes * 100) if total_votes > 0 else 0
        stats.append({
            "label": poll['options'][i],
            "count": count,
            "percent": f"{percent:.2f}"
        })
    return render_template('admin.html', poll=poll, stats=stats, total=total_votes)

@app.route('/admin/setup', methods=['POST'])
@requires_auth
def setup():
    question = request.form.get('question', 'Který text vytvořila AI?')
    options = request.form.getlist('options')
    
    poll['question'] = question
    poll['options'] = [o for o in options if o.strip()]
    poll['votes'] = [0] * len(poll['options'])
    poll['is_open'] = True
    return redirect(url_for('admin'))

@app.route('/admin/toggle', methods=['POST'])
@requires_auth
def toggle():
    poll['is_open'] = not poll['is_open']
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
