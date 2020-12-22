import http.client
import json
import time

class SSP_client():
    def __init__(self, bid_floor):
        """Setting bidding floor format."""
        self.bid_floor = bid_floor
        self.bid_floor = json.dumps(self.bid_floor)

    def POST(self, local, PORT):
        self.local = local
        self.PORT = PORT
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        conn = http.client.HTTPConnection(self.local, self.PORT)
        start = time.time()
        conn.request('POST', '/ippinte/api/scene/getall', self.bid_floor.encode('utf-8'), headers)
        response = conn.getresponse()
        request_time = time.time() - start
        print(f"Request completed in {request_time} sec.")

        if response.status == 200:
            stc1 = response.read().decode('utf-8')
            stc = json.loads(stc1)
            print("-----------------RESPONSE from DSP----------------")
            print(stc)
            print("-----------------RESPONSE from DSP----------------")
            conn.close()
        else:
            print("-----------------RESPONSE from DSP----------------")
            print("response = 204, No contents in response")
            print("-----------------RESPONSE from DSP----------------")
            conn.close()

if __name__ == "__main__":
    bid_floor = {'bid_floor': 12.00}
    client = SSP_client(bid_floor)
    client.POST(local="localhost", PORT=9000)