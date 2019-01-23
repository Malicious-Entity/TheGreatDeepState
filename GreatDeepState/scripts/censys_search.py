#!/usr/bin/env python
'''
Censys.io API script
1. Register an account with https://censys.io/register
2. Grab API ID and secret from https://censys.io/account
pip install censys colorama

Rate Limits:
search 0.2 tokens/second (60.0 per 5 minute), api 0.4 tokens/s (120.0 per 5 minute bucket)


Basic usage example:
 python censys_io.py accenture.com or give it IP ranges
'''

from censys.ipv4 import *
from censys.base import *
from pprint import pprint
from urllib import quote, unquote
from colorama import Fore, Back, Style
import tempfile
import argparse
import pickle
import time, sys, re, os


def Censysquery(arg1,file,jsonarg,outfile):
    def defaultsearch():
        for domain in domains:
            api_id = '<REDACTED>'#place your own ID here
            api_secret = '<REDACTED>'#place your own key here

            global sites
            sites = {}
            # API is time limited
            # 0.2 tokens/second (60.0 per 5 minute)
            report_buckets = 50
            filter_fields = ['location.country', 'location.country_code', 'location.city', 'ip', \
                             'protocols', 'autonomous_system.name', \
                             'autonomous_system.asn', \
                             '443.https.tls.certificate.parsed.subject.organization', \
                             '443.https.tls.certificate.parsed.subject.common_name', \
                             '443.https.tls.certificate.parsed.extensions.subject_alt_name.dns_names', \
                             '993.imaps.tls.tls.certificate.parsed.subject.common_name', \
                             '993.imaps.tls.tls.certificate.parsed.subject.organization', \
                             '80.http.get.title', \
                             '80.http.get.headers.server', \
                             '80.http.get.body', \
                             'metadata.os', 'tags']
            report_fields = ['location.country_code', 'location.country.raw', 'ip', \
                             'autonomous_system.asn', 'autonomous_system.organization.raw', \
                             '443.https.tls.certificate.parsed.subject.common_name.raw', \
                             '993.imaps.tls.tls.certificate.parsed.subject.common_name.raw', \
                             '80.http.get.headers.server.raw', \
                             'metadata.os.raw', 'protocols', 'tags.raw']
            # computed from --country US --report tags.raw
            tags_available = ['http', 'https', 'ssh', 'ftp', 'smtp', 'pop3', 'imap', 'imaps', 'pop3s',
                              'known-private-key', 'rsa-export', 'dhe-export', 'Update utility',
                              'heartbleed', 'building control', 'scada', 'fox', 'NPM', 'bacnet', 'NPM6',
                              'embedded', 'strip-starttls', 'modbus', 'NPM2', 'remote access', 'JACE',
                              'JACE-7', 'NPM3', 'JACE-403', 'Running DD-WRT', 'JACE-545', 's7', 'dnp3',
                              'Broken installation', 'scada processor', 'touchscreen', 'data center',
                              'ethernet']
            #get search query
            searchterms = domain
            # build up query
            query = CensysIPv4(api_id, api_secret)

            page = 1
            generator = query.paged_search(searchterms,filter_fields,page=page)
            total_pages = generator['metadata']['pages']
            while page <= total_pages:
                try:
                    generator = query.paged_search(searchterms,filter_fields,page=page)
                    for result in generator['results']:
                        try:
                            IP = result['ip']
                        except:
                            pass
                        try:
                            ports = (result['protocols'])
                            portlist = "".join(str(x) for x in ports)
                        except:
                            pass
                        if 'autonomous_system.asn' in result:
                            ASN = str(result['autonomous_system.asn'])
                        else:
                            ASN = "None"
                        if '443.https.tls.certificate.parsed.subject.common_name' in result:
                            CN = result['443.https.tls.certificate.parsed.subject.common_name']
                            CNlist = "".join(str(x) for x in CN)
                        else:
                            CNlist = "None"
                        if '443.https.tls.certificate.parsed.subject.organization' in result:
                            Org = result['443.https.tls.certificate.parsed.subject.organization']
                            Orglist = "".join(str(x) for x in Org)
                        else:
                            Orglist = "None"
                        str_result = "IP: " + IP + " CN:" + CNlist + ":" + portlist + " ASN:"+ ASN + " Org:" + Orglist
                        if str_result not in sites:
                                sites[str_result] = {}
                                print str_result
                except:
                    print "Error on page: " + str(page)
                    pass
                page +=1
            if jsonarg == 1:
                with open(outfile, 'a') as fp:
                    json.dump(sites, fp)
            else:
                with open(outfile, 'a') as fp:
                    fp.write("\r\n##### Starting Censys Output #####\r\n")
                    for k,v in sites.items():
                        final = str(k) + str(v)
                        fp.write(final)
                        fp.write('\n')
    if file == 1:
        with open(arg1, 'r') as fd:
            domains = fd.read().splitlines()
        sites = {}
        defaultsearch()
    else:
        domains = [arg1]
        defaultsearch()
