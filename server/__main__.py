from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from os import getcwd
from os.path import join as join_paths

HOST = "0.0.0.0"
PORT = 8080


class MyHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_PUT(self):
        content_len = int(self.headers["Content-Length"])
        content = self.rfile.read(content_len)

        path = join_paths(getcwd(), self.path)
        with open(self.translate_path(path), "wb") as f:
            f.write(content)

        self.send_response(201, "Created")
        self.end_headers()


handler = MyHttpRequestHandler
with TCPServer((HOST, PORT), handler) as server:
    print(f"Server started at http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")
