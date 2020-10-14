XORcrypt
========

## Challenge info:

There's a super secure encryption service available called XORCrypt. You just provide the data you want encrypted and it'll encrypt it! But something tells me they're lying when they say it's secure... can you recover the key?
Connect using netcat in your CTF shell: `nc challenges.ctfd.io 30130`


## Solution:

Since the challenge is called XORcrypt, there's a good chance that the service is using the [XOR cipher](https://en.wikipedia.org/wiki/XOR_cipher) to encrypt the given plaintext. Since the service says it encrypts plaintext with the flag, XORing the result from the service with the submitted plaintext should yield the flag, but a quicker method is to send a bunch of null bytes, which should yield the flag directly:

```
$ python -c 'print("\x00" * 74)' | nc challenges.ctfd.io 30130
Welcome to the XORcrypt encryption service
The most secure crypto service in the world!
Send me a message to encrypt with the secret flag:


Here's your encrypted message, base64 encoded:
RXF1aWZheHt4b3JfZW5jcnlwdGlvbl9pc250X3NlY3VyZV93aGVuX3lvdV9rbm93X3BsYWludGV4dF9hbmRfY2lwaGVydGV4dH0=

Bye!

$ echo -n RXF1aWZheHt4b3JfZW5jcnlwdGlvbl9pc250X3NlY3VyZV93aGVuX3lvdV9rbm93X3BsYWludGV4dF9hbmRfY2lwaGVydGV4dH0= | base64 -d
Equifax{xor_encryption_isnt_secure_when_you_know_plaintext_and_ciphertext}
```
