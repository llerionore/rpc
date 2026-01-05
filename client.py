import socket
import json
import uuid
import time

SERVER_IP = "172.31.38.104"
PORT = 5000
TIMEOUT = 2
MAX_RETRIES = 3

def rpc_call(method, params):
    request_id = str(uuid.uuid4())

    request = {
        "request_id": request_id,
        "method": method,
        "params": params,
        "timestamp": time.time()
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[CLIENT] Attempt {attempt}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(TIMEOUT)
                s.connect((SERVER_IP, PORT))
                s.sendall(json.dumps(request).encode())

                response = s.recv(4096)
                response_data = json.loads(response.decode())

                print("[CLIENT] Response:", response_data)
                return response_data

        except socket.timeout:
            print("[CLIENT] Timeout occurred, retrying...")
        except Exception as e:
            print("[CLIENT] Error:", e)

    print("[CLIENT] RPC failed after retries")
    return None

if __name__ == "__main__":
    rpc_call("add", {"a": 5, "b": 7})
