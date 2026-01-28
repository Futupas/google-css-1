import asyncio
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import websockets

clients = set()
history = []

MAX_HISTORY = 200

async def ws_handler(ws):
    clients.add(ws)

    # send history to new client
    for msg in history:
        await ws.send(msg)

    try:
        async for _ in ws:
            pass
    finally:
        clients.remove(ws)

async def broadcast(message):
    dead = set()
    for c in clients:
        try:
            await c.send(message)
        except:
            dead.add(c)
    clients.difference_update(dead)

class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/send":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode()
        msg = body.strip()

        if not msg:
            self.send_response(204)
            self.end_headers()
            return

        ip = self.client_address[0]
        text = f"{ip}: {msg}"

        history.append(text)
        if len(history) > MAX_HISTORY:
            history.pop(0)

        asyncio.run_coroutine_threadsafe(
            broadcast(text), loop
        )

        self.send_response(204)
        self.end_headers()

def run_http():
    server = HTTPServer(("0.0.0.0", 8766), HttpHandler)
    server.serve_forever()

async def run_ws():
    async with websockets.serve(ws_handler, "0.0.0.0", 8765):
        await asyncio.Future()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

threading.Thread(target=run_http, daemon=True).start()
loop.run_until_complete(run_ws())
