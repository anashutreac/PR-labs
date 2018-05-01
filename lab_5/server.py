import datetime
import socket
import threading
import random


def help_info(arrg):
    info = ''
    for key, value in command_descriptions.items():
        info += key + value + '\n'
    return info


def hello(arrg):
    return 'Hello '  + arrg + '! Nice to have a connection with you.'


def dice(arrg):
    return random.choice(['1', '2', '3', '4', '5', '6'])


def uptime(arrg):
    return str(datetime.datetime.now().time())


def flip(arrg):
    return random.choice(['Heads', 'Tails'])


def stop_server(arrg):
    server_socket.close()
    print('You finished the server session')
    return 'You finished the server session. Further commands won\'t work!'


def handle_commands(command, param):
    try:
        func = commands.get(command)
        if func is None:
            raise KeyError
        print(command, param)
        return func(param)
    except KeyError:
        # return find_similar_commands(command)
        return 'Wrong command Commander! Try once again or help!'


commands = {
    '/dice': dice,
    '/flip': flip,
    '/help': help_info,
    '/hello': hello,
    '/uptime': uptime,
    '/shut_down': stop_server
}


command_descriptions = {
    '/dice': '- virtually role the dice',
    '/flip': '- virtually flip a coin',
    '/help': ' - short usage description of the command',
    '/hello': '- hello Commander. Parameter : name',
    '/uptime': '- displays current system time',
    '/shut_down': '- shut down socket server, use carefully'

}

# We're using TCP/IP as transport
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to the given address and port
server_socket.bind(('127.0.0.1', 8080))


# Start listening on socket, maximum number of queued connections - 10
server_socket.listen(5)
print('Socket created successfully')


def process(client_message):
    param = ''
    message_arrg = client_message.strip().split(' ')
    if len(message_arrg) == 2:
        command, param = message_arrg
    elif len(message_arrg) == 1:
        command = message_arrg[0]
    else:
        return "Wrong command Commander! Your message should have the format /command <param> or /command. Try /help"
    return handle_commands(command, param)


# Function for handling connections. This will be used to create threads
def handle_client(connection):
    # infinite loop so that function do not terminate and thread do not end.
    while True:

        # Receiving from client
        data = connection.recv(1024)
        reply = process(data.decode()).encode()
        if not data:
            break

        connection.sendall(reply)

    # came out of loop
    connection.close()


# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    connection, address = server_socket.accept()
    print('Connected with ' + address[0] + ':' + str(address[1]))

    thread = threading.Thread(target=handle_client, args=(connection,))
    thread.start()

