#!/usr/bin/env python
import argparse
from scripts.Emailhunter import emailquery
from scripts.Shodan import shodanquery
from scripts.DNSDumpster import dnsquery
#from scripts.Zoomeye import zoomquery
from scripts.searchOrg import get_org_repos
from scripts.searchRepo import get_repo
from scripts.searchRepo import search_repo
from scripts.censys_search import Censysquery
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--shodan',action='store_true',help="SHODAN SOME STUFF")
parser.add_argument('--emailhunter', nargs=2, help="HUNT SOME EMALEZ")
parser.add_argument('--dnsdumpster', help="GO DUMPSTER DIVING")
#parser.add_argument('--zoomeye', help="ASK THE CHINESE ABOUT IT")
parser.add_argument('--gitorg', help="SEARCH AN ORG")
parser.add_argument('--gitrepo', help="SEARCH THROUGH A REPO")
parser.add_argument('--searchrepo', help="SEARCH FOR A REPO")
parser.add_argument('--censys',action='store_true', help="CENSYS SEARCH")
parser.add_argument('--json',action='store_true',help="DEFINITELY OUTPUTS EVERYTHING B64")
parser.add_argument('--file', help="use file input for shodan or censys")
parser.add_argument('--net',action='store_true', help="use CIDR range for shodan or censys")
parser.add_argument('--input',help="what to search for e.g. CIDR range, input file, domain")
parser.add_argument('--outfile',help="File to write data to")
args = parser.parse_args()
global outfile
outfile = "gds.txt"
if args.outfile:
    outfile = args.outfile
else:
    outfile = "gds.txt"

if args.shodan:
    if args.json:
        if args.file:
            shodanquery(args.file,1,0,1,outfile)
        elif args.net:
            shodanquery(args.input,0,1,1,outfile)
        elif args.file and args.net:
            shodanquery(args.file,1,1,1,outfile)
        else:
            shodanquery(args.input,0,0,1,outfile)
    else:
        if args.file:
            shodanquery(args.file,1,0,0,outfile)
        elif args.net:
            shodanquery(args.input,0,1,0,outfile)
        elif args.net and args.file:
            shodanquery(args.file,1,1,0,outfile)
        else:
            shodanquery(args.input,0,0,0,outfile)

if args.emailhunter:
    emailquery(args.emailhunter,1,outfile)
if args.dnsdumpster:
    dnsquery(args.dnsdumpster,0,outfile)
#if args.zoomeye:
#    if args.json:
#        zoomquery(args.zoomeye,1,outfile)
#    else:
#        zoomquery(args.zoomeye,0,outfile)
if args.gitorg:
    get_org_repos(args.gitorg)
if args.gitrepo:
    get_repo(args.gitrepo)
if args.searchrepo:
    search_repo(args.searchrepo)
if args.censys:
    if args.json:
        if args.file:
            Censysquery(args.file,1,1,outfile)
        else:
            Censysquery(args.input,0,1,outfile)
    elif args.file:
        Censysquery(args.file,1,0,outfile)
    else:
        Censysquery(args.input,0,0,outfile)

print r"___________.__               ________                      __    ________                           _________ __          __          "
print r"\__    ___/|  |__   ____    /  _____/______   ____ _____ _/  |_  \______ \   ____   ____ ______    /   _____//  |______ _/  |_  ____  "
print r"  |    |   |  |  \_/ __ \  /   \  __\_  __ \_/ __ \\__  \\   __\  |    |  \_/ __ \_/ __ \\____ \   \_____  \\   __\__  \\   __\/ __ \ "
print r"  |    |   |   Y  \  ___/  \    \_\  \  | \/\  ___/ / __ \|  |    |    `   \  ___/\  ___/|  |_> >  /        \|  |  / __ \|  | \  ___/ "
print r"  |____|   |___|  /\___  >  \______  /__|    \___  >____  /__|   /_______  /\___  >\___  >   __/  /_______  /|__| (____  /__|  \___  >"
print r"                \/     \/          \/            \/     \/               \/     \/     \/|__|             \/           \/          \/ "

print "========================================================================================================================================"

# Def module block
def emailhuntermodule():
    try:
        print "Please Enter a domain to search:"
        emailsearch = raw_input() 
        print "Please choose the number of the Email Hunter key you would like to try: \r\n"
        print " 1. Primary Key \r\n"
        print " 2. Secondary Key \r\n"
        choice = int(raw_input())
        print "Running Email Hunter Query"
        emailquery(emailsearch,choice,outfile)
        print "\r\n"
    except:
        print "\r\n Sorry there was an error in Email Hunter Module, skipping... Might be out of montly requests?\r\n"

