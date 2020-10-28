Kittens I
=========

## Challenge info:

CyberOps has been getting reports of unusual email traffic patterns. These emails seem to all include attachments of kitten photos. The team is suspicious that these emails are being used to exfiltrate data from our network. Can you figure out how?

## Solution:

A quick glance at the picture's metadata revealed a base64-encoded string as the author if the image; decoding the string yielded the flag:
```
$ echo -n RXF1aWZheHtIaWRpbmdfZGF0YV9pbl9FWElGX2lzX0NsYSQkaWN9Cg== | base64 -d
Equifax{Hiding_data_in_EXIF_is_Cla$$ic}
```
