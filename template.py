import subprocess
from logger import *

a_constant = 0


def host_discovery(target_ip, intensity, duration):
    log('Start', attack_type='1. Host Discovery')
    # EX) sudo nmap -sn 192.168.0.1/24
    attack_command = 'sudo nmap -sn ' + target_ip + '/24'
    attack_command_list_form = attack_command.split(' ')

    # subprocess.call(args, stin=None, stdout=None, stderr=None, shell=False, timeout=None)
    # EX) subprocess.call(['ls', '-al'])
    subprocess.call(attack_command_list_form)  # 명령어 실행시키는 함수
    log('Mid', attack_command)

    log('End', attack_type='1. Host Discovery')
