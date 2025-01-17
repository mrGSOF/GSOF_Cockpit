import  time

class Clock():
    def __init__(self):
        self.T0 = time.time()

    def tick(self, Fs=None, Ts=None):
        if Ts == None:
            Ts = 1.0/Fs
        self.T0 += Ts
        wait = self.T0 -time.time()
        if wait > 0.01:
            time.sleep(wait)
        wait = self.T0 -time.time()
        while (wait < 0.01) and (wait > 0.001):
            wait = self.T0 -time.time()
