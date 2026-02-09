import os, json
from flask import Flask, render_template, request, redirect, url_for, Response
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- KONFIGURACE ---
CONFIG_FILE = 'data/config.json'
PREDEFINED_URLS = [
    {"name": "Google", "url": "https://google.com"},
    {"name": "Seznam", "url": "https://seznam.cz"},
    {"name": "ChatGPT", "url": "https://chatgpt.com"},
    {"name": "Nyan Cat", "url": "https://nyan.cat"}
]

# Inicializace databáze (souboru)
if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"target_url": "https://google.com"}, f)

def get_target():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)["target_url"]

def set_target(url):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({"target_url": url}, f)

# --- AUTH ---
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == os.getenv('ADMIN_USER') and auth.password == os.getenv('ADMIN_PASS')):
            return Response('Přihlašte se.', 401, {'WWW-Authenticate': 'Basic realm="Admin"'})
        return f(*args, **kwargs)
    return decorated

# --- ROUTES ---

@app.route('/')
def index():
    target = get_target()
    return render_template('index.html', target_url=target)

@app.route('/admin')
@requires_auth
def admin():
    return render_template('admin.html', 
                           current_url=get_target(), 
                           predefined=PREDEFINED_URLS)

@app.route('/admin/update', methods=['POST'])
@requires_auth
def update():
    new_url = request.form.get('url')
    if new_url:
        set_target(new_url)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
