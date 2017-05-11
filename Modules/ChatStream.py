import socket
import select
from thread import *
from Logger import Logger
from time import asctime
import sys

class Chat():

    def __init__(self, PORT):
        self.config = {}
        execfile("config.conf", self.config)

        print('PORT: {}'.format(PORT))

        self.NAMES = {}
        self.CONNECTIONS = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.config['HOST'], PORT))
        self.server_socket.listen(10)

        self.CONNECTIONS.append(self.server_socket)
        self.NAMES[self.server_socket] = 'SERVER'

        self.logger = Logger()

    def broadcast_data(self,sock, message):
        name = self.NAMES[sock]
        for socket in self.CONNECTIONS:
            if socket != self.server_socket and socket != sock:
                try:
                    socket.send('{}: {}'.format(name, message))
                except:
                    socket.close()
                    self.CONNECTIONS.remove(socket)

        log_file = open('bin/logs', 'aw')
        log_message = '{}: {}'.format(name, message)
        line = '<{}>{}'.format(asctime(),log_message)
        log_file.write(line)
        log_file.close()

    def create_name(self, sock):
        sock.send('Please Choose a nickname: ')
        name = sock.recv(128)
        name = name.replace('\n', '').replace('\r', '')
        self.NAMES[sock] = name
        self.broadcast_data(self.server_socket, 'User {} has joined the room \n'.format(name))
        pass

    def main(self):
        while True:
            print('running')
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTIONS, [], [])

            for sock in read_sockets:
                print(sock)
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.CONNECTIONS.append(sockfd)
                    start_new_thread(self.create_name, (sockfd,))

                else:
                    try:
                        message = sock.recv(self.config['MESSAGE_BUFFER'])
                        if message:
                            if message.replace('\n', '').replace('\r', '') == 'EXITCALL':
                                sock.close()
                                self.CONNECTIONS.remove(sock)
                                self.broadcast_data(self.server_socket,
                                                    "User {} has left the channel\n".format(self.NAMES[sock]))
                                break

                            if message.replace('\n', '').replace('\r', '') == 'GETLOGS':
                                log_file = open('bin/logs', 'r')
                                text = log_file.readlines()
                                log_file.close()
                                sock.send(''.join(text))
                                break

                            self.broadcast_data(sock, message)
                    except:
                        self.broadcast_data(sock, "User {} has left the channel\n".format(self.NAMES[sock]))
                        sock.close()
                        self.CONNECTIONS.remove(sock)
                        continue

    def exit(self):
        self.server_socket.close()