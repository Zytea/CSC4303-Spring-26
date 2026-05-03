#define _POSIX_C_SOURCE 200809L

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080
#define BACKLOG 128
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
    printf("[server] socket(AF_INET, SOCK_STREAM, 0)\n");
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd < 0) {
        die("socket");
    }
    printf("[server] listenfd = %d\n", listenfd);

    int reuse = 1;
    if (setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        die("setsockopt");
    }

    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_port = htons(PORT);
    serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);

    printf("[server] bind(listenfd, 0.0.0.0:%d)\n", PORT);
    if (bind(listenfd, (struct sockaddr *)&serveraddr, sizeof(serveraddr)) < 0) {
        die("bind");
    }

    printf("[server] listen(listenfd, %d)\n", BACKLOG);
    if (listen(listenfd, BACKLOG) < 0) {
        die("listen");
    }

    struct sockaddr_in clientaddr;
    socklen_t clientlen = sizeof(clientaddr);

    printf("[server] accept(listenfd, ...) blocks here until a client connects\n");
    int connfd = accept(listenfd, (struct sockaddr *)&clientaddr, &clientlen);
    if (connfd < 0) {
        die("accept");
    }

    char client_ip[INET_ADDRSTRLEN];
    if (inet_ntop(AF_INET, &clientaddr.sin_addr, client_ip, sizeof(client_ip)) == NULL) {
        die("inet_ntop");
    }

    printf("[server] accept returned connfd = %d\n", connfd);
    printf("[server] peer = %s:%u\n", client_ip, ntohs(clientaddr.sin_port));

    char buf[BUF_SIZE];
    printf("[server] read(connfd, ...)\n");
    ssize_t nread = read(connfd, buf, sizeof(buf) - 1);
    if (nread < 0) {
        die("read");
    }
    if (nread == 0) {
        printf("[server] client closed before sending data\n");
    } else {
        buf[nread] = '\0';
        printf("[server] received %zd bytes: %s", nread, buf);

        const char prefix[] = "echo from server: ";
        printf("[server] write(connfd, ...)\n");
        write_all(connfd, prefix, strlen(prefix));
        write_all(connfd, buf, (size_t)nread);
    }

    printf("[server] close(connfd)\n");
    if (close(connfd) < 0) {
        die("close connfd");
    }

    printf("[server] close(listenfd)\n");
    if (close(listenfd) < 0) {
        die("close listenfd");
    }

    return 0;
}
