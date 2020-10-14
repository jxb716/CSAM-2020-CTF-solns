OTP
===

## Challenge info:

So XORcrypt really wasn't the super secure encryption service we thought it was. Well now we've got a brand new encryption service that's definitely more secure!
Connect using your CTF shell: `nc challenges.ctfd.io 30226`

## Solution:

The routine is pretty straightforward now, figure out how this service is broken and decrypt the flag:
```
Welcome to the OTP encryption service. Powered by the Mersenne Twister.
We're so confident in this service, we're giving away an encrypted flag!

The current date and time is: Wed Oct 14 19:55:02 2020
The encrypted flag, base64 encoded is: shURNuR9rOGj5N19fpV/74Wra1BM4hhDtlvF2ldcX7drFn3he8ZIHuvQo2EmRLA/D9G95i7PZUu9CurSWImH15+iQKBKOUw+DveDO+qg6mk0RQ==

Please input your message to encrypt: 
AAAA

Here's your encrypted message, base64 encoded: CWaTwA==
```
The [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister) is infamous in information security, as it generates a lot of numbers that look really random, so unwary developers will use it to generate numbers that need to be cryptographically secure only to find out when they have random Chinese and Russian people running around as admin that they unfortunately were not.
When I saw this was a Mersenne Twister challenge, I thought the challenge would be to generate enough output to reconstruct the PRNG state and use that to decrypt the flag, which is relatively easy as the common inclusion of the Mersenne Twister in CTFs means there are [many](https://github.com/altf4/untwister) [tools](https://github.com/eboda/mersenne-twister-recover) online to do this.
I started down this path until I noticed the inclusion of time and date, which actually meant the issue was much simpler - the random number generator was seeded using the time, which meant turning the timestamp back into an epoch timestamp was all that was necessary to reconstruct the PRNG state and decrypt the flag:
```
$ ./otp.py
Equifax{oops_didnt_use_a_cryptographically_secure_random_number_generator_e7339e8}
```

P.S. Suggesting the PRNG was seeded using the time while it was actually seeded securely and state computation actually was necessary would've been a _spectacular_ troll; I will keep that one in my pocket should I have to create a CTF challenge myself.