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

def byte_str(byts: int) -> str:

    if byts < 2048:
        return str(byts) + "B"
    
    # Make kb
    kbyts = byts // 1024
    if kbyts < 2048:
        return str(kbyts) + "KB"
    
    # Make MB
    mbyts = kbyts // 1024
    if mbyts < 2048:
        return str(mbyts) + "MB"
    
    # Make GB
    gbyts = mbyts // 1024
    return str(gbyts) + "GB"