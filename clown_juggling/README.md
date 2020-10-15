Clown Juggling I
================

## Challenge info:

There's an app here that looks strange. Are you able to guess the correct password and login?
Connect to the app by browsing to: http://challenges.matrix8.net/clownjuggling1/

## Solution:

Visiting the linked site revealed a simple page with an image and form box. Nothing interesting is in the HTML source, however a link to the PHP source is provided.
```php
		<?php
			if( isset($_GET['password']) ) {
				if( strcmp($_GET['password'], $password) == 0 ) {
					echo "<div class=\"alert alert-success\" role=\"alert\">The flag is " . $flag . "</div>";
				} else {
					echo "<div class=\"alert alert-danger\" role=\"alert\">Invalid Password</div>";
				}
			}
		?>
```
So the goal of the challenge seems to be to determine the password, which is defined elsewhere, but there is nothing in either source file that provides any hint as to how to find the password. However, it would be good to remember that the page is written in PHP, and PHP is a [notoriously bad language](https://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/), so perhaps there is some language chicanery to take advantage of.
Checking the [PHP docs for strcmp](https://www.php.net/manual/en/function.strcmp.php) yields an interesting tidbit in the comments:
> If you rely on strcmp for safe string comparisons, both parameters must be strings, the result is otherwise extremely unpredictable

So it seems the goal is to make `$_GET['password']` something other than a string. The PHP docs say `$_GET` is just where the interpreter stores parameters from an incoming GET request, so there isn't much to do there, and trying to pass values like null bytes and integers did not succeed.
At this point I reached into my elite CTF background and went searching for solutions from people who completed similar CTF challenges, coming across [one](https://www.doyler.net/security-not-included/bypassing-php-strcmp-abctf2016) that looked pretty much identical, and granted the flag here:
```
$ curl -s -G -d 'password[]=%22%22' http://challenges.matrix8.net/clownjuggling1/ | grep flag
<div class="alert alert-success" role="alert">The flag is Equifax{type_juggling_can_really_mess_up_ur_day_if_youre_not_careful}</div>
```
P.S. I used `curl` here, but it wasn't necessary; you could have solved the challenge by visiting http://challenges.matrix8.net/clownjuggling1/?password[]=%22%22 in your browser
