#!/usr/bin/env python3

from math import isqrt


def legendre_symbol(a, p):
    """
    Legendre symbol
    Define if a is a quadratic residue modulo odd prime
    http://en.wikipedia.org/wiki/Legendre_symbol
    """
    ls = pow(a, (p - 1)//2, p)
    if ls == p - 1:
        return -1
    return ls

def prime_mod_sqrt(a, p):
    """
    Square root modulo prime number
    Solve the equation
        x^2 = a mod p
    and return list of x solution
    http://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm
    """
    a %= p

    # Simple case
    if a == 0:
        return [0]
    if p == 2:
        return [a]

    # Check solution existence on odd prime
    if legendre_symbol(a, p) != 1:
        return []

    # Simple case
    if p % 4 == 3:
        x = pow(a, (p + 1)//4, p)
        return [x, p-x]

    # Factor p-1 on the form q * 2^s (with Q odd)
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # Select a z which is a quadratic non resudue modulo p
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)

    # Search for a solution
    x = pow(a, (q + 1)//2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        # Find the lowest i such that t^(2^i) = 1
        i, e = 0, 2
        for i in xrange(1, m):
            if pow(t, e, p) == 1:
                break
            e *= 2

        # Update next value to iterate
        b = pow(c, 2**(m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return [x, p-x]

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# This finds a solution for c = x^2 (mod p^2)
def find_solution(c, n):
    '''
    Hensel lifting is fairly simple.  In one sense, the idea is to use
    Newton's method to get a better result.  That is, if p is an odd
    prime, and

                            r^2 = n (mod p),

    then you can find the root mod p^2 by changing your first
    "approximation" r to

                        r - (r^2 - n)/(2r) (mod p^2).

    http://mathforum.org/library/drmath/view/70474.html                    
    '''
    p = isqrt(n)

    # Get square roots for x^2 (mod p)
    r = prime_mod_sqrt(c,p)[1]

    inverse_2_mod_n = modinv(2, n)
    inverse_r_mod_n = modinv(r, n)

    new_r = r - inverse_2_mod_n * (r - c * inverse_r_mod_n)

    return new_r % n

if __name__ == "__main__":
    # These are the given values
    # n is a perfect square: n = p * p
    n = 0x5c243ba1024b0bf18597059a170d7ac339337c6ef19cfc3e8d911f264fac3b6c764ca606b49d61aecde0d28d20f84788af2086fcf57efaff4856e3a96221f4f1f175b5cd05ea45bbe659bc593b798c6d1f26fd29ca76e1a5c378c2e165091fb89abd494dc81dd380f3d25ce4ef4f04196ce4a6d34419e45a8d50f61c00f9b4b1

    # encrypted message
    c = 0x55b1a4826c83c1368cf4647d0183a340cf2c28757b44f0ab3c5d44eae825c21a28906a6b5e04cfcc5cb55bb6833dada76ce922c9e19985a3aed2d4f101052dcf85bd88c30dcfa08d197ba20f7c7b16cf233207619a6eed5f5387b0fb312c7bb8f9261b71bfa14f4728133e1b91b5d0d6ecac6a55f11496aab8cc96b61ef8e9d1

    soln = find_solution(c, n)
    print(bytes.fromhex(format(soln, "x")).decode("ascii"))
