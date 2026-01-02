import json
import socket
import threading
import time

HOST = "0.0.0.0"
PORT = 6000

MAX_REQUESTS = 5
WINDOW_SECONDS = 60

rate_limit = {}


def is_rate_limited(ip):
    now = time.time()
    timestamps = rate_limit.get(ip, [])
    timestamps = [t for t in timestamps if now - t < WINDOW_SECONDS]

    if len(timestamps) >= MAX_REQUESTS:
        rate_limit[ip] = timestamps
        return True

    timestamps.append(now)
    rate_limit[ip] = timestamps
    return False


def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


def handle_client(conn, addr):
    ip = addr[0]
    print(f"Connection from {ip}")

    if is_rate_limited(ip):
        conn.sendall(b'{"error":"rate limit exceeded"}\n')
        conn.close()
        return

    try:
        conn.sendall(
            b"Aatif welcomes you to the challenge! "
            b"We only speak in JSON. I hope that's OK. "
            b"Request the Caesar cipher challenge and solve it.\n"
        )

        data = conn.recv(1024)

        try:
            obj = json.loads(data.decode())
        except json.JSONDecodeError:
            conn.sendall(b'{"error":"invalid json"}\n')
            return

        if not isinstance(obj, dict):
            conn.sendall(b'{"error":"json must be an object"}\n')
            return

        if obj.get("get") != "cipher":
            conn.sendall(b'{"error":"expected {\\"get\\":\\"cipher\\"}"}\n')
            return

        plaintext = "Virat Kohli is the best"
        shift = 3

        challenge = {
            "cipher": caesar_encrypt(plaintext, shift),
            "shift": shift,
            "note": "Decode it yourself.",
        }

        conn.sendall((json.dumps(challenge) + "\n").encode())

    finally:
        conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Server running on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
