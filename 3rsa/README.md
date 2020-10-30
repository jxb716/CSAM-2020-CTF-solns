3RSA
====

## Challenge info:

I need to send my flag to three people securely. Using the public keys for Bob, Alice, and Eve, I encrypted my flag so they can decrypt it using their private keys. You'll never get my flag!

## Solution:

Back to RSA - I wonder if Ron Rivest ever thought of how much chicanery he would be tangentially involved in when he helped create RSA.

Anyway, initial inspection showed each key's modulus was coprime to the others, so recovering a private key likely wasn't required for this challenge. However, each key used a small exponent - 65537 is de rigueur, but 3 was the default exponent in most RSA key-generating software until 2015 or so. Using 3 as an encryption exponent doesn't create a security issue - unless you send the same message to multiple people.

Glossing over the internals of how RSA works, messages need to be numbers less than the modulus of the public key you encrypt it under - when you send the same message to multiple people it needs to be less than the smallest modulus of the public keys you encrypt it under. Assume a message is encrypted under three public keys with moduli `N`, `P`, `Q`, `N` being the smallest. If the message `m` is less than `N` then `m^3` must be less than `N^3` which must be less than `NPQ`. Thus if you can find `m^3 (mod NPQ)`, that's just `m^3` and you can take the cube root to recover `m`.

But how do you find `m^3 (mod NPQ)`? Thankfully the [Chinese Remainder Theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) will do exactly this, allowing recovery of the flag:
```
$ apt-get install libgmp3-dev libmpc-dev
$ pip3 install pycrypto
$ ./3rsa.py 
Equifax{rsa_broadcast_attack_got_me_good_e414e30}
```

P.S. A previous version of this challenge used much larger moduli so when you cubed the flag it didn't wrap around and you could take the cube root of the "ciphertext" without using the CRT and recover the flag; I was getting started on my CRT-based solution when someone brought it up in the comp channel - had they understood the implications of that fact I don't think they would've brought it up. If I had used better tools I probably would've been able to solve it using the larger moduli - my solution gave a flag that started with `Equifax{rsa` and had a bunch of garbage after.
