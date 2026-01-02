![AWS EC2 Instance Running](./instance.png)

# Caesar Cipher TCP Challenge Server

A lightweight, CryptoHack-style **TCP challenge server** built using pure Python sockets.
The server delivers a **Caesar cipher challenge over raw TCP**, designed for learning:

* pwntools
* client–server protocols
* basic cryptography
* cloud deployment (AWS EC2)

This project was built end-to-end as a hands-on learning exercise, including real cloud deployment.

---

## Features

* Raw TCP server (no HTTP, no frameworks)
* JSON-based request/response protocol
* Caesar cipher challenge generation
* Handles multiple clients (threaded)
* Basic rate limiting (per IP)
* Always-on using `systemd`
* Deployable on AWS EC2 Free Tier

---

## Protocol Overview

### Server → Client (on connect)

```
Aatif welcomes you to the challenge! We only speak in JSON.
Request the Caesar Cipher challenge.
```

### Client → Server

```json
{"get": "cipher"}
```

### Server → Client

```json
{
  "cipher": "Yludw Nrkol lv wkh ehvw",
  "shift": 3,
  "note": "Decode it yourself."
}
```

The server **does not verify the solution**.
Cracking the cipher is intentionally left to the user.

---

## Running the Server Locally

```bash
python3 server.py
```

The server listens on:

```
PORT = 6000
```

---

## Connecting Using netcat

```bash
nc <SERVER_IP> 6000
```

Then send:

```json
{"get":"cipher"}
```

---

## Example Client (pwntools)

```python
import json
from pwn import *

r = remote("<SERVER_IP>", 6000)

print(r.recvline().decode())

r.sendline(json.dumps({"get": "cipher"}).encode())

challenge = json.loads(r.recvline().decode())
print(challenge)

r.close()
```

---

## Caesar Cipher Solver (Example)

```python
def caesar_cipher(cipher, shift):
    decoded = ""
    for ch in cipher:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            decoded += chr((ord(ch) - base - shift) % 26 + base)
        else:
            decoded += ch
    return decoded
```

---

## Deployment Notes

* Deployed on **AWS EC2 (Free Tier)**
* Ubuntu 22.04
* Managed using `systemd`
* Firewall rules:

  * SSH (22) → My IP
  * Challenge port (6000) → Anywhere

---

## Learning Outcomes

This project helped understand:

* TCP socket programming
* Client–server lifecycles
* JSON over sockets
* pwntools fundamentals
* Caesar cipher mechanics
* Cloud networking & firewalls
* Running production services with `systemd`

---

## Future Improvements

* Randomized Caesar shifts
* Brute-force-only challenges
* Multiple cipher types (ROT13, XOR, Vigenère)
* Logging and analytics
* Multi-round challenges

---

## License

MIT License — feel free to use, modify, and learn from it.

---

**Built for learning. Deployed for real.**
