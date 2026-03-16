import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# 1. Tiny HTTP server to answer Render's pings
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return # Keep logs clean

def run_health_check_server(port):
    try:
        httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        httpd.serve_forever()
    except Exception:
        # If the port is already taken by Cloudlink, this thread just exits
        pass

def main():
    port = int(os.environ.get("PORT", 10000))

    # 2. Start health check in the background
    # This might fail if Cloudlink binds fast, but it often catches the pings
    threading.Thread(target=run_health_check_server, args=(port,), daemon=True).start()

    # 3. Initialize Cloudlink
    server_inst = server()
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 starting on port {port}...")
    
    # Use the simplest run method
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