def dumpstermodule():
    try:
        print "Please enter a domain to search:"
        dnssearch = raw_input()
        print "Running DNSDumpster Query"
        dnsquery(dnssearch,0,outfile)
        print "\r\n"
    except:
        print "\r\nSorry there was an error in DNSdumpster Module, skipping...\r\n"

def shodanmodule():
    try:
        print "Please enter a domain name, IP address, or type -file or -net to load from a file or CIDR"
        shodansearch = raw_input()
        if shodansearch == "-file":
            print "Please provide a file with a line broken list of domains or IP's"
            shodansearchfile = raw_input()
            shodanquery(shodansearchfile,1,0,0,outfile)
        elif shodansearch == "-net":
            print "Please provide a CIDR range to search"
            netrange = raw_input()
            shodanquery(netrange,0,1,0,outfile)
        else:
            shodanquery(shodansearch,0,0,0,outfile)
        print "\r\n"
    except:
        print "\r\nSorry there was an error in the Shodan Module, skipping...\r\n"

#def zoomeyemodule():
#    try:
#        print "Enter Domain or IP address to search:"
#        zoomsearch = raw_input()
#        zoomquery(zoomsearch,0,outfile)
#        print "\r\n"
#    except:
#        print "\r\nSorry there was an error in the Zoomeye Module, skipping...\r\n"

def githubmodule():
    try:
        print "Enter Org Name to Search (Don't include .com):"
        orgname = raw_input()
        print "Enter any repos you want to skip like Org/Repo"
        skip = raw_input()
        skips = skip.split()
        allskip = []
        for skipps in skips:
            allskip.append("https://github.com/" + str(orgname) + "/" + str(skipps))
        print "Depending on the size of the org this may take awhile..."
        get_org_repos(orgname, *allskip)
        print "\r\n"
    except:
        print "\r\nEither the organization you provided can't be found on Github or there was an error in the Github Module\r\n"

def gitrepomodule():
    try:
        print "Enter individual repos to search like user/repo user/repo2:"
        repo = raw_input()
        repolist = []
        repos = repo.split()
        for reps in repos:
            repolist.append(str(reps))
        print "Depending on the size of the Repo this may take awhile..."
        get_repo(*repolist)
        print "\r\n"
    except:
        print "\r\nEither the repo you provided can't be found or there was an error in the Github Module\r\n"

def censysmodule():
    try:
        print "Enter something to search"
        censearch = raw_input()
        Censysquery(censearch,0,0,outfile)
    except:
        print "Something errored out, either you performed too many searches, API took to long to respond, or something bad happened"

def repo_searchmodule():
    try:
        print "Enter a search to perform"
        reposearch = raw_input()
        search_repo(reposearch)
    except:
        print "Search failed"

# End Def module block
print "Choose an outputfilename:"
outfile = raw_input()

while not len(sys.argv) > 1:
    print "Please Choose a Module:"

    print " 1. Email Hunter \r\n" \
          " 2. DNSdumpster\r\n" \
          " 3. Shodan \r\n" \
          " 4. Censys \r\n" \
          " 5. Github Org Search\r\n" \
          " 6. Github Single Repo Search \r\n" \
          " 7. Github Search for Repos \r\n" \
          " 8. All \r\n" \
          " 9. Exit \r\n"

    try:
        print "Module:"
        selection = int(raw_input())
        if selection == 1:
            emailhuntermodule()
        elif selection == 2:
            dumpstermodule()
        elif selection == 3:
            shodanmodule()
        elif selection == 4:
           censysmodule()
        elif selection == 5:
            githubmodule()
        elif selection == 6:
            gitrepomodule()
        elif selection == 7:
            repo_searchmodule()
        elif selection == 8:
            print "Please enter a domain to search:"
            domain = raw_input()
            print "Email Hunter Module not included because there's a monthly limit, run the module on it's own or uncomment if you need it."
            #try:
            #    print "Starting Email Hunter Module"
            #    emailquery(domain,1)
            #except:
            #    print "Sorry there was an issue with the Email Hunter Module, skipping..."
            try:
                print "Starting DNSdumpster Module"
                dnsquery(domain)
            except:
                print "Sorry there was an issue with the DNSDumpster Module, skipping..."
            try:
                print "Starting Shodan Module"
                shodanquery(domain,0)
            except:
                print "Sorry there was an issue with the Shodan Module, skipping..."
            try:
                print "Starting Github Module"
                githubmodule()
            except:
                print "Sorry there was an issue with the Github Module, skipping..."
        elif selection == 9:
            break
    except:
        print "Oops! Please use a valid integer to select your option"
