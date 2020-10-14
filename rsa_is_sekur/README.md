RSA is Sekur
============

## Challenge info:

We've gathered a file that was encrypted with a 4096-bit RSA key. Can you help us decrypt the file?
Your goal is to compute the RSA private key from rsa.pub and use it to decrypt flag.enc

## Solution:

Now the fun begins. Most of my knowledge regarding RSA-based CTF challenges deals with multi-key shenanigans - keys sharing primes and the like - so a single-key challenge was a bit of a stumper. I checked if the modulus was even, but no luck there. Having exhausted what few tricks I had up my sleeve for solving this easily, I did what every elite CTF player does and went looking for a tool that does it for me (really what they do is go looking for a writeup from another CTF with a similar challenge so they can copy the solution, but keep that to yourself).
Luckily, I managed to find [a tool meant to break RSA keys for CTF challenges](https://github.com/Ganapati/RsaCtfTool), and after a bunch of finagling to get the dependencies installed, the tool worked like a charm, yielding the flag:

```
$ apt-get install libgmp3-dev libmpc-dev
$ pip3 install -r RsaCtfTool-master/requirements.txt
$ RsaCtfTool-master/RsaCtfTool.py --publickey rsa.pub --uncipherfile flag.enc --attack fermat
Equifax{consecutive_primes_with_rsa_will_ruin_ur_day}
```

P.S. For those wondering the issue with the given key was that the primes were too close to each other, allowing a [fast method of factorization](https://math.stackexchange.com/a/71135) to be used.
