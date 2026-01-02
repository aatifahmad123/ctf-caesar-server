import json

import pwn

r = pwn.remote("65.0.122.230", 6000)

print(r.recvline().decode())

r.sendline(json.dumps({"get": "cipher"}).encode())

challenge = json.loads(r.recvline().decode())
print("Challenge received:", challenge)

r.close()
