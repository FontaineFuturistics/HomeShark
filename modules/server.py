from http.server import BaseHTTPRequestHandler, HTTPServer
import modules.thread_monitor as thread_monitor
import threading

# Make our request handler
class Request_Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.path = 'output.html'
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

def start_server(mon: thread_monitor.ThreadMonitor):

    # Make a server
    server = HTTPServer(("0.0.0.0", 8080), Request_Handler)

    # Start serving in another thread
    t3 = threading.Thread(target=server.serve_forever, args=())
    t3.start()

    # Keep checking if we need to close
    while mon.must_exit == False:
        continue

    # Now we need to exit
    server.shutdown()

    return

# Server link: http://127.0.0.1/8080
