#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main() {
    // 创建 UDP socket
    int udp_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (udp_socket == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // 设置服务器地址和端口
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("目标IP地址");
    server_addr.sin_port = htons(目标端口号);

    // 发送 UDP 请求数据
    const char* request_data = "Your UDP request data";
    sendto(udp_socket, request_data, strlen(request_data), 0, (struct sockaddr*)&server_addr, sizeof(server_addr));

    // 关闭 socket 连接
    close(udp_socket);

    return 0;
}
