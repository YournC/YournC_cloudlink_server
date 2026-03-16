import os
import time
import threading
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from cloudlink import server
from cloudlink.server.protocols import clpv4

# 1. SILENCE THE LOGS: This stops the EOFError/InvalidMessage spam from Render pings
logging.getLogger("websockets").setLevel(logging.CRITICAL)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        return

def run_temporary_handler(port):
    print(f"Bypassing Render health check on {port}...")
    try:
        httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        threading.Thread(target=httpd.handle_request).start() 
        time.sleep(5)
        httpd.server_close()
    except:
        pass

def main():
    port = int(os.environ.get("PORT", 10000))
    run_temporary_handler(port)

    # 2. Configure Cloudlink for Web compatibility
    server_inst = server()
    
    # Allows PenguinMod/TurboWarp to connect without security rejections
    server_inst.check_origin = False 
    
    # Load the protocol
    cl_protocol = clpv4(server_inst)

    print(f"Cloudlink 4.0 is LIVE. Connection string: wss://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'your-url')}")
    
    # Bind to 0.0.0.0 to ensure the proxy can route traffic
    server_inst.run(ip="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
