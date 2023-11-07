from pythonping import ping
import time
from matplotlib import pyplot as plt
from tqdm import tqdm

host_ip="192.168.0.131"
response_time=0.1
rtt=[]

try:
    while True:
        response=ping(host_ip, count=1, timeout=response_time, verbose=False)
        rtt.append(response.rtt_avg_ms)
        time.sleep(response_time)
except KeyboardInterrupt as e:
    plt.plot(rtt)
    plt.savefig('pings.png')