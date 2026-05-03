#define _POSIX_C_SOURCE 200809L

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 8080
#define BUF_SIZE 1024

static void die(const char *message)
{
    perror(message);
    exit(EXIT_FAILURE);
}

static void write_all(int fd, const void *buf, size_t len)
{
    const char *p = buf;

    while (len > 0) {
        ssize_t n = write(fd, p, len);
        if (n < 0) {
            if (errno == EINTR) {
                continue;
            }
            die("write");
        }

        p += n;
        len -= (size_t)n;
    }
}

int main(void)
{
    printf("[client] socket(AF_INET, SOCK_STREAM, 0)\n");
    int clientfd = socket(AF_INET, SOCK_STREAM, 0);
    if (clientfd < 0) {
        die("socket");
    }
    printf("[client] clientfd = %d\n", clientfd);

    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(SERVER_PORT);

    printf("[client] inet_pton(AF_INET, \"%s\", &serveraddr.sin_addr)\n", SERVER_IP);
    if (inet_pton(AF_INET, SERVER_IP, &serveraddr.sin_addr) <= 0) {
        die("inet_pton");
    }

    printf("[client] connect(clientfd, %s:%d) starts TCP handshake\n", SERVER_IP, SERVER_PORT);
    if (connect(clientfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) < 0) {
        die("connect");
    }
    printf("[client] connect returned; TCP channel is established\n");

    const char message[] = "hello from client\n";
    printf("[client] write(clientfd, ...)\n");
    write_all(clientfd, message, strlen(message));

    char buf[BUF_SIZE];
    printf("[client] read(clientfd, ...)\n");
    ssize_t nread = read(clientfd, buf, sizeof(buf) - 1);
    if (nread < 0) {
        die("read");
    }
    if (nread == 0) {
        printf("[client] server closed without replying\n");
    } else {
        buf[nread] = '\0';
        printf("[client] received %zd bytes: %s", nread, buf);
    }

    printf("[client] close(clientfd)\n");
    if (close(clientfd) < 0) {
        die("close clientfd");
    }

    return 0;
}
