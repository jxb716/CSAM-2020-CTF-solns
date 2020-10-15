Baby's Second Buffer Overflow
=============================

## Challenge info:

The program has been modified, but it's still vulnerable to a buffer overflow. Are you able to exploit it and get the flag?

Connect using your CTF shell using netcat: `nc challenges.ctfd.io 30183`

## Solution:

I figured things wouldn't be so easy twice, so I decided to look at the source code this time:

```c
int main(int argc, char **argv) {
	int canary = 0;
	char buf[64];
	char flag[128] = {0};

	loadflag(flag, sizeof(flag));

	printf("fixed the canary. now you can't overflow the buffer. haha! Give me some input!\n");
	fflush(NULL);
	_getline(buf);

	if (canary != 0xbaadf00d) {
	printf("nope. too bad.\n");
	} else {
	printf("you overflowed the buffer and changed the canary value!\nhere's your flag: %s\n", flag);
}
```
Now the objective is to set the canary to a certain value, which will require a buffer overflow to do so. Understanding how to do this requires a minimal understanding of the x86 architecture, so this is going to get very technical, very quick.

I don't know if this will make things more or less confusing, but I suggest visiting [Compiler Explorer](https://godbolt.org/) to get an actual look at how the executable is laid out in memory. Near the center-top of the screen is a dropdown with C++ selected; change it to C then overwrite the code in the box on the left with the code for the challenge. This will make a bunch of stuff appear on the right side.

Right-click on the line `int canary = 0;` and select "Reveal linked code". When you hover over the line on the left, a corresponding line should become highlighted on the right; that line shows where the value for `canary` is stored in the program. For me, the line reads `mov DWORD PTR [rbp-4], 0` which tells me the value of `canary` is stored at the address in the register rbp minus four bytes. Knowing what rbp represents isn't necessary here and I don't think I could explain it adequately well, if you want to know you can search for introductory x86 articles, or perhaps introductory binary exploitation articles for a CTF focus.

Now, right-click on the line `_getline(buf);` and select "Reveal linked code" again, hovering over it shows the preparations the computer makes before calling `_getline(buf)` including specifying the location of `buf` in memory. For me the important line reads `lea rax, [rbp-80]`, which means `buf` begins at the address in the register minus 80 bytes.

Now we know the difference between `buf` and `canary`, so we know we have to write 76 bytes (overflowing the buffer by 12 bytes) before writing the canary to get the flag. It is also important to know that x86 is a [little-endian architecture](https://en.wikipedia.org/wiki/Endianness#Current_architectures) so the canary will have to be written in reverse:
```
$ python -c 'print("A" * 76 + "\x0d\xf0\xad\xba")' | nc challenges.ctfd.io 30183
fixed the canary. now you can't overflow the buffer. haha! Give me some input!
you overflowed the buffer and changed the canary value!
here's your flag: Equifax{starting_to_become_a_buffer_overflow_pro}
```
P.S. I didn't do any of this; I assumed the memory layout of the programs in this challenge and its predecessor were similar since the code was, then I went back to Baby's First Buffer Overflow and, starting from 64, kept adding characters until I first changed the canary value. That let me know I had to write 76 bytes before I changed `canary`, and the rest was the same.
