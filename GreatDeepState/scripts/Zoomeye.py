import requests
import json

def zoomquery(arg,jsonarg):
    #Using account with 's fake gmail
    r = requests.post('https://api.zoomeye.org/user/login', data= '{"username":"<REDACTED>", "password":"<REDACTED>"}')#place your own user and pass here
    print "Attempting to get access token\r\n"
    token = r.json()
    auth = token['access_token']
    print "Got access token\r\n" \
          "Querying Zoomeye by host..."
    #Adding auth token required by Zoomeye API
    headers = {'Authorization': 'JWT ' + auth}
    rq = requests.get('https://api.zoomeye.org/host/search?query=' + arg, headers=headers)
    data = rq.json()
    if jsonarg == 1:
        with open('gds.json', 'a') as fp:
            json.dump(data, fp)
    else:
        outfile = open('gds.txt', 'a')
        outfile.write("\r\n\r\n##### Starting Zoomeye Output #####\r\n")
       #Retrieving Desired data from returned dictionaries
        for host in data['matches']:
            hostname = str(host['portinfo']['hostname'])
            ip = str(host['ip'])
            port = str(host['portinfo']['port'])
            if hostname:
                result = hostname + ":" + port
            else:
                result = ip + ":" + port
            print result

            outfile.write("\r\n" + result)
        wrq = requests.get('https://api.zoomeye.org/web/search?query=' + arg, headers=headers)
        #Performing same query again but searching for web services instead of hosts
        print "\r\nQuerying Zoomeye by web service..."
        wdata = wrq.json()
        for web in wdata['matches']:
            # domain = str(web['domains'])
            website = str(web['site'])
            for ip in web['ip']:
                ip = str(web['ip'])
            #Sometimes the server attribute doesn't exist, it contains more data than website so attempting that first
            if web['server'] is not None:
                for server in web['server']:
                    with open('gds.txt', 'a') as outfile:
                        servertype = str(server['name']) + " Version:" + str(server['version'])
                        print website + " server type: " + servertype
                        outfile.write("\r\n" + website + " server type: " + servertype)
            else:
                print website + " (" + ip + ")"
                outfile = open('gds.txt', 'a')
                outfile.write("\r\n" + website + " (" + ip + ")")
                outfile.close()
            outfile.close()



