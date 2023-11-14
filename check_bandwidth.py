from scapy.all import *

live=True 
if live:
    iterable=sniff(iface='eth0')
else:
    filename="../Cam_1_ps_replay.pcapng"
    iterable=rdpcap(filename)

attacker_ip="192.168.0.199"
victim_ip='192.168.0.131'

attacker_count=0
other_count=0

try:
    for pkt in iterable:
        if pkt.haslayer(IP):
            if pkt[IP].dst == victim_ip:
                if pkt[IP].src == attacker_ip:
                    attacker_count+=1
                else:
                    other_count+=1
except KeyboardInterrupt as e:
    pass 

print("occupied bandwidth", attacker_count/(attacker_count+other_count))
