import socket
import sys


class IRC:

    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.channel = None

    def send(self, msg):
        chan = self.channel
        msg = "PRIVMSG " + chan + " :" + msg + "\n"
        self.irc.sendall(msg.encode())

    def connect(self, server, channel, botnick):
        print("connecting to:"+server)
        self.irc.connect((server, 6667))
        user = "USER " + botnick + " " + botnick + " " + botnick + " :Cool bot!\n"
        self.irc.sendall(user.encode())
        nick = "NICK " + botnick + "\n"
        self.irc.sendall(nick.encode())
        join = "JOIN " + channel + "\n"
        self.irc.sendall(join.encode())
        self.channel = channel

    def get_text(self):
        text = self.irc.recv(2040).decode("utf-8")[:-2]

        if text.find('PING') != -1:
            pong = 'PONG ' + text.split() [1] + '\r\n'
            self.irc.sendall(pong.encode())

        return text
