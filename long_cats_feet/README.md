Long Cat's Feet
===============

## Challenge info:

Long cat is missing his feet. Where did they go?

## Solution:

Viewing the image normal does not reveal anything to be out of order, save for the fact that the cat's feet are not in the picture. However, checking the file itself indicates something is going on:
```
$ pngcheck -vf longcat.png 
[stuff]
chunk IEND at offset 0x4de44, length 0
additional data after IEND chunk
```
Viewing the file at offset 0x4de44 in a [hex editor](https://hexed.it/) suggested there was an entirely separate PNG file hidden at the end of the first file; extracting the file with `pngcheck -x` yielded a picture of longcat's feet, and the flag.

![longcat's feet, with the flag: EFX{o_hai_ther_u_r}](feet.png)
