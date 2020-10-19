Sweeeeet
========

## Challenge info:

There is a website that is currently under construction however, the website has some interesting cookies exposing some sweeeeetness. Can you find it?
Connect using your web browser to http://challenges.matrix8.net/sweeeeet/

## Solution:

Visiting the linked website doesn't reveal much, with nothing of interest in the source and no ancillary files such as robots.txt. The challenge primer indicates looking at the site's cookies to be beneficial, so inspecting them reveals a cookie named UID set to some random value. Clearing the cookie and reloading the page sets UID to the same value so the value likely refers to something specific. Changing the value of UID, or leaving it the value originally set, and reloading the page causes a second cookie named FLAG to appear, with the text `1t%275_n0t_7h4t_e45y`; presumably once the correct value of UID is found the FLAG cookie will actually contain the flag.

The initial assumption that UID was some encrypted value and needed to be set didn't hold up as there didn't appear to be a way to send plaintext to the site to be encrypted under some secret key, and no reasonable pad could be determined for use with XOR.

Operating under the assumption that the value of UID is a hash of something, a check for 128-bit hash functions revealed MD5, a common weak hashing algorithm used in many CTFs. Checking an [online MD5 reverse lookup service](http://reversemd5.com/) showed the value in UID is the MD5 digest of the string `100`; setting the value of UID to the MD5 digest of the string `0` yields the flag:
```
$ curl -s -c - -b UID=cfcd208495d565ef66e7dff9f98764da http://challenges.matrix8.net/sweeeeet/ | grep FLAG
challenges.matrix8.net  FALSE   /sweeeeet/      FALSE   0       FLAG    Equifax{4lwa4y5_ch3ck_7h3_c0Oki3s}
```
