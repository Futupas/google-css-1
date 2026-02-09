import hashlib
import requests
from flask import Flask, render_template, request, jsonify
from zxcvbn import zxcvbn

app = Flask(__name__)

def check_pwned_api(password):
    """Checks if password has been leaked using k-Anonymity."""
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code != 200:
            return 0
        
        # The API returns 'SUFFIX:COUNT' lines
        hashes = (line.split(':') for line in res.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count)
        return 0
    except Exception:
        return 0 # Fail silently if API is down

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    password = data.get('password', '')
    
    if not password:
        return jsonify({"error": "No password"}), 400
        
    # 1. zxcvbn Analysis
    result = zxcvbn(password)
    
    # 2. Leak Check
    leak_count = check_pwned_api(password)
    
    return jsonify({
        "score": result['score'],
        "crack_time": result['crack_times_display']['offline_fast_hashing_1e10_per_second'],
        "warning": result['feedback']['warning'],
        "suggestions": result['feedback']['suggestions'],
        "leak_count": leak_count
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
