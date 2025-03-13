import argparse
import asyncio
import http.server
import socket
import ssl
import threading
import websockets
from sys import stdout

CERT = 'cert.pem'
KEY = 'key.pem'

def start_https_server():
    httpd = http.server.HTTPServer(('0.0.0.0', args.https_port), http.server.SimpleHTTPRequestHandler)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile = CERT, keyfile = KEY)
    
    httpd.socket = context.wrap_socket(httpd.socket, server_side = True)
    
    print(f'HTTPS server starting:    https://0.0.0.0:{args.https_port}')
    httpd.serve_forever()

async def websocket_handler(websocket):
    print('Client connected')
    try:
        async for message in websocket:
            stdout.write('\r' + message)
            stdout.flush()
    except websockets.exceptions.ConnectionClosed:
        print('Client disconnected')

async def start_websocket_server():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(CERT, KEY)
    server = await websockets.serve(websocket_handler, '0.0.0.0', args.ws_port, ssl = ssl_context)
    
    print(f'WebSocket server running: wss://0.0.0.0:{args.ws_port}\n\nBrowse this address on the iPhone:\nhttps://{local_ip}:{args.https_port}/index.html')
    await server.wait_closed()

async def main():
    parser = argparse.ArgumentParser(description = 'Start HTTPS and WebSocket servers')
    parser.add_argument('--https-port', type = int, default = 8000, help = 'HTTPS server port')
    parser.add_argument('--ws-port', type = int, default = 8001, help = 'WebSocket server port')
    global args
    args = parser.parse_args()

    global local_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1)) # Doesn't have to be reachable
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    print(f'Local IP:                 {local_ip}')

    threading.Thread(target = start_https_server, daemon = True).start()
    await start_websocket_server()

asyncio.run(main())
