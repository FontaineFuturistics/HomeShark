from math import floor
from time import strftime, localtime
import pyshark.packet.packet as pypacket
from modules.utils import get_dst, get_src

CONNECTION_TIMEOUT = 300 # Number of seconds it takes a connection to timeout

class Connection:

    def __init__(self, name: str, user_ip: str, server_ips: list[str], start_time: float):

        # Setup variables
        self.names = [name]
        self.user_ip = user_ip
        self.server_ips = server_ips

        # Constant starting variables
        self.end_time = 0
        self.volume = 0
        self.packet_count = 0
        self.is_alive = True
        
        # Set start time
        self.start_time = floor(start_time)

    def accept_packet(self, packet: pypacket.Packet) -> None:

        # update end time
        self.end_time = floor(float(packet.sniff_timestamp))

        # probably increase length correctly TODO: Check this
        self.volume += len(packet)

        # Increase packet count
        self.packet_count += 1

    def expand_server_ips(self, new_ips: list[str]) -> None:

        # Add new ips to the server ips list
        for ip in new_ips:
            if ip not in self.server_ips:
                self.server_ips.append(ip)

    def expand_name(self, new_name: str) -> None:

        # Add the new name if necessary
        if new_name not in self.names:
            self.names.append(new_name)

    # Return whether or not a packet is part of our connection
    def is_ours(self, packet: pypacket.Packet) -> bool:
        return (get_src(packet) in self.server_ips)
    
    # Check if a packet should be considered a new connection for us
    def is_new_connection(self, packet: pypacket.Packet) -> bool:

        # If this is a dns query, check if it has the same name as us
        if "DNS" in packet:
            return packet.dns.qry_name in self.names and ((floor(float(packet.sniff_timestamp)) - (self.end_time if self.end_time > self.start_time else self.start_time)) >= CONNECTION_TIMEOUT)
        else: # Otherwise just check the ip
            return get_src(packet) in self.server_ips and ((floor(float(packet.sniff_timestamp)) - (self.end_time if self.end_time > self.start_time else self.start_time)) >= CONNECTION_TIMEOUT)

    def is_dead(self, current_time: float) -> bool:

        return (floor(float(current_time) - (self.end_time if self.end_time > self.start_time else self.start_time)) >= CONNECTION_TIMEOUT)
    
    def getConnLen(self) -> str:

        return strftime('%Y-%m-%d %H:%M:%S', localtime(self.start_time))
    
    def __str__(self) -> str:
        if self.is_alive == True:
            return f"<div class='connectionDiv'><h4>{self.names}</h4><ul><li>Start Time: {self.start_time} ({strftime('%Y-%m-%d %H:%M:%S', localtime(self.start_time))})</li><li>End Time: {self.end_time} ({strftime('%Y-%m-%d %H:%M:%S', localtime(self.end_time))})</li><li>Run Time (sec): {self.end_time - self.start_time}</li><li>Size Down: {self.volume}</li><li>Server Ips: {self.server_ips}</li></ul></div>"
        return f"<div class='connectionDiv'><h4>{self.names} (Dead Connection)</h4><ul><li>Start Time: {self.start_time} ({strftime('%Y-%m-%d %H:%M:%S', localtime(self.start_time))})</li><li>End Time: {self.end_time} ({strftime('%Y-%m-%d %H:%M:%S', localtime(self.end_time))})</li><li>Run Time (sec): {self.end_time - self.start_time}</li><li>Size Down: {self.volume}</li><li>Server Ips: {self.server_ips}</li></ul></div>"