import requests

def emailquery(arg,arg2, outfile):
    error = None
    offset = 0
    primary_key = "<REDACTED>" #place your own keys here
    secondary_key = "<REDACTED>" # secondary key if primary key runs out of requests
    #personal_key = ""
    if arg2 == 1:
        key = primary_key
    elif arg2 == 2:
        key = secondary_key
    
    # Add your own keys here:
    #elif arg2 == 3:
    #    key = personal_key
    # Add an argument for your own key to base as well
    else:
        print "Please choose a valid key"
    r1 = requests.get("https://api.hunter.io/v2/domain-search?domain=" + arg + "&offset=" + str(offset) + "&api_key=" + key)
    data = r1.json()
    if not 'errors' in data:
        count = data['meta']['results']
        with open(outfile, 'a') as outfile:
            print "Found " + str(count) + " emails, iterating through..."
            outfile.write("\r\n##### Starting Email Hunter Output #####\r\n")
            outfile.write("\r\nFound " + str(count) + " emails, iterating through...\r\n")
            while offset < count:
                r2 = requests.get("https://api.hunter.io/v2/domain-search?domain=" + arg + "&offset=" + str(offset) + "&api_key=" + key)
                data = r2.json()               
                for email in data['data']['emails']:
                    source = email['sources'][0]['uri']  # only printing first source
                    print email['value'] + " (" + source + ")"
                    outfile.write("\r\n" + email['value'] + " (" + source + ")")
                offset += 10
    else:
        for error in data['errors']:
            if error['code'] == 429:
                print "Key is out of monthly requests, rerun and attempt another key or get your own"
            else:
                print "Unidentified error encountered"
