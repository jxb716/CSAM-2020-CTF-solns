Obscurity I
===========

## Challenge info:

Our threat intelligence team has notified us of evidence that hackers have been searching popular search engines for secrets that may be accidently exposed on one of our web sites.
You've been tasked with reviewing the new sales and marketing dashboard application for any signs of mistakes made by developers that may lead to exposed secrets.
The new dashboard can be found here: http://challenges.matrix8.net/obscurity1/

## Solution:

Clicking the link revealed a simple jQuery/Boostrap site, none of the buttons worked and nothing interesting was in the source. Like Don't Git Me, checking robots.txt yielded a solid lead:
```
User-agent: *
Allow: /*.html$
Disallow: /*/data/*
Disallow: /secret/*
```
Inspecting the secret folder reveals a file with the name flag.txt which, unsurprisingly, contained the flag.
`Equifax{Never_put_secr3ts_in_rob0ts.txt}`
