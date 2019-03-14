import math

from commands.base import BaseCommand
from utils import filtered_split


class Match(BaseCommand):
    name = "match"

    def help(self) -> str:
        return f"Usage: {self.name} <wins> <losses> <draws>"

    def run(self, arg) -> str:
        args = filtered_split(arg)
        if len(args) < 3:
            return "Wins, losses and draws must be provided in that order."
        wins, losses, draws = args[0], args[1], args[2]
        try:
            wins = int(wins)
            losses = int(losses)
            draws = int(draws)
        except ValueError:
            return " All values must be integers."

        if wins < 2 or losses < 2 or draws < 2:
            return "Wins, losses and draws must all be greater than 1."

        n = float(wins + losses + draws)
        wins /= n
        losses /= n
        draws /= n
        m_mu = wins + draws / 2.0

        dev_w = wins * pow(1.0 - m_mu, 2.0)
        dev_l = losses * pow(0.0 - m_mu, 2.0)
        dev_d = draws * pow(0.5 - m_mu, 2.0)
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

        return " ".join(["Elo diff:", str(round(elo_diff, 2)),
                         "±", str(round(err, 2))])
