#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

int err(const char* str, ...) {
  va_list ap;
  va_start(ap, str);
  vfprintf(stderr, str, ap);
  va_end(ap);
  return 1;
}

char* search_end_loop(char* str) {
  int i = 1;

  while(i && *(++str)) {
    switch(*str) {
      case '[': i++; break;
      case ']': i--; break;
    }
  }

  return str;
}

char* search_begin_loop(char* str) {
  int i = 1;

  while(i && *(--str)) {
    switch(*str) {
      case '[': i--; break;
      case ']': i++; break;
    }
  }

  return str;
}

void eval(char* str) {
  int tape[30000];
  int head = 0;
  for (int i = 0; i<30000; i++) tape[i] = 0;
  while(*str) {
    switch(*str) {
      case '+': tape[head]++; break;
      case '-': tape[head]--; break;
      case '>': head++; break;
      case '<': head--; break;
      case '.': printf("%c", tape[head]); break;
      case ',': scanf("%c", (char*)&tape[head]); break;
      case '[': if(!tape[head]) str = search_end_loop(str); break;
      case ']': if(tape[head]) str = search_begin_loop(str); break;
    }
    ++str;
  }
}

int main(int argc, char** argv) {
  if (argc != 2) return err("usage: %s <filename>\n", argv[0]);

  FILE* f = fopen(argv[1], "rb");

  if (!f) return err("couldn’t open file %s.\n", argv[1]);

  fseek(f, 0, SEEK_END);
  long fsize = ftell(f);
  fseek(f, 0, SEEK_SET);

  char *string = malloc(fsize + 1);
  fread(string, fsize, 1, f);
  fclose(f);

  eval(string);

  free(string);

  return 0;
}
