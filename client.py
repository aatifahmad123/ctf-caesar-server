import json

import pwn

r = pwn.remote("crypto-aatif.duckdns.org", 6000)

print(r.recvline().decode())

r.sendline(json.dumps({"get": "cipher"}).encode())

challenge = json.loads(r.recvline().decode())
print("Challenge received:", challenge)

r.close()
