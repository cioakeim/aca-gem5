
SOURCES= lbm.c main.c

CC=arm-none-linux-gnueabihf-gcc
CC=aarch64-linux-gnu-gcc
CFLAGS=-O0
COMP_FLAGS=-DSPEC_CPU -DNDEBUG -static

all: $(SOURCES)
	$(CC) $(COMP_FLAGS) $(SOURCES) $(CFLAGS) -o speclibm -lm



