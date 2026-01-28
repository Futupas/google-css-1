import asyncio
import websockets

clients = set()

async def handler(websocket):
    clients.add(websocket)
    ip = websocket.remote_address[0]

    try:
        async for message in websocket:
            text = f"{ip}: {message}"
            await asyncio.gather(
                *[client.send(text) for client in clients]
            )
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()

asyncio.run(main())
