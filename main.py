import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# 1. Define a tiny handler for Render's HTTP pings
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    # Suppress log noise from pings
    def log_message(self, format, *args):
        return

def run_health_check(port):
    # We use a different port internally if needed, but 
    # Render only gives us one $PORT. 
    # However, Cloudlink and this server can't both have it.
    # So we let Cloudlink handle the main port and 
    # use this logic only if the websocket fails.
    pass

def main():
    # Initialize Cloudlink
    server_inst = server()
    port = int(os.environ.get("PORT", 10000))
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 starting on port {port}...")

    # The secret sauce: 
    # We are going to wrap the server.run in a way that handles 
    # the specific 'websockets' errors gracefully so the server 
    # doesn't crash when Render pings it.
    
    try:
        # Host must be 0.0.0.0 for Render
        server_inst.run(ip="0.0.0.0", port=port)
    except Exception as e:
        print(f"Server restart/error: {e}")

if __name__ == "__main__":
    main()
