"""
Credit for this code goes to https://github.com/ryanbaxendale 
via https://github.com/dxa4481/truffleHog/pull/9
"""
import requests
import truffleHogplus
import json
import sys
import re

def get_org_repos(orgname, *skips):
    response = requests.get(url='https://api.github.com/users/' + orgname + '/repos')
    page = 1
    page_total = re.findall('page=\d+', response.headers['link'])
    page_total = page_total[1]
    page_total = page_total[5:]
    while page <= int(page_total):
        r = requests.get(url='https://api.github.com/users/' + orgname + '/repos?page=' + str(page))
        json = r.json()
        #Github had to make this super hard to retrieve page numbers so regex for total pages
        f = open('gds-gitout.txt', 'a')
        for item in json:
            if item["html_url"] not in skips:
                print item["html_url"]
                if item['private'] == False:
                    print('searching ' + item["html_url"])
                    orig_stdout = sys.stdout
                    sys.stdout = f
                    print('\r\n-----Searching ' + item["html_url"] + "-----\r\n")
                    truffleHogplus.find_strings(item["html_url"], printJson=False)
                    sys.stdout = orig_stdout
        page += 1
    f.close

