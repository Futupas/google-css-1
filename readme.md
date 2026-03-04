# Google CSS project - practice

To run any proactice, go to a folder for that and simply run `docker compose up`. You will need `.env` file somewhere, follow the fields in `.env.sample`. No tokens or anything like that is needed, just password somethimes

All the needed ports are also in `docker-compose.yml` file there. Generally the main service uses `80`/`443` port. You can connect from remote machine to see the presentation by your machine's IP address

## Description of the services

### AI test quiz (`ai-text-quiz`)

Just a simple quiz for detecting AI-generated vs human-written text.

* Port `80` is used
* Admin panel - `/admin`. Password-protected
* Password should be set in `.env` file
* `SECRET_KEY` in `.env` file can be basically anything

### Fake links (`fake-links`)

Shows that not all the links (even when they look legitimate) are in fact truthworthy. So there are some links that folow to the place they are not supposed to

### Homograph attack (`homograph-attack`)

Shows how different letters (with different codes) can look absolutely similar in browser. Basically it is just a fork from one of my projects [futupas.github.io/homograph-attack-demonstrator](https://futupas.github.io/homograph-attack-demonstrator/), but with czech language and a better default example

### HTTP_S (`http-s`)

There are 2 servers: `HTTP` on port `80` and `HTTPS` on port `443`. Also there is a simple machine with wireshark and `VMC` on port `6080` (accessible only from local machine, not from remote ones). Its secret is set in `docker-compose.yml` (you will need to log in). 

So go to `http://localhost:6080` in y9our browser (on the machine you are running `docker compose` on), log in and open wireshark (`Start -> Internet -> Wireshark`), then select your interface (`eth0`) and start capturing packets.

* WireShark filter HTTP: `tcp.port == 8080 && ip.dst == 172.20.0.2 && http`.
* WireShark filter HTTPS: `tcp.port == 8443 && ip.dst == 172.20.0.2`
* These IP addresses might be incorrect, that depends on your settings

### Password strength (`password-strength`)

Simple shows how strong is your password. Requires HTTPS and a certificate. 

If you do not have one, go to `password-strength/nginx` folder and run `openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=CZ/ST=Czechia/L=Brno/O=Dev/OU=IT/CN=localhost"` (or place your certs there)

### QR generator (`qr-generator`)

Simply generates QR codes

## Credits

Made by Futupas with help of Google Gemini and OpenAI ChatGPT

