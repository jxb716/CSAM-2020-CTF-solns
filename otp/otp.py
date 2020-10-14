#!/usr/bin/env python3

from base64 import b64decode
from datetime import datetime
from socket import getaddrinfo, socket
from random import Random, randint

def solve(flag, c, timestamp):
	# SHOUT OUT TO srand(time(NULL))
	r = Random(timestamp)

	print("".join(chr(c ^ r.randint(0, 255)) for c in flag))

if __name__ == "__main__":
	af, socktype, proto, canonname, sa = getaddrinfo("challenges.ctfd.io", 30226)[0]
	with socket(af, socktype, proto) as sock:
		sock.connect(sa)
		with sock.makefile() as f:
			f.readline()									# Welcome to the OTP encryption service
			f.readline()									# We're so confident in this service
			f.readline()									# \n

			time_str = f.readline().split(": ")[1].strip()	# 
			flag = f.readline().split(": ")[1]				#

			f.readline()									# \n
			f.readline()									# Please input your message to encrypt:

			sock.sendall(b"\x00" * 2500 + b"\n")			# 625 32-bit ints

			f.readline()									# \n
			c = f.readline().split(":")[1].strip()

			#print(f"timestamp: {timestamp}\nflag: {flag}\nc: {c}")

			# Convert timestamp to epoch time
			timestamp = int(datetime.strptime(time_str, "%a %b %d %H:%M:%S %Y").timestamp())
			solve(b64decode(flag), b64decode(c), timestamp)
