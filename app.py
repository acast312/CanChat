from Modules.ChatStream import Chat
import sys
import socket
import select
from thread import *


if __name__ == '__main__':
    config = {}
    execfile("config.conf", config)

    chat = Chat(config['PORT'])
    chat.main()