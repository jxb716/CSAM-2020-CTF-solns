#!/usr/bin/env python3

from base64 import b64decode
from socket import getaddrinfo, socket

def solve(flag):
	print(b64decode(flag).decode("ascii"))

if __name__ == "__main__":
	af, socktype, proto, canonname, sa = getaddrinfo("challenges.ctfd.io", 30130)[0]
	with socket(af, socktype, proto) as sock:
		sock.connect(sa)
		with sock.makefile() as f:
			f.readline()									# Welcome to the XORcrypt encryption service
			f.readline()									# The most secure crypto service in the world!
			f.readline()									# Send me a message to encrypt with the secret flag:

			sock.sendall(b"\x00" * 74 + b"\n")				# Assume the flag is 74 chars long...

			f.readline()									# \n
			f.readline()									# \n
			f.readline()									# Here's your encrypted message, base64 encoded:

			flag = f.readline().strip()

			solve(flag)
