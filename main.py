import threading
import modules.homeshark as homeshark
import modules.server as server
import modules.thread_monitor as thread_monitor

#Remember to setup monitor mode
# sudo airmon-ng stop wlan0
# sudo airmon-ng start wlan0

# Link to server: http://127.0.0.1:8080

# If you make threads and don't kill them, check with "ps"
# then kill them with "kill -9 <pid>"

if __name__ =="__main__":

    mon = thread_monitor.ThreadMonitor()

    t1 = threading.Thread(target=homeshark.start_capture, args=(mon,))
    t2 = threading.Thread(target=server.start_server, args=(mon,))
 
    t1.start()
    t2.start()

    input("press enter to kill")
    mon.kill()
    print("killing")

    t1.join()
    print("Homeshark killed")
    t2.join()
    print("Server killed")