from http.server import HTTPServer, BaseHTTPRequestHandler
from SQL_database import *
import json

class requestHandler(BaseHTTPRequestHandler):
    response = None
    def __init__(self, request, client_address, server):
        """
        Initialize MySQL settings
        """
        try:
            self.mysql = MySQL(db_settings)
            BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        except:
            print("SQL coonection failed!")

    def do_POST(self):
        """Serve a POST request."""
        req_datas = self.rfile.read(int(self.headers['content-length']))
        ssp_post = req_datas.decode('utf-8')
        ssp_post = json.loads(ssp_post)
        print("--------------------POST from SSP----------------")
        print(ssp_post)
        print("--------------------POST from SSP----------------")

        requestHandler.response = self.mysql.bidding_strategy(bid_floor=ssp_post["bid_floor"])
        if requestHandler.response != None:
            requestHandler.response = json.dumps(requestHandler.response)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(requestHandler.response.encode())
        else:
            self.send_response(204)
            self.end_headers()

    def do_GET(self):
        """Serve a GET request."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        ad_settings = self.mysql.fetch_all_data()
        self.wfile.write('<h1>Demand-Side Platform<h1>'.encode())
        output = ''
        output += '<html><body>'
        for i in ad_settings:
            output += str(i)
            output += '</br>'
        output += '</body>'
        self.wfile.write("<h1>Advertiser : <h1> ".encode())
        self.wfile.write(output.encode())
        if requestHandler.response:
            self.wfile.write(f"<h1>{requestHandler.response}<h1> ".encode())

if __name__ == "__main__":
    local, PORT = "localhost", 9000
    address = (local, PORT)

    server = HTTPServer(address, requestHandler)
    print(f"Server running on http://{local}:{PORT}/bw_dsp")
    server.serve_forever()
