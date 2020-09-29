#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

/* some OSes don't like huge reads */
#define READSIZE 4096

void error(char *msg)
{
  fputs(msg, stderr); fputc('\n', stderr);
  exit(EXIT_FAILURE);
}

void *map_and_read(void *map_target,
                   size_t map_size,
                   size_t read_offset,
                   char *filename)
{
  void *mapping;
  int fd;
  struct stat statbuf;
  off_t bytes_left;
  char *read_pos;
  ssize_t n;

  if ( (mapping = mmap(map_target, map_size, PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED,
                       -1, 0)) == MAP_FAILED)
    error("Could not map memory region.");
  
  if (  (fd = open(filename, O_RDONLY)) == -1)
    error("Could not open file.");
  
  if (fstat(fd, &statbuf) == -1)
    error("Could not stat file.");

  bytes_left = statbuf.st_size;
  read_pos = (char *)mapping + read_offset;

  while (bytes_left > 0)
    {
      n = read(fd, read_pos,
               (bytes_left < READSIZE ? bytes_left : READSIZE));
      
      if (n  == -1)
        error("Failed to read from file.");
      if (n == 0)               /* EOF reached */
        break;
      
      read_pos += n;
      bytes_left -= n;
    }

  if (close(fd) == -1)
    error("Could not close file.");

  return mapping;
}

#define ROP_BASE   (void *)0x37800000
#define ROP_SIZE           0x00800000
#define ROP_OFFSET         0

#define TAPE_BASE   (void *)0x39000000
#define TAPE_SIZE           0x01000000
#define TAPE_OFFSET         0x00800000

int main(int argc, char *argv[])
{
  void *rop_mapping,  *rop_start;
  void *tape_mapping, *tape_start;

  if (argc != 3)
    error("Usage: driver [ropfile] [tapefile].");

  rop_mapping  = map_and_read(ROP_BASE,  ROP_SIZE,  ROP_OFFSET,  argv[1]);
  tape_mapping = map_and_read(TAPE_BASE, TAPE_SIZE, TAPE_OFFSET, argv[2]);

  rop_start  = (char *)rop_mapping  + ROP_OFFSET;
  tape_start = (char *)tape_mapping + TAPE_OFFSET;

  asm("mov %1, %%ecx; \
       mov %0, %%esp; \
       ret"
      :
      : "r"(rop_start), "r"(tape_start));

  /* NOTREACHED */
  return 0;
}
