import pyshark
import pyshark.capture
import modules.web_tracker as web_tracker
import modules.app_tracker as app_tracker
import modules.gui as gui
import modules.thread_monitor as thread_monitor
import pyshark.packet.packet as pypacket
from pyshark.capture.capture import StopCapture
from math import floor

class HomeShark:

    def __init__(self, mon: thread_monitor.ThreadMonitor, discard_base: int, key: str):

        # Initialize the modules
        self.modules = [web_tracker.Web_Tracker(discard_base)]
        self.modules.append(app_tracker.App_Tracker(self.modules[0], discard_base))

        self.mon = mon
        self.current_packet = 1
        self.gui_obj = gui.GUI(self.modules, "output.html")
        self.capture = None
        self.discard_base = discard_base
        self.key = key

    # Start capturing packets
    def start_capture(self, capture_device: str):

        if self.key =="": # If we don't have a key, don't use it

            # Create a new live capture
            self.capture = pyshark.LiveCapture(interface=capture_device, display_filter=f"ip.dst == 192.168.0.0/16 && (dns || frame.number % {self.discard_base} == 1)", # Ignoring all traffic that isn't inbound ip traffic
                                        ) # NOTE: This is a memory leak, tshark will eventually run out of ram and crash without reporting it to pyshark
                                        #       a potential fix would be to delete all .pcapng files in /tmp/ on a regular basis to prevent the leak

        else:

            # Create a new live capture
            self.capture = pyshark.LiveCapture(interface=capture_device, display_filter=f"ip.dst == 192.168.0.0/16 && (dns || frame.number % {self.discard_base} == 1)", # Ignoring all traffic that isn't inbound ip traffic
                                        decryption_key=self.key, # Using decryption based on users input
                                        encryption_type="wpa-pwd",
                                        ) # NOTE: This is a memory leak, tshark will eventually run out of ram and crash without reporting it to pyshark
                                        #       a potential fix would be to delete all .pcapng files in /tmp/ on a regular basis to prevent the leak
        
        # Process packets (stopping capture is handled by process_packet
        self.capture.apply_on_packets(self.process_packet)

        # Time to quit
        return

    # Start capturing
    def process_packet(self, packet: pypacket.Packet):

        # Set time in gui object
        self.gui_obj.time = floor(float(packet.sniff_timestamp))

        # If we need to exit, exit
        if self.mon.must_exit == True:
            raise StopCapture()

        # Print how far into the capture we are
        if self.current_packet % 100 == 1:

            # Print status to the console
            print(f"\r{self.current_packet - 1:05}", end="")

            # Update the output file
            self.gui_obj.updateGUI()

            # Tell web_tracker to kill dead packets
            self.modules[0].find_dead_connections(float(packet.sniff_timestamp))

        self.current_packet += 1

        for module in self.modules:
            if module.accept_packet(packet):
                break