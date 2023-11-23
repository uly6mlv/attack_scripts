from main import launch_attack
import numpy as np
import time 
from attack_intensity import measure_response
from main import IP_DICT, TARGET_DICT, ATK_DICT, record_packets_at_pi

target=[6]
attacks=[9,5]

# benign
# with open('benign_response.csv','w') as f:
#     f.write("device,average rtt,loss\n")
#     for t in target:
#         print(f"profiling {TARGET_DICT[t]}")
#         rtt, percent_time=measure_response(30, IP_DICT[t])
#         f.write(f"{TARGET_DICT[t]},{np.mean(rtt)},{percent_time}\n")


# attacks
# with open('attack_response.csv','w') as f:
#     f.write("device,attack,intensity,average rtt,loss\n")
#     for t in target:
#         for a in attacks:
#             intensity=3000
#             percent_time=0
#             while percent_time<0.98:
#                 print(f"attacking {TARGET_DICT[t]} with {ATK_DICT[a].__name__} @ {intensity}")
#                 device, attack, rtt, percent_time=launch_attack(a, t, pps=intensity, time=30)
#                 f.write(f"{device},{attack},{intensity},{np.mean(rtt)},{percent_time}\n")

#                 print(f"{device},{attack},{intensity},{np.mean(rtt)},{percent_time}")
#                 intensity+=500
#                 #wait for flooding to finish
#                 time.sleep(20)


# replay attack files
# target=[6,1,3,4]
# attacks=["SYN_Flooding","ACK_Flooding","UDP_Flooding"]

# with open('replay_attack_response.csv','w') as f:
#     f.write("device,attack,intensity,average rtt,loss\n")
#     for t in target:
#         device=TARGET_DICT[t]
#         for a in attacks:
            
#             pcap_file=f"../Malicious/{device}/{device}_{a}.pcap"
#             print(f"replaying pcap_file")
#             device, attack,attack_pps, rtt, percent_time=launch_attack(10, t, pcap=pcap_file, loop=1, atk_name=a)
#             f.write(f"{device},{a},{attack_pps},{np.mean(rtt)},{percent_time}\n")

#             print(f"{device},{a},{attack_pps},{np.mean(rtt)},{percent_time}")
#             #wait for flooding to finish
#             time.sleep(20)


# replay adversarial attacks
target=[1,3,4]
attacks=["SYN_Flooding_iter_0","ACK_Flooding_iter_0","UDP_Flooding_iter_0"]

with open('replay_adv_attack_response.csv','w') as f:
    f.write("device,attack,intensity,average rtt,loss\n")
    for t in target:
        device=TARGET_DICT[t]
        for a in attacks:
            pcap_file=f"../Adversarial/{device}/{device}_{a}.pcapng"
            print(f"replaying {pcap_file}")
            device, attack,attack_pps, rtt, percent_time=launch_attack(10, t, pcap=pcap_file, loop=1, atk_name=a)
            f.write(f"{device},{a},{attack_pps},{np.mean(rtt)},{percent_time}\n")
            print(f"{device},{a},{attack_pps},{np.mean(rtt)},{percent_time}")
            #wait for flooding to finish
            time.sleep(20)

