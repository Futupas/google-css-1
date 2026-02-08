import os, uuid
from flask import Flask, render_template, request, redirect, url_for, Response, session, jsonify
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-key-for-dev')

# --- KONFIGURACE ---
LABEL_LIMIT = 40  # Kolik znaků z textu se ukáže v popisku grafu

# --- DATASET ---
QUESTIONS = [
    {
        "id": "Q1",
        "options": [
            {"text": "V hlubokém lese šeptá vítr staré příběhy. Listí stromů se jemně chvěje v nekonečném tanci světla a stínu, zatímco mechový koberec pod nohama tlumí každý krok.", "ai": False},
            {"text": "Detekována anomálie v atmosférickém tlaku. Generování narativní struktury bylo dokončeno s vysokou mírou pravděpodobnosti úspěchu u cílové skupiny.", "ai": True}
        ]
    },
    {
        "id": "Q2",
        "options": [
            {"text": "Dnes ráno jsem vstal a uvědomil si, že jsem zapomněl vypnout kávovar. Ta vůně spálených zrn se táhla celým bytem jako nechtěná připomínka mé ranní roztržitosti.", "ai": False},
            {"text": "Kávový extrakt byl připraven v souladu s nastavenými parametry teploty a tlaku. Systém zaznamenal překročení časového limitu ohřevu organických látek.", "ai": True}
        ]
    }
]

state = {
    "index": 0,
    "phase": "voting", 
    "votes": [],
    "poll_id": str(uuid.uuid4())
}

def init_q():
    state["votes"] = [0] * len(QUESTIONS[state["index"]]["options"])
    state["poll_id"] = str(uuid.uuid4())

init_q()

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not (auth.username == os.getenv('ADMIN_USER') and auth.password == os.getenv('ADMIN_PASS')):
            return Response('Login', 401, {'WWW-Authenticate': 'Basic realm="Admin"'})
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html', q=QUESTIONS[state["index"]], state=state)

@app.route('/api/state')
def get_state():
    q = QUESTIONS[state["index"]]
    return jsonify({
        "phase": state["phase"],
        "correct_indices": [i for i, opt in enumerate(q["options"]) if opt["ai"]] if state["phase"] == "results" else [],
        "poll_id": state["poll_id"],
        "q_id": q["id"]
    })

@app.route('/api/stats')
@requires_auth
def get_stats():
    total = sum(state["votes"])
    q = QUESTIONS[state["index"]]
    correct_votes = sum(state["votes"][i] for i, opt in enumerate(q["options"]) if opt["ai"])
    
    # Dynamické popisky grafu (N znaků)
    labels = [opt["text"][:LABEL_LIMIT] + "..." for opt in q["options"]]
    
    return jsonify({
        "votes": state["votes"],
        "labels": labels,
        "accuracy": f"{correct_votes}/{total} ({round(correct_votes/total*100,1) if total>0 else 0}%)",
        "phase": state["phase"],
        "correct_indices": [i for i, opt in enumerate(q['options']) if opt['ai']]
    })

@app.route('/vote/<int:oid>', methods=['POST'])
def vote(oid):
    if state["phase"] != "voting": return redirect(url_for('index'))
    key = f"v_{state['poll_id']}"
    if key in session: state["votes"][session[key]] -= 1
    state["votes"][oid] += 1
    session[key] = oid
    session.modified = True
    return redirect(url_for('index'))

@app.route('/admin/nav/<action>')
@requires_auth
def navigate(action):
    if action == "next": state["index"] = (state["index"] + 1) % len(QUESTIONS)
    elif action == "prev": state["index"] = (state["index"] - 1) % len(QUESTIONS)
    elif action == "toggle": state["phase"] = "results" if state["phase"] == "voting" else "voting"
    
    if action in ["next", "prev"]:
        state["phase"] = "voting"
        init_q()
    return redirect(url_for('admin'))

@app.route('/admin')
@requires_auth
def admin():
    return render_template('admin.html', q=QUESTIONS[state["index"]], state=state)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
