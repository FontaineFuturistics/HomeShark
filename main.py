import pyshark
import modules.web_tracker as web_tracker
import modules.app_tracker as app_tracker
import modules.gui as gui

# Remember to setup monitor mode
# sudo airmon-ng stop wlan0
# sudo airmon-ng start wlan0

# View the output:
# file:///home/kali/Documents/output.html

# Get the capture device we are using (Default to wlan0)
capture_device = input("enter the device to capture on (-1 for default) ")

if (capture_device == "-1"):
    capture_device = "wlan0"

# Create a new live capture
capture = pyshark.LiveCapture(interface=capture_device, display_filter="ip.dst == 192.168.1.0/16", # Ignoring all traffic that isn't inbound ip traffic
                              decryption_key="0a211ea90a276821c4abc90cb9b60bebc934685a90efd62a044dfa6c8fecf66f", # linksys psk
                              encryption_type="wpa-psk")

# Determine how many packets to capture
current_packet = 1
MAX_PACKET = 5_000

# Initialize the modules
modules = [web_tracker.Web_Tracker()]
modules.append(app_tracker.App_Tracker(modules[0]))

# Make gui
gui_obj = gui.GUI(modules, "output.html")

# Start capturing
#for packet in capture.sniff_continuously(packet_count=MAX_PACKET):
for packet in capture.sniff_continuously():

    # Print how far into the capture we are
    if current_packet % 100 == 0:

        # Print status to the console
        print(f"\r{current_packet:05}/{MAX_PACKET:05}")

        # Update the output file
        gui_obj.updateGUI()

    current_packet += 1

    for module in modules:
        module.accept_packet(packet)