from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    # Získáme IP adresu. 
    # request.remote_addr v 'host' módu ukáže skutečnou IP klienta.
    user_ip = request.remote_addr
    
    # Pokud by byl web za proxy, použili bychom toto:
    # user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    return render_template('index.html', ip=user_ip)

if __name__ == '__main__':
    # Port 80, aby to vypadalo jako opravdový web
    app.run(host='0.0.0.0', port=80)
