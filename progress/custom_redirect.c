#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <dlfcn.h>
#include <arpa/inet.h>

int(*orig_socket)(int, int, int);

int socket(int domain, int type, int protocol) {
    // オリジナルのsocket関数をロード
    if(!orig_socket){
        orig_socket = dlsym(RTLD_NEXT, "socket");
    }
    // 実際のsocketを呼び出し
    int result = orig_socket(domain, type, protocol);

    // リダイレクト先のIPアドレスとポート
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(50000);  // リダイレクト先ポート
    inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);  // リダイレクト先IPアドレス

    // リダイレクト
    connect(result, (struct sockaddr*)&addr, sizeof(addr));

    return result;
}
