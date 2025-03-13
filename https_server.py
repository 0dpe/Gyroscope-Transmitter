import argparse
import asyncio
import http.server
import socket
import ssl
import threading
import websockets

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def start_https_server(port, cert, key):
    httpd = http.server.HTTPServer(('0.0.0.0', port), http.server.SimpleHTTPRequestHandler)
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert, keyfile=key)
    
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"HTTPS Server running on https://0.0.0.0:{port}")
    httpd.serve_forever()

async def websocket_handler(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            print("Received:", message)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def start_websocket_server(port, cert, key):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert, key)
    server = await websockets.serve(websocket_handler, "0.0.0.0", port, ssl=ssl_context)
    
    print(f"Secure WebSocket server started on wss://0.0.0.0:{port}")
    await server.wait_closed()

async def main():
    parser = argparse.ArgumentParser(description='Start HTTPS and WebSocket servers')
    parser.add_argument('--https-port', type=int, default=8000, help='HTTPS server port')
    parser.add_argument('--ws-port', type=int, default=8001, help='WebSocket server port')
    parser.add_argument('--cert', type=str, default='cert.pem', help='SSL certificate file')
    parser.add_argument('--key', type=str, default='key.pem', help='SSL key file')
    args = parser.parse_args()

    # Get local IP
    local_ip = get_local_ip()
    print(f"Local IP: {local_ip}")

    # Start HTTPS server in a separate thread
    https_thread = threading.Thread(
        target=start_https_server,
        args=(args.https_port, args.cert, args.key),
        daemon=True
    )
    https_thread.start()

    # Start WebSocket server in the main thread
    await start_websocket_server(args.ws_port, args.cert, args.key)

asyncio.run(main())
