from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_server(port=8080):
    server_address = ('', port)  # Listen on all interfaces
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
