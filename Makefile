CC := gcc
CFLAGS := -g -O -Wall

driver: driver.c

clean:
	-rm -f driver driver.o
