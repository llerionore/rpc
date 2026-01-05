import socket
import json
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

def add(a, b):
    return a + b

def get_time():
    return time.ctime()

def reverse_string(s):
    return s[::-1]

FUNCTIONS = {
    "add": add,
    "get_time": get_time,
    "reverse_string": reverse_string
}

def handle_client(conn, addr):
    print(f"[SERVER] Connected by {addr}")
    try:
        data = conn.recv(4096)
        if not data:
            return

        request = json.loads(data.decode())
        print(f"[SERVER] Received request: {request}")

        if request.get("method") == "add":
            time.sleep(5)

        method = request["method"]
        params = request.get("params", {})
        request_id = request["request_id"]

        if method not in FUNCTIONS:
            response = {
                "request_id": request_id,
                "status": "ERROR",
                "error": "Unknown method"
            }
        else:
            result = FUNCTIONS[method](**params)
            response = {
                "request_id": request_id,
                "status": "OK",
                "result": result
            }

        conn.sendall(json.dumps(response).encode())

    except Exception as e:
        print("[SERVER] Error:", e)
    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Listening on port {PORT}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    start_server()
