from scapy.all import * 

file1="../Cam_1_ps_replay.pcapng"
file2="../Cam_1_ps.pcapng"

source="192.168.0.151"
dest="192.168.0.199"
ignore_dest_port=True

def get_content(filename):
    a=rdpcap(filename)
    contents=[]
    for p in a:
        if p.haslayer(IP):
            if p[IP].src==source and p[IP].dst ==dest:
                if ignore_dest_port:
                    p[IP][TCP].dport=50025
                contents.append(str(p[IP].payload))
    return set(contents)

file1_cont=get_content(file1)
file2_cont=get_content(file2)

print(file1_cont)
print(file2_cont)

intersection=len(file1_cont&file2_cont)
union=len(file1_cont|file2_cont)
print(float(intersection)/union)

