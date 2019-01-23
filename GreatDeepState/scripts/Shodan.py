#!/usr/bin/env python
import shodan
import json

def shodanquery(arg1,arg2,arg3,jsonarg,outfile):
    # Configuration
    API_KEY = "<REDACTED>" #place your own key here
    import sys
    global sites

    def defaultsearch():
        for domain in domains:
            print "Shodan of %s" % domain
            # Setup the api
            api = shodan.Shodan(API_KEY)
            # Perform the search
            # query = ' '.join(domain)
            # print "Sending %s" % query
            print "Searching by Domain/Hostname"
            page = 1
            result = api.search("Hostname:" + domain)
            if result['matches'] > 100:
                pagenum = (result['total'] / 100) + 1
                while page <= pagenum:
                    try:
                        result = api.search("Hostname:" + domain, page=page)
                        # Loop through the matches and print each IP
                        for service in result['matches']:
                            try:
                                hostname = service['hostnames']
                                str_ip = service['ip_str']
                                port = str(service['port'])
                                for host in hostname:
                                    result = "IP: " + str_ip + " Hostname: " + host
                                    if result not in sites:
                                        sites[result] = {}
                                        sites[result]['ports'] = []
                                        sites[result]['ports'].append(port)
                                    else:
                                        if result in sites:
                                            sites[result]['ports'].append(port)
                            except:
                                print "Error searching hostname from site: " + str_ip
                    except:
                        print "Error performing search, moving to next page"
                    page += 1

            print "Searching by SSL Cert"
            sslresult = api.search("ssl:" + domain)
            page = 1
            if sslresult['matches'] > 100:
                pagenum = (sslresult['total'] / 100) + 1
                while page < pagenum:
                    try:
                        sslresult = api.search("ssl:" + domain, page=page)
                        for sslservice in sslresult['matches']:
                            try:
                                if sslservice['ssl']['cert']:
                                    if sslservice['ssl']['cert']['subject']['CN']:
                                        CNs = sslservice['ssl']['cert']['subject']['CN']
                                    else:
                                        CNs = "None"
                                else:
                                    CNs = "None"
                                port = str(sslservice['port'])
                                str_ip = sslservice['ip_str']
                                result = "IP: " + str_ip + " CN: " + CNs
                                if result not in sites:
                                    sites[result] = {}
                                    sites[result]['ports'] = []
                                    sites[result]['ports'].append(port)
                                else:
                                    if result in sites:
                                        sites[result]['ports'].append(port)
                            except:
                                print "Error searching by SSL from site: " + str_ip + " usually this means the system" \
                                                                                      " was returned by SSL search," \
                                                                                      " but for some reason" \
                                                                                      " doesn't have a CN or" \
                                                                                      "something else weird"


                    except:
                        print "Error performing search, moving to next page"
                    page += 1
        if jsonarg == 1:
            with open(outfile + '.json', 'a') as fp:
                json.dump(sites,fp)
        else:
            outfile.write("\r\n##### Starting Shodan Output #####\r\n")
            for k, v in sites.items():
                final = str(k) + " " + str(v)
                print final
                outfile.write(str(final))
                outfile.write('\n')
            outfile.close()


    def netsearch():
        api = shodan.Shodan(API_KEY)
        for domain in domains:
            result = api.search("net:" + domain)
            page = 1
            if result['matches'] > 100:
                pagenum = (result['total'] / 100) + 1
                while page <= pagenum:
                    try:
                        result = api.search("net:" + domain, page=page)
                        # Loop through the matches and print each IP
                        for service in result['matches']:
                            try:
                                hostname = service['hostnames']
                                str_ip = service['ip_str']
                                port = str(service['port'])
                                if len(hostname) is not 0:
                                    for host in hostname:
                                        result = "IP: " + str_ip + " Hostname: " + host
                                        if result not in sites:
                                            sites[result] = {}
                                            sites[result]['ports'] = []
                                            sites[result]['ports'].append(port)
                                        else:
                                            if result in sites:
                                                sites[result]['ports'].append(port)
                                else:
                                    result = "IP: " + str_ip + " Hostname: None"
                                    if result not in sites:
                                        sites[result] = {}
                                        sites[result]['ports'] = []
                                        sites[result]['ports'].append(port)
                                    else:
                                        if result in sites:
                                            sites[result]['ports'].append(port)
                            except:
                                print "Error searching hostname from site: " + str_ip
                    except:
                        print "Error performing search, moving to next page"
                    page += 1
        if jsonarg == 1:
            with open(outfile + '.json', 'a') as fp:
                json.dump(sites,fp,indent=2, separators=(',', ': '))
        else:
            outfile.write("\r\n##### Starting Shodan Output #####\r\n")
            for k, v in sites.items():
                final = str(k) + " " + str(v)
                print final
                outfile.write(str(final))
                outfile.write('\n')
            outfile.close()

    if arg2 == 1:
        with open(arg1, 'r') as fd:
            domains = fd.read().splitlines()
        sites = {}
        outfile = open(outfile, 'a')
        defaultsearch()
    elif arg3 == 1:
        print "Shodan of Net range %s" % arg1
        domains = [arg1]
        sites = {}
        outfile = open(outfile, 'a')
        netsearch()
    else:
        domains = [arg1]
        sites = {}
        outfile = open(outfile, 'a')
        defaultsearch()


