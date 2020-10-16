#include <stdio.h>
#include <stdlib.h>

// Let's define a grammar for esoteric:

// prog  := expr*
// expr  := token | ( expr* )
// token := + | - | } | { | !

// increment   ->  +
// decrement   ->  -
// shift right ->  }
// shift left  ->  {
// print char  ->  !
// open loop   ->  (
// close loop  ->  )

typedef enum {
	TOK_PROG,		// beginning of program 
	TOK_CELL_INC,  	// ++*p
	TOK_CELL_DEC, 	// --*p
	TOK_IP_INC, 	// ++p
	TOK_IP_DEC, 	// --p
	TOK_PRINT_CHAR, // putchar(p)
	TOK_LOOP, 		// start loop
	TOK_LOOP_END,	// close loop
	TOK_LOOP_START,	// loop start
	TOK_COMMENT		// for all other chars; won't be used in our AST
} tok_type;

struct node {
	tok_type type;
	struct node *parent;
	struct node *body;
	struct node *prev;
	struct node *next;
};



struct node * node_create(tok_type type, struct node *parent, struct node *body, struct node *prev, struct node *next) {
	struct node *n = malloc(sizeof(struct node));
	if (n == NULL) {
		printf("cannot allocate mem fam :(\n");
		exit(1);
	}
	n->type = type;
	n->parent = parent;
	n->body = body;
	n->prev = prev;
	n->next = next;
	return n;
}

struct node * node_append(struct node *prev, struct node *next) {
	prev->next = next;
	next->prev = prev;
	return next;
}

tok_type get_type(char c) {
	switch(c) {
		case '+': 	return TOK_CELL_INC;
		case '-':	return TOK_CELL_DEC;
		case '}':	return TOK_IP_INC;
		case '{':	return TOK_IP_DEC;
		case '!':	return TOK_PRINT_CHAR;
		case '(':	return TOK_LOOP;
		case ')':	return TOK_LOOP_END;
		default:	return TOK_COMMENT;
	}
}

void flag(char *buf) {
	FILE *flag = fopen("flag", "r");
	char c;
	while ((c = fgetc(flag)) && c != EOF) *buf++ = c;
	fclose(flag);
	*buf = '\n';
}

void print_ast(struct node *prog, int indent) {
	while (prog != NULL) {
		for (int i=0; i<indent; i++) printf("  ");
		switch (prog->type) {
			case TOK_PROG:			printf("TOK_PROG\n"); 		break;
			case TOK_CELL_INC:		printf("TOK_CELL_INC\n"); 	break;
			case TOK_CELL_DEC: 		printf("TOK_CELL_DEC\n"); 	break;
			case TOK_IP_INC:		printf("TOK_IP_INC\n"); 	break;
			case TOK_IP_DEC:		printf("TOK_IP_DEC\n"); 	break;
			case TOK_PRINT_CHAR:	printf("TOK_PRINT_CHAR\n"); break;
			case TOK_LOOP:			printf("TOK_LOOP\n"); 		print_ast(prog->body, indent + 1); break;
			case TOK_LOOP_START:	printf("TOK_LOOP_START\n"); break;
			case TOK_LOOP_END:		printf("TOK_LOOP_END\n"); 	break;
			default:				printf("TOK_COMMENT\n"); 
		}
		prog = prog->next;
	}
}


struct node * build_ast(FILE *fd) {
	struct node *prog = node_create(TOK_PROG, NULL, NULL, NULL, NULL);
	struct node *current_node = prog;
	unsigned int loop = 0;
	tok_type type;
	char c;
	
	do {
		c = fgetc(fd);
		type = get_type(c);

		// we don't want nodes for comments or the ending loop
		if (!(type == TOK_COMMENT)) {
			struct node *new = node_create(type, NULL, NULL, current_node, NULL);
			current_node = node_append(current_node, new);
		}

		if (type == TOK_LOOP) {
			++loop;
			// Make a new list of nodes for the loop body
			current_node->body = node_create(TOK_LOOP_START, current_node, NULL, NULL, NULL);
			current_node = current_node->body;
		}

		if (type == TOK_LOOP_END) {
			--loop;
			if (loop < 0) break;
			// Move to the beginning of the loop body
			while (current_node->prev != NULL) current_node = current_node->prev;
			// And set the current node to the loop open
			current_node = current_node->parent;
		}

	} while (c != '\n');

	if (loop != 0) {
		printf("Unmatched brackets. I won't have it. Bye.\n");
		exit(1);
	}

	return prog;
}

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

void clean_ast(struct node *prog) {
	while (prog != NULL) {
		if (prog->body != NULL) clean_ast(prog->body);
		struct node *next = prog->next;
		free(prog);
		prog = next;
	}
}

int main(int argc, char **argv) {
	setbuf(stdout, 0);
	printf("esoteric REPL v0.1\n> ");

	struct node *prog;
	while (1) {
		prog = build_ast(stdin);
		if (prog != NULL && prog->next == NULL) break;
		if (argc > 1) print_ast(prog, 0);
		run_ast(prog);
		printf("> ");
		clean_ast(prog);
	}

	printf("bye\n");
	return 0;
}
