#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-09-12 16:56
# @File    : 将ip转换为cidr.py


import netaddr
def interpreter_ip_section_to_ip(ip_section_string):
    """
    提供一个功能，将IP段转换成CIDR IP的表示方法如，
    "10.33.0.15-10.33.0.24"转换为['10.33.0.15/32','10.33.0.16/29','10.33.0.24/32']
    :param ip_section_string: 以ip网段表示的一个ip段
    :return: list，以CIDR表示的ip
    """
    if not ip_section_string:
        return ""
    ip_start, ip_end = ip_section_string.split("-")
    cidrs_list = netaddr.iprange_to_cidrs(min(ip_start, ip_end), max(ip_start, ip_end))
    return cidrs_list

def interpreter_ip_to_section_ip(ips_list):
        """
        提供一个功能，将CIDR表示的IP转换成 IP段的表示方法如，不连续的段会以#分隔开，注意以CIDR表示的IP，必须表示的是
        一段或多段连续的IP，不可是一段连续的ip，一段独立的ip的形式：
        ['10.33.0.15/32','10.33.0.16/29','10.33.0.24/32']转换为"10.33.0.15-10.33.0.24"
        :param ips_list: list，以CIDR表示的ip
        :return:string  以ip网段表示的一个ip段
        """
        ip_net = []
        ip_string = ""
        int_to_ip = lambda x: '.'.join([str(x / (256 ** i) % 256) for i in range(3, -1, -1)])
        for ips in ips_list:
            ip_net.append(netaddr.glob_to_iprange(netaddr.cidr_to_glob(ips)))
        ip_start = ip_net[0].key()[1]
        ip_end = ip_net[0].key()[2]
        for index in xrange(len(ip_net)):
            if ip_net[index].key()[1] - 1 <= ip_end:
                ip_end = ip_net[index].key()[2]
                if index == len(ip_net) - 1:
                    ip_end = ip_net[index].key()[2]
                    ip_string += "%s-%s#" % (int_to_ip(ip_start), int_to_ip(ip_end))
            else:
                if index == len(ip_net) - 1:
                    ip_string += "%s-%s#" % (int_to_ip(ip_start), int_to_ip(ip_end))
                ip_string += "%s-%s#" % (int_to_ip(ip_start), int_to_ip(ip_end))
                ip_start = ip_net[index].key()[1]
                ip_end = ip_net[index].key()[2]
        ip_string = ip_string[:-1]
        return ip_string

if __name__ == '__main__':
    result = interpreter_ip_section_to_ip("10.33.0.1-10.33.0.254")
    print(result)