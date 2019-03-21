import base64
import os
import socket

from communication_services.base import BaseCommunicationService

STATES = [EXPECTING_CAP, EXPECTING_AUTH, EXPECTING_CONFIRMATION, DONE] \
    = ["CAP", "AUTHENTICATE", "SASL", "DONE"]


class IRCService(BaseCommunicationService):
    name = "irc"
    active = False
    channel = None

    def _send(self, text: str):
        if text.find("PONG") == -1:
            print(f"SEND:{text}")
        self.irc.sendall(f"{text}\n".encode())

    def _recv(self):
        text = self.irc.recv(2040).decode("utf-8").strip("\r\n")

        if text.find("PING") != -1:
            self._send(f"PONG {text.split()[1]}")
        else:
            print(f"RECV:{text}")

        return text

    def __init__(self):
        server = os.getenv("IRC_SERVER")
        channel = os.getenv("IRC_CHANNEL")
        nickname = os.getenv("IRC_NICKNAME")
        username = os.getenv("IRC_USERNAME")
        password = os.getenv("IRC_PASSWORD")

        self.active = False
        self.channel = channel
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
        self._send(f"JOIN {self.channel}")

    def send(self, text) -> None:
        self._send(f"PRIVMSG {self.channel} :{text}")

    def recv(self) -> str:
        text = self._recv()
        text = text[text.find(":", 1) + 1:]
        return text

    def is_active(self) -> bool:
        return self.active
