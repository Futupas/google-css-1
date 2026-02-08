import os, uuid
from flask import Flask, render_template, request, redirect, url_for, Response, session, jsonify
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'tajny-klic-123')

# --- GLOBÁLNÍ STAV ---
poll = {
    "id": str(uuid.uuid4()), # Unikátní ID kola
    "question": "Který text vytvořila AI?",
    "options": ["Text 1", "Text 2"],
    "votes": [0, 0],
    "is_open": False
}

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == os.getenv('ADMIN_USER') and auth.password == os.getenv('ADMIN_PASS')):
            return Response('Přihlašte se.', 401, {'WWW-Authenticate': 'Basic realm="Admin"'})
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html', poll=poll)

@app.route('/api/data')
def get_data():
    total = sum(poll['votes'])
    stats = []
    for i, count in enumerate(poll['votes']):
        percent = round((count / total * 100), 2) if total > 0 else 0
        stats.append({"label": poll['options'][i], "count": count, "percent": percent})
    return jsonify({"stats": stats, "total": total, "is_open": poll['is_open'], "question": poll['question']})

@app.route('/vote/<int:option_id>', methods=['POST'])
def vote(option_id):
    if not poll['is_open']: return redirect(url_for('index'))
    
    # Každé kolo hlasování má své ID v session
    session_key = f"voted_{poll['id']}"
    prev_vote = session.get(session_key)

    if prev_vote is not None:
        poll['votes'][prev_vote] -= 1 # Odečíst starý hlas
    
    poll['votes'][option_id] += 1
    session[session_key] = option_id # Uložit nový hlas
    session.modified = True
    return redirect(url_for('index'))

@app.route('/admin')
@requires_auth
def admin():
    return render_template('admin.html', poll=poll)

@app.route('/admin/action', methods=['POST'])
@requires_auth
def admin_action():
    action = request.form.get('action')
    
    if action == "start":
        # RESET VŠEHO
        poll['id'] = str(uuid.uuid4())
        poll['question'] = request.form.get('question', 'Který text vytvořila AI?')
        poll['options'] = [o for o in request.form.getlist('options') if o.strip()]
        poll['votes'] = [0] * len(poll['options'])
        poll['is_open'] = True
    elif action == "stop":
        poll['is_open'] = False
        
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
