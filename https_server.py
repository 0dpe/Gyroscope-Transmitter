import http.server
import ssl
import sys

# Default port
port = 8000
if len(sys.argv) > 1:
    port = int(sys.argv[1])

# Create an HTTP server
handler = http.server.SimpleHTTPRequestHandler
httpd = http.server.HTTPServer(('0.0.0.0', port), handler)

# Create an HTTPS context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

# Wrap the HTTP server socket
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

print(f"HTTPS Server running on https://0.0.0.0:{port}")
httpd.serve_forever()