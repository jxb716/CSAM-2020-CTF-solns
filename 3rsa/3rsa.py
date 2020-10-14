#!/usr/bin/env python3

from base64 import b64decode

from Crypto.PublicKey import RSA
from gmpy import invert, root


def solve(pk_a, c_a, pk_b, c_b, pk_e, c_e):
	n_a = pk_a.n
	n_b = pk_b.n
	n_e = pk_e.n

	N = n_a * n_b * n_e
	N_be = n_b * n_e						# N / n_a
	N_ae = n_a * n_e						# N / n_b
	N_ab = n_a * n_b						# N / n_e

	x_be = invert(N_be, n_a)
	x_ae = invert(N_ae, n_b)
	x_ab = invert(N_ab, n_e)

	cube_m = (c_a * N_be * x_be + c_b * N_ae * x_ae + c_e * N_ab * x_ab) % N
	m = bytes.fromhex(root(cube_m, 3)[0].digits(16)).decode("ascii")
	print(m)


def load_ct(path):
	with open(path, "rb") as f:
		return int.from_bytes(f.read(), "big")


def load_key(path):
	with open(path, "r") as f:
		return RSA.importKey(b64decode("".join(f.readlines()[1:-1])))


if __name__ == "__main__":
	pk_a = load_key("alice.pub")
	pk_b = load_key("bob.pub")
	pk_e = load_key("eve.pub")

	c_a = load_ct("alice.enc")
	c_b = load_ct("bob.enc")
	c_e = load_ct("eve.enc")

	solve(pk_a, c_a, pk_b, c_b, pk_e, c_e)
