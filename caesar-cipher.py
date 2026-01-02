def caesar_cipher(cipher, shift):
    decoded = ""

    for ch in cipher:
        if ch.isalpha():
            # Decide base depending on case
            base = ord("A") if ch.isupper() else ord("a")

            # Shift backwards and wrap using modulo
            decoded += chr((ord(ch) - base - shift) % 26 + base)
        else:
            # Keep spaces and punctuation unchanged
            decoded += ch

    return decoded


print(caesar_cipher("Yludw Nrkol lv wkh ehvw", 3))
