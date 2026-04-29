import random

# =========================
# QUEUE
# =========================
class Queue:
    def __init__(self):
        self.data = []

    def isEmpty(self):
        return len(self.data) == 0

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        if not self.isEmpty():
            return self.data.pop(0)

    def size(self):
        return len(self.data)


# =========================
# PASSENGER
# =========================
class Passenger:
    def __init__(self, time):
        self._timeArrived = time

    def timeArrived(self):
        return self._timeArrived


# =========================
# AGENT (PETUGAS)
# =========================
class Agent:
    def __init__(self):
        self._busy = False
        self._finishTime = 0

    def isFree(self):
        return not self._busy

    def startService(self, passenger, finishTime):
        self._busy = True
        self._finishTime = finishTime

    def isFinished(self, currentTime):
        return self._busy and currentTime >= self._finishTime

    def stopService(self):
        self._busy = False


# =========================
# SIMULATION
# =========================
class TicketCounterSimulation:
    def __init__(self, numAgents, numMinutes, arrivalProb, serviceTime):
        self._passengerQ = Queue()
        self._theAgents = [Agent() for _ in range(numAgents)]

        self._numMinutes = numMinutes
        self._arriveProb = arrivalProb
        self._serviceTime = serviceTime

        self._totalWaitTime = 0
        self._numPassengers = 0

    # =========================
    # PENUMPANG DATANG
    # =========================
    def _handleArrival(self, curTime):
        if random.random() <= self._arriveProb:
            passenger = Passenger(curTime)
            self._passengerQ.enqueue(passenger)
            self._numPassengers += 1

    # =========================
    # MULAI LAYANAN
    # =========================
    def _handleBeginService(self, curTime):
        for agent in self._theAgents:
            if agent.isFree() and not self._passengerQ.isEmpty():
                passenger = self._passengerQ.dequeue()
                agent.startService(passenger, curTime + self._serviceTime)

                waitTime = curTime - passenger.timeArrived()
                self._totalWaitTime += waitTime

    # =========================
    # SELESAI LAYANAN
    # =========================
    def _handleEndService(self, curTime):
        for agent in self._theAgents:
            if agent.isFinished(curTime):
                agent.stopService()

    # =========================
    # RUN SIMULASI
    # =========================
    def run(self):
        for currentTime in range(self._numMinutes):
            self._handleArrival(currentTime)
            self._handleEndService(currentTime)
            self._handleBeginService(currentTime)

        self._printResults()

    # =========================
    # HASIL
    # =========================
    def _printResults(self):
        print("=== HASIL SIMULASI ===")
        print("Total penumpang:", self._numPassengers)

        if self._numPassengers > 0:
            avgWait = self._totalWaitTime / self._numPassengers
            print("Rata-rata waktu tunggu:", round(avgWait, 2))
        else:
            print("Tidak ada penumpang")

        print("Sisa antrian:", self._passengerQ.size())


# =========================
# MAIN PROGRAM
# =========================
if __name__ == "__main__":
    sim = TicketCounterSimulation(
        numAgents=2,      # jumlah petugas
        numMinutes=20,    # waktu simulasi
        arrivalProb=0.3,  # peluang kedatangan
        serviceTime=3     # waktu pelayanan
    )

    sim.run()