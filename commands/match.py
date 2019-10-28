import math

from commands.base import BaseCommand
from utils import filtered_split


class Elo():
    def __init__(self, wins, losses, draws):
        self.wins = wins
        self.losses = losses
        self.draws = draws

    def erfInv(self, x):
        assert x < 1.0
        assert x > -1.0
        a = 8.0 * (math.pi - 3.0) / (3.0 * math.pi * (4.0 - math.pi))
        y = math.log(1.0 - x * x)
        z = 2.0 / (math.pi * a) + y / 2.0
        ret = math.sqrt(math.sqrt(z * z - y / a) - z)
        return ret if x >= 0.0 else -ret

    def phiInv(self, p):
        return math.sqrt(2.0) * self.erfInv(2.0 * p - 1.0)

    def diff(self, p):
        if p >= 1.0:
            return math.inf
        elif p <= 0.0:
            return -math.inf
        return -400.0 * math.log(1.0 / p - 1.0, 10)

    def elo(self):
        total = self.wins + self.losses + self.draws

        if total == 0:
            return math.nan

        m_mu = (self.wins + self.draws / 2.0) / total

        x = self.diff(m_mu)
        return 0.0 if x == -0.0 else x

    def err(self):
        total = self.wins + self.losses + self.draws

        if total == 0:
            return math.nan

        m_mu = (self.wins + self.draws / 2.0) / total

        w = self.wins / total
        l = self.losses / total
        d = self.draws / total

        devW = w * math.pow(1.0 - m_mu, 2.0)
        devL = l * math.pow(0.0 - m_mu, 2.0)
        devD = d * math.pow(0.5 - m_mu, 2.0)

        m_stdev = math.sqrt(devW + devL + devD) / math.sqrt(total)

        muMin = m_mu + self.phiInv(0.025) * m_stdev
        muMax = m_mu + self.phiInv(0.975) * m_stdev
        return (self.diff(muMax) - self.diff(muMin)) / 2.0

    def los(self):
        if self.wins + self.losses == 0:
            return math.nan
        return 100 * (0.5 + 0.5 * math.erf((self.wins - self.losses)/math.sqrt(2.0 * (self.wins + self.losses))))

    def drawRatio(self):
        total = self.wins + self.losses + self.draws

        if total == 0:
            return math.nan

        return self.draws / total


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

        if wins < 0 or losses < 0 or draws < 0:
            return " All values must be >= 0"

        elo = Elo(wins, losses, draws)

        return " ".join(["Elo diff:", str(round(elo.elo(), 2)),
                         "±", str(round(elo.err(), 2))])
