
SOURCES= spec.c blocksort.c bzip2.c bzlib.c compress.c crctable.c \
	 decompress.c huffman.c randtable.c

CC=arm-linux-gnueabihf-gcc
CC=aarch64-linux-gnu-gcc
CFLAGS=-O0
COMP_FLAGS=-lm -DSPEC_CPU -DNDEBUG -static

all: $(SOURCES)
	$(CC) $(COMP_FLAGS) $(SOURCES) $(CFLAGS) -o specbzip



