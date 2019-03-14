import socket

import settings
from communication_services.base import BaseCommunicationService


class IRCService(BaseCommunicationService):
    name = "irc"
    init_params = [settings.IRC_SERVER, settings.IRC_CHANNEL, settings.IRC_NICKNAME]

    def __init__(self, server, channel, nickname):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((server, 6667))
        user = "USER " + nickname + " " + nickname + " " + nickname + " :Cool bot!\n"
        self.irc.sendall(user.encode())
        nick = "NICK " + nickname + "\n"
        self.irc.sendall(nick.encode())
        join = "JOIN " + channel + "\n"
        self.irc.sendall(join.encode())
        self.channel = channel

    def send(self, text) -> None:
        chan = self.channel
        text = "PRIVMSG " + chan + " :" + text + "\n"
        self.irc.sendall(text.encode())

    def recv(self) -> str:
        text = self.irc.recv(2040).decode("utf-8")[:-2]

        if text.find('PING') != -1:
            pong = 'PONG ' + text.split()[1] + '\r\n'
            self.irc.sendall(pong.encode())

        text = text[text.find(":", 1) + 1:]
        return text
