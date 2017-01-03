#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char* argv[]) {
  int status;
  if (argc < 1) {
    printf("usage %s <executable> <arg1> <arg2> ...\n", argv[0]);
    exit(-1);
  }
  for(;;) {
    switch(fork()) {
      case 0 : //execute argv
        if (-1 == execvp(argv[1], argv+1)) {
          perror("exec");
          exit(-1);
        }
      break;
      case -1 : //error occured
        perror("fork");
        exit(-1);
      break;
      default : //we wait until the child is exited, and launched it again
        do {
          if ( -1 == wait(&status) ) {
            perror("wait");
            //maybe we should kill the child as well ?
            exit(-1);
          }
        } while( !WIFEXITED(status) );
    }
  }
  return 0;
}
