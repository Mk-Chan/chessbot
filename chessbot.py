import os
import math
import random

from irc import *

channel = "##chessprogramming"
server = "irc.freenode.net"
nickname = "qtpi"

irc = IRC()
irc.connect(server, channel, nickname)

STATIC_RESPONSES = {
    "hello": "Hello!",
    "bye": "Bye!"
}

def match(text):
    tsplit = text.split(" ")
    w, l, d = tsplit[1], tsplit[2], tsplit[3]
    try:
        w = int(w)
        l = int(l)
        d = int(d)
        assert w > 1 and l > 1 and d > 1
    except Exception:
        irc.send("Usage: .match <wins> <losses> <draws>. All values must be > 1\n")
        return

    n = float(w + l + d)
    w /= n
    l /= n
    d /= n
    m_mu = w + d / 2.0

    dev_w = w * pow(1.0 - m_mu, 2.0)
    dev_l = l * pow(0.0 - m_mu, 2.0)
    dev_d = d * pow(0.5 - m_mu, 2.0)
    m_std_dev = math.sqrt(dev_w + dev_l + dev_d) / math.sqrt(n)

    def diff(p):
        return -400.0 * math.log10(1.0 / p - 1.0)

    elo_diff = diff(m_mu)

    def erf_inv(x):
        pi = math.pi
        a = 8.0 * (pi - 3.0) / (3.0 * pi * (4.0 - pi))
        y = math.log(1.0 - x * x)
        z = 2.0 / (pi * a) + y / 2.0
        ret = math.sqrt(math.sqrt(z * z - y / a) - z)
        return ret if x >= 0.0 else -ret

    def phi_inv(p):
        return math.sqrt(2.0) * erf_inv(2.0 * p - 1.0)

    mu_min = m_mu + phi_inv(0.025) * m_std_dev
    mu_max = m_mu + phi_inv(0.975) * m_std_dev
    err = (diff(mu_max) - diff(mu_min)) / 2.0

    irc.send("Elo diff: " + str(round(elo_diff, 2)) + " ± " + str(round(err, 2)) + "\n")

def main():
    while True:
        text = irc.get_text()
        print(text)

        try:
            if "PRIVMSG" in text and channel in text:
                if ".match" in text:
                    text = text[text.find(".match"):]
                    match(text)
                    continue
                else:
                    for key in STATIC_RESPONSES.keys():
                        if key in text:
                            irc.send(STATIC_RESPONSES[key])
                            break
        except Exception as e:
            print(e)
            irc.send("Something failed...\n")

if __name__ == "__main__":
    main()
