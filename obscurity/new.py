#!/usr/bin/env python3

def decrypt(text, key):
    keylen = len(key)
    keyPos = 0
    decrypted = ""
    for x in text:
        keyChr = key[keyPos]
        newChr = ord(x)
        newChr = chr((newChr - ord(keyChr)) % 255)
        decrypted += newChr
        keyPos += 1
        keyPos = keyPos % keylen
    return decrypted

pass_enc = open("passwordreminder.txt").read()
enc = open("out.txt").read()
dec = open("check.txt").read()

print(decrypt(enc, dec))
print(decrypt(pass_enc, "alexandrovich"))
