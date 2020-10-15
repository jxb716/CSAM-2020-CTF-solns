#include <stdio.h>

void _getline(char *buf) {
  char c;
  int i = 0;
  while ((c=getchar())&&c!='\n') buf[i++] = c;
}

// You can ignore `loadflag'. Its only purpose is to load the flag from a file into memory, and
// doesn't have anything related to the vulnerability in this program.
void loadflag(char *buf, int size) {
  FILE *f = fopen("flag", "r");
  char c;
  int i=0;
  while((c=fgetc(f))&&c!=EOF&&i<size) buf[i++] = c;
  fclose(f);
}

int main(int argc, char **argv) {
  int canary = 0xbaadf00d;
  char buf[64];
  char flag[128] = {0};

  loadflag(flag, sizeof(flag)-1);

  printf("Can you perform your first buffer overflow? Give me some input!\n");
  fflush(NULL);
  _getline(buf);
  
  if (canary == 0xbaadf00d) {
    printf("nope. too bad.\n");
  } else {
    printf("you overflowed the buffer and changed the canary value!\nhere's your flag: %s\n", flag);
  }

  return 0;
}
