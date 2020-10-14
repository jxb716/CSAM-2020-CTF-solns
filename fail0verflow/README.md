fail0verflow
============

## Challenge info:

There's an encryption service that gives us an encrypted flag every time we connect. Can you decrypt the flag?
Use your CTF shell to connect using Netcat: `nc challenges.ctfd.io 30181`

## Solution:

If you ran in gaming or security circles around 2010, you might recall the name fail0verflow as the group who made their bones by deducing Sony's PS3 codesigning key and subsequently breaking codesigning on the platform; this primed me to think the challenge would have something to do with some form of [DSA](https://en.wikipedia.org/wiki/Digital_Signature_Algorithm), but was actually a bit lower level.
The challenge was conducted through another encryption service a la XORcrypt, where you provide plaintext to be encrypted by the service:
```
$ nc challenges.ctfd.io 30181
Welcome to the fail0verflow encryption service
Now generating keys...
Encrypting FLAG...
Our public key for today is:
  p=26439493456868946823000752920207733687766459681950410735392417171547469745011680115579519539202948648307231574202383
  g=2327262786272467513118318009409751671336438234126341146008587813133804549884225715822791656668359702992649623219038
  y=23227065276775059029989828848838001548952266736988953759047039539205889068118466094424559176788565885260707592365168

The encrypted flag is
  c1=5309534021256164630442830064860206369242423039772347822589267111080386673133423977191934217740959489687025908858826
  c2=7354481695040497369661563152694560867839401729608936126960879494375107673711254484011495988576430774121840012109202

Send me a message to encrypt:
AAAA
Here's your encrypted message:
  C1=5309534021256164630442830064860206369242423039772347822589267111080386673133423977191934217740959489687025908858826
  C2=17785117593089593876088936540966642819495574392568069435471186248531331289500363912710121621257398735036576989054830

Bye!
```
Given that DSA only covers signing meant this challenge wasn't based on it, but DSA is based on ElGamal signatures, whose output looks a lot like that of  [ElGamal encryption](https://en.wikipedia.org/wiki/ElGamal_encryption), so let's shake that tree and see what falls out.
Eagle-eyed readers may have spotted that c1 for the encrypted flag and C1 for the encrypted plaintext are the same which, due to how the value is generated, means a value that is only supposed to be used once was actually used twice. When this happens, given you know the plaintext of one message encrypted using the key it is [trivial to recover the second](https://crypto.stackexchange.com/a/77223).

```
$ ./fail0verflow.py
Equifax{k3y_reuse_in_elgamal_iz_b4d_mmmm_k4y}
```
