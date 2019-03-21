import base64
import socket

import settings
from communication_services.base import BaseCommunicationService

STATES = [EXPECTING_CAP, EXPECTING_AUTH, EXPECTING_CONFIRMATION, DONE] \
    = ["CAP", "AUTHENTICATE", "SASL", "DONE"]


class IRCService(BaseCommunicationService):
    name = "irc"
    init_params = [
        settings.IRC_SERVER, settings.IRC_CHANNEL, settings.IRC_NICKNAME,
        settings.IRC_USERNAME, settings.IRC_PASSWORD
    ]
    active = False
    channel = settings.IRC_CHANNEL

    def _send(self, text):
        print(f"SEND:{text}")
        text += "\n"
        self.irc.sendall(text.encode())

    def _recv(self):
        text = self.irc.recv(2040).decode("utf-8").strip("\r\n")
        print(f"RECV:{text}")

        if text.find('PING') != -1:
            self._send(f"PONG {text.split()[1]}\n")

        return text

    def __init__(self, server, channel, nickname, username, password):
        self.active = False
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc.connect((server, 6667))

        self._send("CAP REQ :sasl")
        self._send(f"NICK {nickname}")
        self._send(f"USER {username} {server} {nickname} :{nickname} {nickname}")

        curr_state = EXPECTING_CAP
        while curr_state != DONE:
            resp = self.irc.recv(2040).decode("utf-8").strip("\n\r")
            if not resp:
                continue
            print(resp)

            if str(curr_state) not in resp:
                continue

            if curr_state == EXPECTING_CAP:
                resp_split = resp.split(" ")
                if resp_split[1] != "CAP" or resp_split[2] != "*" \
                        or resp_split[3] != "ACK" or resp_split[4] != ":sasl":
                    print("Unexpected CAP response from server")
                    break

                self._send("AUTHENTICATE PLAIN")
                curr_state = EXPECTING_AUTH
            elif curr_state == EXPECTING_AUTH:
                resp_split = resp.split(" ")
                if resp_split[0] != "AUTHENTICATE" or resp_split[1] != '+':
                    print("Unexpected AUTH response from server")
                    break

                payload = f"{username}\0{username}\0{password}"
                settings.IRC_PASSWORD = "\0"
                payload_b64 = str(base64.b64encode(payload.encode("utf-8")), "utf-8")
                self._send(f"AUTHENTICATE {payload_b64}")
                curr_state = EXPECTING_CONFIRMATION
            elif curr_state == EXPECTING_CONFIRMATION:
                resp_split = resp[resp.find(str(EXPECTING_CONFIRMATION)) + 5:].split(" ")
                if resp_split[0] != "authentication" and resp_split[1] != "successful":
                    print("Unexpected SASL confirmation from server")
                    break
                self._send("CAP END")
                curr_state = DONE

        if curr_state != DONE:
            print("Failed to connect")
            return
        self.active = True
        self.irc.sendall(f"JOIN {channel}".encode())

    def send(self, text) -> None:
        self._send(f"PRIVMSG {self.channel} :{text}\n")

    def recv(self) -> str:
        text = self._recv()
        text = text[text.find(":", 1) + 1:]
        return text

    def is_active(self) -> bool:
        return self.active
