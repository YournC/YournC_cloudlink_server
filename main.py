import os
import asyncio
import logging
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Silence all websockets logging to stop the log spam
logging.getLogger("websockets").setLevel(logging.CRITICAL)

# 1. Immediate Health Check to satisfy Render's boot-up probe
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        # Keeps logs clean
        return

def run_health_check(port):
    try:
        httpd = HTTPServer(('0.0.0.0', port), HealthCheck)
        # Handle just enough requests to satisfy Render's initial check
        threading.Thread(target=httpd.handle_request).start()
        time.sleep(1)
        httpd.server_close()
    except Exception:
        pass

async def start_cloudlink():
    # Use Render's assigned port
    port = int(os.environ.get("PORT", 10000))
    
    # Run the shield server first
    run_health_check(port)

    # Initialize Cloudlink
    server_inst = server()
    server_inst.check_origin = False # CRITICAL for PenguinMod
    
    # 2. PATCH: Ignore non-WebSocket pings (Fixes the EOFError)
    async def process_request(path, request_headers):
        # Check if the request is actually a WebSocket upgrade
        if "upgrade" not in request_headers.get("Connection", "").lower():
            # Return a standard HTTP 200 for Render's health checks
            return (200, [("Content-Type", "text/plain")], b"OK\n")
        return None

    # Load the CL4 protocol
    clpv4(server_inst)
    
    print(f"Cloudlink 4.0 starting on port {port}...")
    
    # 3. RUN: Bind to 0.0.0.0 so the external world can see it
    try:
        await server_inst.run(
            ip="0.0.0.0", 
            port=port, 
            process_request=process_request
        )
    except Exception as e:
        print(f"Server encountered an error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(start_cloudlink())
    except KeyboardInterrupt:
        pass
