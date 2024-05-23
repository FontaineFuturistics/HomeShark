class ThreadMonitor:

    def __init__(self):

        self.must_exit = False

    def kill(self) -> None:

        self.must_exit = True