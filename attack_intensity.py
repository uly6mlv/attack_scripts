from pythonping import ping 
import time 
from matplotlib import pyplot as plt 
import numpy as np
import threading
from threading import Thread


class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def ping_wrapper(host_ip, count, timeout, verbose):
    response=ping(host_ip, count=count, verbose=verbose)
    return response.rtt_avg_ms

def measure_response(duration, host_ip):
    response_time=0.1
    rtt=[]
    start_time=time.time()
    while True:
        ping_thread=ThreadWithReturnValue(target=ping_wrapper, args=(host_ip, 1, response_time, False))
        ping_thread.start()
        av_rt=ping_thread.join(response_time)
        if av_rt is None:
            av_rt=response_time*1000

        rtt.append(av_rt)

        time.sleep(max(0,(response_time-av_rt/1000.)))
        
        if time.time() - start_time >= duration:
            break
    rtt=np.array(rtt)
    not_responding=np.count_nonzero((response_time*1000-rtt)<1e-4)
    percent_time=not_responding/len(rtt)
    # print(f"{percent_time*100:.3f}% non-responsive packets @ {response_time}")
    # print(f"average response time {np.mean(rtt)}ms")
    return rtt, percent_time
    
if __name__=="__main__":
    print(measure_response(30, "192.168.0.131"))