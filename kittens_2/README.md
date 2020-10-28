Kittens II
==========

## Challenge info:

Continued reports from CyberOps have come in regarding unusual email traffic with photos of kittens attached. The scanners aren't finding anything wrong with these photos, but we're very suspicious that they're being used to exfiltrate data from our network. These seem, different, from the first set we discovered. Can you figure it out?

## Solution:

Checking the picture's metadata revealed no suspicious strings, and inspecting the picture itself did not suggest there may be data hidden in the picture itself, leaving the option of inspecting the raw image data. Opening the image in a [hex editor](https://hexed.it/) showed a suspicious string of bytes at the end of the file.
Given that the string started with the values 4571, the value 0x45 represents the letter "E" and the value 0x71 represents the letter "q", it was likely this string was the flag in hex, which was confirmed soon after:
```
$ python3 -c 'print(bytes.fromhex("457175696661787B486964696E675F46696C65735F696E5F30746865725F66696C65735F69735F436C337633727D").decode())'
Equifax{Hiding_Files_in_0ther_files_is_Cl3v3r}
```
