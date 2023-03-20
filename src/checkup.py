import datetime
import socket
import threading
from time import sleep
import logging

from pythonping import ping

# class Pinger:
#     def __init__(self, timeout=2, count=4, interval=0, verbose=False):
#         self.timeout = timeout
#         self.count = count
#         self.interval = interval
#         self.verbose = verbose

#     def ping_host(self, target):
#         return ping(target, timeout=self.timeout, count=self.count,
#                     interval=self.interval, verbose=self.verbose)


# class PortCheckup:
#     def __init__(self):


class DomainCheckup:
    def __init__(self, timeout=2, count=4, interval=0, max_threads=100, ping_verbose=False):
        self.timeout = timeout
        self.count = count
        self.interval = interval
        self.ping_verbose = ping_verbose
        self.max_threads = max_threads
        self.results = {}
        self.protocols = {"TCP": socket.SOCK_STREAM, "UDP": socket.SOCK_DGRAM}

    def dns_lookup(self, domain, port):
        return socket.getaddrinfo(domain, port)

    def ping_domain(self, target):
        self.results[target]['ping'] = ping(target,
                                            timeout=self.timeout,
                                            count=self.count,
                                            interval=self.interval,
                                            verbose=self.ping_verbose
                                            ).__dict__

    def check_port_availability(self, target, port):
        self.results[target]['ports'][port] = {}
        if port.isdigit() and 0 <= int(port) <= 65535:
            results = []
            for protocol_name, protocol in self.protocols.items():  # TCP, UDP
                sock = socket.socket(socket.AF_INET, protocol)
                socket.setdefaulttimeout(self.timeout)
                results.append(sock.connect_ex((target, int(port))))
                sock.close()
                if results[-1] == 0:
                    self.results[target]['ports'][port]["status"] = "OPEN"
                    self.results[target]['ports'][port]["type"] = protocol_name
                    return
            self.results[target]['ports'][port]["status"] = "CLOSED"
        else:
            self.results[target]['ports'][port]["status"] = "INVALID"
        self.results[target]['ports'][port]["type"] = "UNKNOWN"

    def __call__(self, checklist):
        for target, ports in checklist.items():
            if target is not None:
                self.results[target] = {}
                if ports is not None:
                    self.results[target]['ports'] = {}
                    for port in ports:
                        threading.Thread(target=self.check_port_availability,
                                         args=[str(target), port]).start()
                threading.Thread(target=self.ping_host,
                                 args=[target]).start()
            while threading.active_count() >= self.max_threads:
                sleep(1)
