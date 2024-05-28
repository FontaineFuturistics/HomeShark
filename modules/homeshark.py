import pyshark
import pyshark.capture
import modules.web_tracker as web_tracker
import modules.app_tracker as app_tracker
import modules.gui as gui
import modules.thread_monitor as thread_monitor
import pyshark.packet.packet as pypacket
from pyshark.capture.capture import StopCapture

class HomeShark:

    def __init__(self, mon: thread_monitor.ThreadMonitor):

        # Initialize the modules
        self.modules = [web_tracker.Web_Tracker()]
        self.modules.append(app_tracker.App_Tracker(self.modules[0]))

        self.mon = mon
        self.current_packet = 1
        self.gui_obj = gui.GUI(self.modules, "output.html")
        self.capture = None

    # Start capturing packets
    def start_capture(self, capture_device: str):

        # Create a new live capture
        self.capture = pyshark.LiveCapture(interface=capture_device, display_filter="ip.dst == 192.168.0.0/16 && (dns || frame.number % 10 == 1)", # Ignoring all traffic that isn't inbound ip traffic NOTE: Might drop eapol, not sure if its an issue
                                    #decryption_key="0a211ea90a276821c4abc90cb9b60bebc934685a90efd62a044dfa6c8fecf66f", # linksys psk
                                    #decryption_key="7bc9e287677511f0635b904643665f9fba4cd4f31995ef9671280ddae3efa6be", # nexus5g psk
                                    decryption_key="f1f93d02795d8db06ad2052852ae7f98ec769e4d3f0714888dc7a05a510bfee0", # nexus2g psk
                                    encryption_type="wpa-psk", 
                                    )
        
        # Process packets (stopping capture is handled by process_packet
        self.capture.apply_on_packets(self.process_packet)

        # Time to quit
        return

    # Start capturing
    def process_packet(self, packet: pypacket.Packet):

        # If we need to exit, exit
        if self.mon.must_exit == True:
            raise StopCapture()

        # Print how far into the capture we are
        if self.current_packet % 100 == 1:

            # Print status to the console
            print(f"\r{self.current_packet:05}", end="")

            # Update the output file
            self.gui_obj.updateGUI()

            # Tell web_tracker to kill dead packets
            self.modules[0].find_dead_connections(float(packet.sniff_timestamp))

        self.current_packet += 1

        for module in self.modules:
            if module.accept_packet(packet):
                break