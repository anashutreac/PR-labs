import socket

# We're using TCP/IP as transport
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the given `address` and `port`
server_address = ('127.0.0.1', 8080)
print('Connecting to 127.0.0.1:8080')
client_socket.connect(server_address)
try:
    # Read input from the user (as string)
    while 1:
        print('Enter a command:')
        data = input('>>')
        client_socket.sendall(data.encode())
        # Receive 1kB of data from the server
        data = client_socket.recv(1024)
        print('<<<:' + data.decode() + '\n')
finally:
    print('Closing socket')
    server_address.close()
a