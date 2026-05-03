CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -pedantic -O2

.PHONY: all clean run

all: server client

server: server.c
	$(CC) $(CFLAGS) -o $@ $<

client: client.c
	$(CC) $(CFLAGS) -o $@ $<

run: all
	./server &
	sleep 1
	./client
	wait

clean:
	rm -f server client
