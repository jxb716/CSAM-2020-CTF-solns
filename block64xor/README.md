Block64XOR
==========

## Challenge info:

The developers realized their mistake in XORcrypt, and they've introduced a new encryption service called Block64XOR. They claim it's a block cipher using random keys for encryption, and they're giving away an encrypted flag. Can you find out what the flag is?
Connect using your CTF shell: `nc challenges.ctfd.io 30230`

## Solution:

Once again the challenge is to exploit the vulnerable service and recover the flag:
```
$ nc challenges.ctfd.io 30230
Welcome to Block64XOR! This is the more secure replacement for XORcrypt!
Block64XOR is a block cipher that uses random keys for encryption!

Now generating a random key to encrypt flag...
Here's the encrypted flag, base64 encoded:
31KUkUwWTdDpQoXZdRVZxPlI18xSGEf081C+jl8bW87oQoOUTyhBxMVCvohLBUHC+0++iEYWXMXuRpmMdRZB3/tAiqcfT1TK/hDThQ==

Now generating a new random key...
Key generated. Please input your message to encrypt:
AAAAAAAAAAAAAAAA


Here's your encrypted message, base64 encoded:
f3IEK2wuAq9/cgQrbC4Crw==

Bye!
```
My initial thought was to avoid fixing what isn't broken, send some null bytes to recover the pad and XOR to victory; it wasn't until I was wondering why I was staring at garbage that I noticed the service generated a new key to encrypt the provided plaintext.

At this point my plan became to pass in the encrypted flag and figure out some way to end up with the flag XORed only by the second keystream, which I could recover. I don't know if there was some input validation that checked if you were passing in a substring of the key or what, but I must've beat my head against that service for an hour at least to make it give me _something_.  I tried passing the flag in reverse, I tried XORing the flag locally before I sent it, I tried random substrings of the flag - I couldn't get anything back. The worst part was if I tried passing throwaway data like "AAAAAAAA" everything worked fine.

At some point, though, it clicked - the service was XORing in eight-byte blocks and I could assume with high probability the first eight characters of the flag were "Equifax{", so what if I XORed that with the encrypted flag to get the pad and use the pad to decrypt the rest of the flag? 

```
$ solns/block64xor.py 
Equifax{sad!_block64xor_is_vulnerable_to_a_partial_plaintext_attack_58aad32}
```
