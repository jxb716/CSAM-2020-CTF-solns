Kittens III
===========

## Challenge info:

OK, it seems that the cyber criminals have really stepped up their game. We really need to figure out how these images are being used to exfiltrate data! Can you help?!

## Solution:

Like in the previous challenge there were no leads in the image metadata or the image itself, but inspecting the raw data in a [hex editor](https://hexed.it/) suggested the presence of additional data. The fact the string `PK` appears multiple times in the appended data suggested the appended data was a zip file, which was confirmed after extracting and testing the data:
```
$ dd if=kitty-45623d.jpg of=flag.zip skip=2186912 count=240 bs=1 && printf 'P' | dd of=flag.zip bs=1 conv=notrunc && unzip -v flag.zip
Archive:  flag.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
      46  Stored       46   0% 2020-10-26 02:53 7ca0e59b  flag.txt
--------          -------  ---                            -------
      46               46   0%                            1 file
```
However, things can't be so easy:
```
$ unzip flag.zip 
Archive:  flag.zip
[flag.zip] flag.txt password:
```
There was no obvious password in any previously-inpected location, so it would seem more intense efforts to find the password would be necessary. Initial efforts to find a hidden password using `strings` were unsuccessful, so the plan shifted to check if the password is a common one by using wordlists. A combination of [John the Ripper](https://github.com/openwall/john) and the [RockYou wordlist](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) allowed for successful recovery of the password followed closely by the flag:
```
$ jtr/run/zip2john flag.zip > flag.john && jtr/run/john --wordlist=rockyou.txt flag.john
monkey42         (flag.zip/flag.txt)
1g 0:00:00:00 DONE (2020-10-28 15:40) 12.50g/s 1256Kp/s 1256Kc/s 1256KC/s mylove19..monbebe
Session completed.

$ unzip -P monkey42 -p flag.zip 
Equifax{Steganography_3xfiltration_is_Scary!}
```
