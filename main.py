import modules.homeshark as homeshark
import modules.server as server
import modules.thread_monitor as thread_monitor
import multiprocessing
from time import sleep

#Remember to setup monitor mode
# sudo airmon-ng stop wlan0
# sudo airmon-ng start wlan0

# Link to server: http://127.0.0.1:8080

# If you make threads and don't kill them, check with "ps"
# then kill them with "kill -9 <pid>"

if __name__ =="__main__":

    mon = thread_monitor.ThreadMonitor()

    # Get the capture device we are using (Default to wlan0)
    capture_device = input("Enter the device to capture on (-1 for default) ")

    if (capture_device == "-1"):
        capture_device = "wlan0"

    key = ""
    if input("is this a promiscuous mode capture? (y/n): ") == "y":
        key = input("Please enter the network password: ") + ":" + input("Please enter the network SSID: ")

    # Get how many packets to discard
    discard_base = int(input("For optimization, most non-DNS packets must be discarded, please enter a number to server as the discard base (A reasonably minimum is 10, with higher recommended for weaker systems): "))

    # Make the homeshark object
    hs = homeshark.HomeShark(mon, discard_base, key)

    p1 = multiprocessing.Process(target=hs.start_capture, args=(capture_device,))
    p2 = multiprocessing.Process(target=server.start_server, args=(mon,))
 
    p1.start()
    p2.start()

    input("Press enter at any time to end capture...\n")
    mon.kill()
    print("Killing")

    # Give processes a few second to close gracefully
    sleep(5)
    
    # Kill them
    p1.terminate()
    print("Homeshark killed")
    p2.terminate()
    print("Server killed")