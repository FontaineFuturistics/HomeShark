import time
import datetime

class TimeKeeper:

    def __init__(self, fp: str):

        self.outfile = open(fp, "w")
        self.last_time = datetime.datetime.now()

    def log(self, log_msg: str) -> None:

        # Calc time since last log message
        current_time = datetime.datetime.now()

        # calc time diff
        diff = current_time - self.last_time

        # update last_Time
        self.last_time = current_time

        self.outfile.write(f'{diff.seconds}.{diff.microseconds:06} | {log_msg}\n')

    def close(self) -> None:
        self.outfile.close()

if __name__ == "__main__":

    tk = TimeKeeper()

    tk.log("tk started")

    time.sleep(0.5)

    tk.log("1")

    time.sleep(0.005)

    tk.log("2")

    time.sleep(2)

    tk.log("time to stop")