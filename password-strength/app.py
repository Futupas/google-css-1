from flask import Flask, render_template, request, jsonify
from zxcvbn import zxcvbn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    password = data.get('password', '')
    
    if not password:
        return jsonify({"error": "Password is required"}), 400
        
    # Analyze the password using Dropbox's zxcvbn algorithm
    result = zxcvbn(password)
    
    # Extract the most relevant data for the frontend
    return jsonify({
        "score": result['score'],  # 0 to 4
        "crack_time": result['crack_times_display']['offline_fast_hashing_1e10_per_second'],
        "warning": result['feedback']['warning'],
        "suggestions": result['feedback']['suggestions']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
