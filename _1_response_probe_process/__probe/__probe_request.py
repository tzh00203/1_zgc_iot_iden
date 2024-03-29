import socket


def send_tcp_request(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((ip, port))
        # 构建你的 TCP 请求数据
        request_data = b"GET / HTTP/1.0\r\n\r\n"

        # 发送 TCP 请求数据
        client_socket.sendall(request_data)

        # 接收响应数据
        response = client_socket.recv(4096)
        print("TCP Response:", response.decode())

    except socket.error as e:
        print("Socket error:", e)
    finally:
        client_socket.close()


def send_udp_request(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # 构建你的 UDP 请求数据
        request_data = b"Your UDP request data"
        
        # 发送 UDP 请求数据
        client_socket.sendto(request_data, (ip, port))
        
        # 接收响应数据
        response, addr = client_socket.recvfrom(4096)
        print("UDP Response:", response.decode())
    
    except socket.error as e:
        print("Socket error:", e)
    finally:
        client_socket.close()


# 要发送 TCP 请求的 IP 和端口
target_ip = "192.168.1.10"
target_port = 22 # 替换为实际的目标端口号

# 发送 TCP 请求
send_tcp_request(target_ip, target_port)
