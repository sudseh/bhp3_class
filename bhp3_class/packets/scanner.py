from bhp3_class.packets import IP, ICMP
import ipaddress
import socket
import sys
import threading
import time

SUBNET = '10.253.221.0/24'
MESSAGE = 'RUBYRULES!'

def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 65212))
            

class Scanner:
    def __init__(self, host):
        self.host = host
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        self.socket.bind((host, 0))
        
    def sniff(self):
        hosts_up = [f'{str(self.host)} *']
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)
                    
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(SUBNET):
                            if raw_buffer[len(raw_buffer) - len(MESSAGE): ] == bytes(MESSAGE, 'utf8'):
                                hosts_up.append(str(ip_header.src_address))
                                print(f'Host Up: {str(ip_header.src_address)}')
        # handle CTRL-C
        except KeyboardInterrupt:
            print('User interrupted.')
            if hosts_up:
                print(f'\n\nSummary: Hosts up on {SUBNET}')
            for host in sorted(hosts_up):
                print(f'{host}')
            print('')
            sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '10.253.221.135'
    s = Scanner(host)
    time.sleep(1)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()