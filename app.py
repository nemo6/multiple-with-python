import http.server
import socketserver
import sys
import glob
from os import path

file_paths = sys.argv[1:]

def my_function():

	tableau = []

	for args in file_paths:
		for x in glob.glob(args+"\\*"):
			if path.isfile(x):  
				tableau.append( { "name": path.basename(x), "size": path.getsize(x)} )

	tableau.sort(key=lambda x:x["size"])

	fullStr = "<style> table { font-family: arial, sans-serif; border-collapse: collapse; width: 100%; } td, th { border: 1px solid #dddddd; text-align: left; padding: 8px; } </style><link rel='icon' href='' /><table>"

	fullStr += "<table>"

	for x in tableau:
		fullStr += f"<tr><td>{x['name']}</td><td>{x['size']}</td></tr>"

	fullStr += "</table>"

	return fullStr

PORT = 8080

Handler = http.server.SimpleHTTPRequestHandler

class SimpleHTTPRequestHandler(Handler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf8")
        self.end_headers()
        self.wfile.write(bytes(my_function(), 'utf8'))

httpd = http.server.HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Le contenu du fichier est afficher sur le localhost:{PORT}")
    httpd.serve_forever()