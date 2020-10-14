All Your Base
=============

## Challenge info:

There's a weird looking message below. Can you help us figure out what this means?
`QmFzZTY0IGlzIGNvbW1vbmx5IHVzZWQgZm9yIGVuY29kaW5nIGRhdGEuIEVxdWlmYXh7eW91X3Nob3VsZF9yZWNvZ25pemVfYmFzZTY0X3N0cmluZ3N9Cg==`

## Solution:

This is just base64-encoded text:

```
$ echo -n "QmFzZTY0IGlzIGNvbW1vbmx5IHVzZWQgZm9yIGVuY29kaW5nIGRhdGEuIEVxdWlmYXh7eW91X3Nob3VsZF9yZWNvZ25pemVfYmFzZTY0X3N0cmluZ3N9Cg==" | base64 -d
Base64 is commonly used for encoding data. Equifax{you_should_recognize_base64_strings}
```
