import pandas as pd
import json
from datetime import datetime

from datetime import datetime


class Writer:
    def __init__(self, filename='res.json'):
        self.filename = filename

    def __call__(self, data):
        with open(self.filename, 'w+') as outfile:
            json.dump(data, outfile)

    # def to_csv(self, data):
    #     print(data)
    #     export_dict = {'domain': [], 'ip': [], 'port': [], 'port_status': [],
    #                    'port_type': [], 'rtt_avg': [], 'packet_loss': []}
    #     for domain, domain_data in data.items():
    #         if domain_data:
    #             for ip, ip_data in domain_data.items():
    #                 if "ports" in ip_data.keys():
    #                     for ports_data in ip_data['ports']:
    #                         for port, port_data in ports_data.items():
    #                             export_dict['domain'].append(domain)
    #                             export_dict['ip'].append(ip)
    #                             export_dict['port'].append(port)
    #                             export_dict['port_status'].append(
    #                                 port_data['status'])
    #                             export_dict['port_type'].append(
    #                                 port_data['type'])
    #                             export_dict['rtt_avg'].append(
    #                                 ip_data['rtt_avg'])
    #                             export_dict['packet_loss'].append(
    #                                 ip_data['packet_loss'])
    #                 else:
    #                     export_dict['domain'].append(domain)
    #                     export_dict['ip'].append(ip)
    #                     export_dict['port'].append(None)
    #                     export_dict['port_status'].append(None)
    #                     export_dict['port_type'].append(None)
    #                     export_dict['rtt_avg'].append(ip_data['rtt_avg'])
    #                     export_dict['packet_loss'].append(
    #                         ip_data['packet_loss'])
    #         else:
    #             export_dict['domain'].append(domain)
    #             export_dict['ip'].append(None)
    #             export_dict['port'].append(None)
    #             export_dict['port_status'].append(None)
    #             export_dict['port_type'].append(None)
    #             export_dict['rtt_avg'].append(None)
    #             export_dict['packet_loss'].append(None)
    #     df = pd.DataFrame.from_dict(export_dict)
    #     df.to_csv(self.output_file)
    #     return df
