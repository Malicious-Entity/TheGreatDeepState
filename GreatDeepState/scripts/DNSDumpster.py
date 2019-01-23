ƒ#!env python
# -*- coding: utf-8 -*-
from dnsdumpster import DNSDumpsterAPI

def dnsquery(arg2,jsonarg,outfile):
    res = DNSDumpsterAPI.DNSDumpsterAPI(False).search(arg2)
    with open(outfile, 'a') as outfile:
        print "Domain:"
        print res['domain']
        outfile.write("\r\n##### Starting DNSDumpster Output #####\r\n")
        outfile.write(res['domain'])

        print "\n\n\nDNS Servers"
        outfile.write("\n\n\nDNS Servers\r\n")
        for entry in res['dns_records']['dns']:
            print("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry))
            outfile.write("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry) + "\r\n")

        print "\n\n\nMX Records"
        outfile.write("\n\n\nMX Records\r\n")
        for entry in res['dns_records']['mx']:
            print("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry))
            outfile.write("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry) + "\r\n")

        print "\n\n\nHost Records (A)"
        outfile.write("\n\n\nHost Records (A)\r\n")
        for entry in res['dns_records']['host']:
            if entry['reverse_dns']:
                print("{domain} ({reverse_dns}) ({ip}) {as} {provider} {country} {header}".format(**entry))
                outfile.write("\r\n{domain} ({reverse_dns}) ({ip}) {as} {provider} {country} {header}".format(**entry))
            else:
                print("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry))
                outfile.write("{domain} ({ip}) {as} {provider} {country} {header}".format(**entry))

        print "\n\n\nTXT Records\r\n"
        outfile.write("\n\n\nTXT Records")
        for entry in res['dns_records']['txt']:
            print entry
            outfile.write(entry)
    outfile.close()


        #xls_retrieved = res['xls_data'] is not None
        #print "\n\n\nRetrieved XLS hosts? {} (accessible in 'xls_data')".format(xls_retrieved)
        #print repr(res['xls_data'].decode('base64')[:20]) + '...' # to save it somewhere else.
        # open('site.com.xlsx','wb').write(res['xls_data'].decode('base64')) # example of saving xlsx

