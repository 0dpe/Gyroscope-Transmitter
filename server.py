import asyncio
import websockets
import ssl

async def handler(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            print("Received:", message)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    # SSL context for secure WebSockets
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # Use the same certificate and key as your HTTPS server
    ssl_context.load_cert_chain('cert.pem', 'key.pem')
    
    # Start secure WebSocket server with SSL context
    server = await websockets.serve(handler, "0.0.0.0", 8765, ssl=ssl_context)
    
    print("Secure WebSocket server started on wss://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())