import os
import http
from cloudlink import server
from cloudlink.server.protocols import clpv4

# Custom handler to satisfy Render's health checks
async def health_check(path, request_headers):
    # If the request is not a WebSocket upgrade (like Render's HEAD/GET pings)
    if "upgrade" not in request_headers.get("Connection", "").lower():
        # Return a standard HTTP 200 OK response
        return http.HTTPStatus.OK, [], b"OK"
    return None

def main():
    server_inst = server()
    
    # Render provides the port via environment variable
    port = int(os.environ.get("PORT", 10000))
    
    # Initialize the protocol
    cl_protocol = clpv4(server_inst)
    
    print(f"Cloudlink 4.0 starting on port {port} with Health Check support...")

    # We inject the health_check into the underlying websockets server
    # Cloudlink 4.0 uses the 'ip' parameter for binding
    server_inst.run(
        ip="0.0.0.0", 
        port=port, 
        process_request=health_check # This is the magic line
    )

if __name__ == "__main__":
    main()
