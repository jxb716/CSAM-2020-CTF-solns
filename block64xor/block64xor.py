#!/usr/bin/env python3

from base64 import b64decode
from itertools import cycle
from socket import getaddrinfo, socket

def solve(flag):
	flag = b64decode(flag)
	pad = bytes(x ^ y for (x, y) in zip(flag, b"Equifax{"))
	print("".join(chr(x ^ y) for (x, y) in zip(flag, cycle(pad))))

if __name__ == "__main__":
	af, socktype, proto, canonname, sa = getaddrinfo("challenges.ctfd.io", 30230)[0]
	with socket(af, socktype, proto) as sock:
		sock.connect(sa)
		with sock.makefile() as f:
			f.readline()									# Welcome to Block64XOR!
			f.readline()									# Block64XOR is a block cipher
			f.readline()									# \n
			f.readline()									# Now generating a random key to encrypt flag...
			f.readline()									# Here's the encrypted flag, base64 encoded:

			flag = f.readline().strip()						#

			f.readline()									# Now generating a new random key...
			f.readline()									# \n
			f.readline()									# Key generated. Please input your message to encrypt:

			sock.sendall(b"\x00\n")							# Message doesn't matter for this challenge

			f.readline()									# \n
			f.readline()									# \n
			f.readline()									# Here's your encrypted message, base64 encoded:
			c = f.readline().strip()

			solve(flag)
