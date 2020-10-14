#!/usr/bin/env python3

from socket import getaddrinfo, socket

from gmpy2 import divm


def solve(p, cipher_1, cipher_2):
	flag_hex = divm(cipher_1, cipher_2, p).digits(16)
	print(bytes.fromhex(flag_hex).decode("ascii"))


if __name__ == "__main__":
	af, socktype, proto, canonname, sa = getaddrinfo("challenges.ctfd.io", 30181)[0]
	with socket(af, socktype, proto) as sock:
		sock.connect(sa)
		with sock.makefile() as f:
			f.readline()							# Welcome to the fail0verflow encryption service
			f.readline()							# Now generating keys...
			f.readline()							# Encrypting FLAG...
			f.readline()							# Our public key for today is:

			p = int(f.readline().split("=")[1])
			g = int(f.readline().split("=")[1])
			y = int(f.readline().split("=")[1])

			f.readline()							# \n
			f.readline()							# The encrypted flag is

			c1 = int(f.readline().split("=")[1])
			c2 = int(f.readline().split("=")[1])

			f.readline()							# \n
			f.readline()							# Send me a message to encrypt:

			sock.sendall(b"\x01\n")					# Message should have numeric value 1

			f.readline()							# Here's your encrypted message:

			d1 = int(f.readline().split("=")[1])
			d2 = int(f.readline().split("=")[1])

			solve(p, c2, d2)
