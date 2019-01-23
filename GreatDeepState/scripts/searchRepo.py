"""
Credit for this code goes to https://github.com/ryanbaxendale 
via https://github.com/dxa4481/truffleHog/pull/9
"""
import requests
import truffleHogplus
import json
import sys

def get_repo(*repo):
    for repos in repo:
        response = requests.get(url='https://api.github.com/repos/' + str(repos))
        json = response.json()
        f = open('gds-singlegitout.txt', 'a')
        #print item["html_url"]
        #if item['private'] == False:
        #print('searching ' + item["html_url"])
        orig_stdout = sys.stdout
        sys.stdout = f
        print('\r\n-----Searching ' + str(repos) + "-----\r\n")
        truffleHogplus.find_strings('https://github.com/' + str(repos), printJson=False)
        sys.stdout = orig_stdout
    f.close

def search_repo(*search):
    for searches in search:
        response = requests.get(url='https://api.github.com/search/repositories?q=' + str(searches))
        json = response.json()
        repolist = []
        for item in json['items']:
            print item['html_url']
            repolist.append(item['html_url'])
