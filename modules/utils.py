import pyshark.packet.packet as pypacket

def get_src(packet: pypacket.Packet) -> str:

    try:
        return packet.ip.src
    except:
        try:
            return packet.wlan_aggregate.ip_src
        except:
            print("ip_src access failure")
            return ""
        
def get_dst(packet: pypacket.Packet) -> str:

    try:
        return packet.ip.dst
    except:
        try:
            return packet.wlan_aggregate.ip_dst
        except:
            print("ip_dst access failure")
            return ""
        
def epoch_time_diff(epoch_start_time: int, epoch_end_time: int) -> str:

    minutes = max((epoch_end_time - epoch_start_time) // 60, 0)
    seconds = max((epoch_end_time - epoch_start_time) % 60, 0)

    return f"{minutes}:{seconds:02}"

def list_join(strlist: list) -> str:

    output = ""

    for thing in list:
        output += thing

    return output