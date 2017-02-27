import numpy as np
import pylab as py


class disSim(object):

    def __init__(self, taxFraction=0.05, limit=1, numberOfPlayers=int(1e4), endRound=int(1e1), startingPot=1e4, avgGain=.2, fluc=.4):
        self.numberOfPlayers = numberOfPlayers
        self.limit = limit              # The limit below which the plater is out
        self.taxFrac = taxFraction      # The fraction of earning that are taxed
        self.startingPot = startingPot  # Starting amount of each player
        self.avgGain = avgGain          # Expected fractional gain
        self.fluctuation = fluc         # Average fluctuation from average gain
        self.endRound = 1e3             # Number of itreations
        self.round = 0                  # Initial first round
        self.totals = np.zeros(self.numberOfPlayers) # The current amount of money of each player
        self.totals[:] = self.startingPot
        self.startSumTotal = np.sum(self.totals)
        self.sumTotal = self.startSumTotal



    def iterateStep(self):
        fractions = np.random.rand(self.numberOfPlayers)
        fractions[fractions>=.5] = 1 + self.avgGain + self.fluctuation
        fractions[fractions<.5] = 1 + self.avgGain - self.fluctuation
        self.totals *= fractions
        for total in self.totals:
            if (total < self.limit):
                total = 0
        self.sumTotal = np.sum(self.totals)
        self.totals *= self.startSumTotal / self.sumTotal
        self.sumTotal = np.sum(self.totals)
        self.tax()
        self.round += 1

    def run(self):
        while self.round < self.endRound:
            self.iterateStep()
        self.totals = np.sort(self.totals)

    def tax(self):
        """
        Tax everybody by some amount and distribute the total equally
        """
        taxedAmount = self.totals * self.taxFrac
        self.totals *= (1 - self.taxFrac)
        totalPot = np.sum(taxedAmount)
        reimbursement = totalPot / self.numberOfPlayers
        self.totals[:] += reimbursement

    def summary(self):
        print("Top 20% own {:.5f}% of the wealth".format(100 * np.sum(self.totals[int(self.numberOfPlayers * 0.8):])/self.sumTotal))

    def showDistribution(self):
        py.plot(np.arange(self.numberOfPlayers), self.totals)
        py.title("Distribution of wealth")
        py.xlabel("Player no.")
        py.ylabel("Total money")
        py.show()

    def showLogDistribution(self):
        py.semilogy(np.arange(self.numberOfPlayers), self.totals, label="TaxFrac={}\nAvgGain={}\nAvgFluc={}".format(self.taxFrac, self.avgGain, self.fluctuation))
        py.title("Distribution of wealth")
        py.xlabel("Player no.")
        py.ylabel("Total money")
        py.legend(loc="upper left")
        py.show()






if __name__ == "__main__":


    flucVals = np.array([0.1, 0.2, 0.3, 0.4])
    taxRates = np.array([0.01, 0.05, 0.1, 0.2, 0.4])

    for flucVal in flucVals:
        sims = [disSim(fluc=flucVal, taxFraction=taxRates[0]),
                disSim(fluc=flucVal, taxFraction=taxRates[1]),
                disSim(fluc=flucVal, taxFraction=taxRates[2]),
                disSim(fluc=flucVal, taxFraction=taxRates[3]),
                disSim(fluc=flucVal, taxFraction=taxRates[4])]
        py.figure()
        for i, sim in enumerate(sims):
            sim.run()
            py.semilogy(np.arange(sim.numberOfPlayers), sim.totals, label=r"TaxRate={}".format(taxRates[i]))
        py.title(r"Distribution of wealth for $fluc={}$".format(flucVal))
        py.xlabel("Player no.")
        py.ylabel("Total money")
        py.legend(loc="upper left")
        py.show()
