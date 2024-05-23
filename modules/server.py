import http
from http.server import BaseHTTPRequestHandler, HTTPServer

# Make our request handler
class Request_Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.path = 'test.html'
        try:
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.file = open(self.path).read()
            self.wfile.write(self.file.encode())
        except:
            self.send_response(404)
            self.file = "file not found"

    def do_POST(self):
        self.do_GET()


server = HTTPServer(("0.0.0.0", 8080), Request_Handler)
server.serve_forever()

# Server link: http://127.0.0.1/8080
