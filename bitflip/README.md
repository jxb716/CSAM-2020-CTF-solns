Bitflip
=======

## Challenge info:

We intercepted this file, but we can't make any sense of it. Can you help us?

## Solution:

Before engaging in any serious research into what this file could be, the first step is to ask if the computer knows what it is already:
```
$ file be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251 
be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251: data
```
Guess it doesn't. Next up is to see if there's potentially any text in the file that could provide a hint:
```
$ strings be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251 
flag.gzUT
i_ux
flag
O-K-
flag.gzUT
i_ux
```
Presumably handling this file will somehow lead to another file, `flag.gz`, which can be expanded to retrieve the flag. Now to begin looking at the file proper:
```
$ xxd be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251 
00000000: 514b 0304 0a00 0000 0000 2988 3551 8534  QK........).5Q.4
00000010: 7e1b 4300 0000 4300 0000 0700 1c00 666c  ~.C...C.......fl
00000020: 6167 2e67 7a55 5409 0003 9e14 695f 3915  ag.gzUT.....i_9.
00000030: 695f 7578 0b00 0104 f701 0000 0414 0000  i_ux............
00000040: 001f 8b08 089e 1469 5f00 0366 6c61 6700  .......i_..flag.
00000050: 732d 2ccd 4c4b aca8 4e8c 4fca 2c89 4fcb  s-,.LK..N.O.,.O.
00000060: c92c 884f 4ecc 8b4f ce48 cc4b 4f8d 4f2d  .,.ON..O.H.KO.O-
00000070: 4b2d aa2c c9c8 cc4b afe5 0200 00f1 de6f  K-.,...K.......o
00000080: 2a00 0000 504b 0102 1e03 0a00 0000 0000  *...PK..........
00000090: 2988 3551 8534 7e1b 4300 0000 4300 0000  ).5Q.4~.C...C...
000000a0: 0700 1800 0000 0000 0000 0000 a481 0000  ................
000000b0: 0000 666c 6167 2e67 7a55 5405 0003 9e14  ..flag.gzUT.....
000000c0: 695f 7578 0b00 0104 f701 0000 0414 0000  i_ux............
000000d0: 0050 4b05 0600 0000 0001 0001 004d 0000  .PK..........M..
000000e0: 0084 0000 0000 00                        .......
```
To continue requires knowledge of a practice that is interchangeably called magic bytes, magic numbers or simply file signatures. Essentially, in this situation a file signature is a collection of bytes at the beginning of a file that indicate what type fo file it is - for this file, the signature appears to be `QK`. Searching for "QK file signature" yielded no results, however there were many references to the signature for a Zipfile, which is "PK". A quick check confirms that the leters Q and P only differ by one bit and the name of the challenge is "Bitflip", so this looks to be a viable solution path. Making a quick check before moving forward confirms the hypothesis:
```
$ unzip -v be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251 
Archive:  be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
      67  Stored       67   0% 2020-09-21 21:01 1b7e3485  flag.gz
--------          -------  ---                            -------
      67               67   0%                            1 file
```
So now the goal is first to remove the flipped bit:
```
$ printf 'P' | dd of=be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251 bs=1 conv=notrunc   1+0 records in
1+0 records out
1 byte copied, 0.00116963 s, 0.9 kB/s
$ xxd be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251 
00000000: 504b 0304 0a00 0000 0000 2988 3551 8534  PK........).5Q.4
00000010: 7e1b 4300 0000 4300 0000 0700 1c00 666c  ~.C...C.......fl
00000020: 6167 2e67 7a55 5409 0003 9e14 695f 3915  ag.gzUT.....i_9.
00000030: 695f 7578 0b00 0104 f701 0000 0414 0000  i_ux............
00000040: 001f 8b08 089e 1469 5f00 0366 6c61 6700  .......i_..flag.
00000050: 732d 2ccd 4c4b aca8 4e8c 4fca 2c89 4fcb  s-,.LK..N.O.,.O.
00000060: c92c 884f 4ecc 8b4f ce48 cc4b 4f8d 4f2d  .,.ON..O.H.KO.O-
00000070: 4b2d aa2c c9c8 cc4b afe5 0200 00f1 de6f  K-.,...K.......o
00000080: 2a00 0000 504b 0102 1e03 0a00 0000 0000  *...PK..........
00000090: 2988 3551 8534 7e1b 4300 0000 4300 0000  ).5Q.4~.C...C...
000000a0: 0700 1800 0000 0000 0000 0000 a481 0000  ................
000000b0: 0000 666c 6167 2e67 7a55 5405 0003 9e14  ..flag.gzUT.....
000000c0: 695f 7578 0b00 0104 f701 0000 0414 0000  i_ux............
000000d0: 0050 4b05 0600 0000 0001 0001 004d 0000  .PK..........M..
000000e0: 0084 0000 0000 00                        .......
```
Then the internal file can be extracted and inflated itself:
```
$ unzip -p be10e8584b96c8434b5ade07e9f379b536af5c5a5805d94c8b2c7685d1085251 | gunzip -c
Equifax{a_bit_flip_can_change_everything}
```
