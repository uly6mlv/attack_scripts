from main import launch_attack
import numpy as np
import time 
from attack_intensity import measure_response
from main import IP_DICT, TARGET_DICT, ATK_DICT

target=[6]
attacks=[9,5]

# benign
# with open('benign_response.csv','w') as f:
#     f.write("device,average rtt,loss\n")
#     for t in target:
#         print(f"profiling {TARGET_DICT[t]}")
#         rtt, percent_time=measure_response(30, IP_DICT[t])
#         f.write(f"{TARGET_DICT[t]},{np.mean(rtt)},{percent_time}\n")


#attacks
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


# replay SmartTV_SYN_Flooding_iter_0
device, attack, rtt, percent_time=launch_attack(10, 6, pcap="../attack/SmartTV_SYN_Flooding_iter_0.pcapng", loop=1, time=30)
print(device, attack, np.mean(rtt), percent_time)


# device, attack, rtt, percent_time=launch_attack(9, 6, pps=17000, time=30)
# print(device, attack, np.mean(rtt), percent_time)