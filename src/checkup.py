
import socket
import threading
from time import sleep

from pythonping import ping

import src.exception_handlers as exc


class DomainCheckup:
    def __init__(self, timeout=2, count=1, interval=0, max_threads=100,
                 start_thread_count=threading.active_count(), ping_verbose=False):
        self.timeout = timeout
        self.count = count
        self.interval = interval
        self.ping_verbose = ping_verbose
        self.max_threads = max_threads
        self.responses = {}
        self.protocols = {"TCP": socket.SOCK_STREAM, "UDP": socket.SOCK_DGRAM}
        self.start_thread_count = start_thread_count

    @exc.socket_exc
    def dns_lookup(self, domain, port=0):
        return [r[-1][0] for r in socket.getaddrinfo(domain, port) if not r[-1][0].startswith('::')]

    @exc.socket_exc
    def ping(self, domain, ip):
        r = ping(ip,
                 timeout=self.timeout,
                 count=self.count,
                 interval=self.interval,
                 verbose=self.ping_verbose
                 ).__dict__
        self.responses[domain][ip]['rtt_avg'] = r['rtt_avg']
        self.responses[domain][ip]['packet_loss'] = \
            1 - r['stats_packets_returned'] / r['stats_packets_sent']

    def check_port_availability(self, domain, ip, port):
        port_check_results = {port: {}}
        if port.isdigit() and 0 <= int(port) <= 65535:
            for protocol_name, protocol in self.protocols.items():  # TCP, UDP
                sock = socket.socket(socket.AF_INET, protocol)
                socket.setdefaulttimeout(self.timeout)
                res = sock.connect_ex((ip, int(port)))
                sock.close()
                if res == 0:
                    port_check_results[port]["status"] = "OPEN"
                    port_check_results[port]["type"] = protocol_name
                    self.responses[domain][ip]['ports'].append(
                        port_check_results)
                    return
            port_check_results[port]["status"] = "CLOSED"
        else:
            port_check_results[port]["status"] = "INVALID"
        port_check_results[port]["type"] = "UNKNOWN"
        self.responses[domain][ip]['ports'].append(port_check_results)

    def check_domain(self, domain, ports):
        self.responses[domain] = {}
        ips = self.dns_lookup(domain)
        if ips:
            for ip in ips:
                self.responses[domain][ip] = {}
                threading.Thread(target=self.ping,
                                 args=[domain, ip]).start()
                if ports is not None:
                    self.responses[domain][ip]['ports'] = []
                    for port in ports:
                        threading.Thread(target=self.check_port_availability,
                                         args=[domain, ip, port]).start()

        while threading.active_count() >= self.max_threads:
            sleep(1)

    def __call__(self, checklist):
        for domain, ports in checklist.items():
            if domain:
                self.check_domain(domain, ports)
        while threading.active_count() > self.start_thread_count:
            sleep(1)
        return self.responses
