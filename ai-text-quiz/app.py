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
    # {
    #     "id": "Q1",
    #     "options": [
    #         {"text": "V hlubokém lese šeptá vítr staré příběhy. Listí stromů se jemně chvěje v nekonečném tanci světla a stínu, zatímco mechový koberec pod nohama tlumí každý krok.", "ai": False},
    #         {"text": "Detekována anomálie v atmosférickém tlaku. Generování narativní struktury bylo dokončeno s vysokou mírou pravděpodobnosti úspěchu u cílové skupiny.", "ai": True}
    #     ]
    # },
    # {
    #     "id": "Q2",
    #     "options": [
    #         {"text": "Dnes ráno jsem vstal a uvědomil si, že jsem zapomněl vypnout kávovar. Ta vůně spálených zrn se táhla celým bytem jako nechtěná připomínka mé ranní roztržitosti.", "ai": False},
    #         {"text": "Kávový extrakt byl připraven v souladu s nastavenými parametry teploty a tlaku. Systém zaznamenal překročení časového limitu ohřevu organických látek.", "ai": True}
    #     ]
    # },
    {
        "id": "Q1",
        "options": [
            { "ai": False, "text": "Po studiích se stává knězem a odchází jako kaplan do Markova ke staršímu moudrému a laskavému knězi, kde prožívá šťastnou idylku. Zde setrvává několik let, dokonce i poté, co jeho někdejší spolužáci již odcházejí na svá první samostatná místa." },
            { "ai": True,  "text": "Po atestaci se stává lékařem a nastupuje do venkovské nemocnice k postaršímu, trpělivému a zkušenému primáři, u něhož nachází klidnou praxi. Setrvává zde dlouhou dobu, a to i v době, kdy jeho vrstevníci z fakulty již usilují o vedoucí pozice na velkých pražských klinikách." },
        ]
    },
    {
        "id": "Q2",
        "options": [
            { "ai": False, "text": "Za čas, krátce po dokončení Jesliček, je poslán do důchodu. Důvodem je, mimo jiné, že zavádí do některých částí liturgie češtinu a že jím vyřezané Jesličky jsou „příliš lidové“. Je mu umožněno ještě u těchto Jesliček vést první pobožnost." },
            { "ai": True,  "text": "Nedlouho po dokončení návrhu radnice je poslán na odpočinek. Hlavním důvodem je, že do konzervativního projektu vkládá moderní materiály a jeho pojetí fasády je prý „příliš odvážné“. Dostává však šanci osobně se zúčastnit slavnostního poklepání na základní kámen." },
        ]
    },
    {
        "id": "Q3",
        "options": [
            { "ai": False, "text": "V roce 1462 Jiří vyslal poselstvo k novému papeži se slibem poslušnosti, ale též se žádostí o potvrzení basilejské úmluvy. Papež Pius II. však 31. března 1462 za přítomnosti českého poselstva basilejská kompaktáta zrušil." },
            { "ai": True,  "text": "Na podzim roku 1938 vyslala vláda vyslance k mezinárodní komisi s ujištěním o spolupráci, leč zároveň s prosbou o garantování stávajících hranic. Mocnosti však na rozhodujícím zasedání v Mnichově za přítomnosti diplomatů veškeré předchozí záruky a dohody prohlásily za neplatné." },
        ]
    },
    {
        "id": "Q4",
        "options": [
            { "ai": False, "text": "Rokycana nejprve hlouček bratří, který se seskupil kolem Řehoře, podporoval a vyjednal jim možnost pobytu ve vsi Kunvaldu na králově zboží litickém. Brzy se však polekal věroučných novot, ke kterým bratří dospěli. Hlásali bratrství všech a považovali každý boj za veliký hřích." },
            { "ai": True,  "text": "Starosta nejprve komunitu zahradníků, která se utvořila v opuštěném vnitrobloku, chránil a vyjednal jim legální pronájem obecních pozemků. Brzy se však polekal ideových novot, které skupina začala prosazovat. Odmítali jakýkoliv soukromý majetek a považovali každé sekání trávy za útok na planetu." },
        ]
    },
    {
        "id": "Q5",
        "options": [
            { "ai": False, "text": "Tento děj je doprovázen výjevy ze života poddaných. Znovu se setkáváme s Petrem, který se pilně věnuje práci v bratrském sboru, i s Noemi, manželkou pana Rychnovského. Dalším dějovým pásmem je příběh Němkyně Anny." },
            { "ai": True,  "text": "Vyprávění je doprovázeno výjevy ze života měšťanů. Opět narážíme na Jakuba, který pilně pracuje v tkalcovském stavu, i na Marii, manželku mistra cechu. Dalším dějovým pásmem je osud osiřelé Kateřiny, která se snaží přežít v nelehkých časech po válce." },
        ]
    },
    {
        "id": "Q6",
        "options": [
            { "ai": False, "text": "Na třetím setkání se už ale Petr odhodlá a dá se s dívkou do hovoru. Začíná se rodit láska. Tráví spolu spousty času, Petr doprovází Lucii i do práce. Dívka se živí malováním a následně svá díla prodává, aby si vydělala na živobytí." },
            { "ai": True,  "text": "Při páté procházce už se ale Martin sebere a dá se s dívkou do řeči. Začíná rozkvétat láska. Tráví spolu veškerý volný čas, Martin doprovází Annu i na trh. Dívka se živí vyšíváním ubrusů a následně své zboží nabízí měšťkám, aby si zajistila skromné živobytí." },
        ]
    },
    {
        "id": "Q7",
        "options": [
            { "ai": False, "text": "On the third trip Pip jumped again when a whale hit the boat. He was a young boy—a cook—not a whaler. He was afraid. This time Stubb left him in the ocean. “Please come back!” Pip shouted. “Please don't leave me! The sharks will eat me!”" },
            { "ai": True,  "text": "During the fourth assault Thomas froze again when a shell hit the trench. He was a simple farmhand—a drummer—not a soldier. He was terrified. This time the Sergeant left him in the mud. “Wait for me!” Thomas screamed. “Please don't go! The enemy will find me!”" },
        ]
    },
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
