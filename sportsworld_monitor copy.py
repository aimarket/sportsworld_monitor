import json 
import requests
import time
import os
import random
from datetime import datetime
from datetime import date
from pytz import timezone
import xml.etree.ElementTree as ET

webhook="YOURWEBHOOKGOESHERE"

proxy_dict = {}
with open('Proxy-List.txt') as li:
    proxy = li.readline()
    cnt = 0
    
    while proxy:
        proxy_dict[cnt] = {"https":"http://{0}".format(proxy.strip())}
        proxy = li.readline()
        cnt += 1
li.close()

def fetchinfo():
    choice = random.randint(0,999)
    new = None
    while(new == None ):
        try:
            print("Using proxy" + str(proxy_dict[choice]))
            new = requests.get('https://sportsworld165.com/collections/new-arrivals/fitted.oembed',proxies=proxy_dict[choice])
        except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
            send_Error("Timeout error", e)
            choice = random.randint(0,999)
            print("retying...")
        except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
            send_Error("Too many redirects", e)
            choice = random.randint(0,999)
            print("Retrying....")
        except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
            send_Error("Catastrophic Error Fuck You!", str(e) + "\nwhile using proxy"+str(proxy_dict[choice]))
            choice = random.randint(0,999)
            print("Retrying")
    
    with open("updates.xml","wb") as f:
        f.write(new.content)


def send_Error(message, e):
    data = {"embeds":[]}
    embed = {}
    
    embed["title"]=message
    embed["description"] = str(e)
    embed['color']= 0xff0000
    data['username']= 'SportsWorld Monitor'
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"].append(embed)
    requests.post(webhook,data=json.dumps(data), headers={"Content-Type": "application/json"})

def send_notification(title,url, image):
    data = {"embeds":[]}
    embed = {}
    embed["title"]=title
    embed["image"]={"url":"https:"+image}
    embed['color']= 65301
    data['username']= 'SportsWorld Monitor'
    embed["url"] = url
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"].append(embed)
    requests.post(webhook,data=json.dumps(data), headers={"Content-Type": "application/json"})
    #print(product["title"])
    time.sleep(1.5)
def main():
    awake = False #change to False
    while(True):
        
        while(awake):
            print("inside main loop")
            already_set = False
            today = str(date.today())
            fetchinfo()
            tree = ET.parse('updates.xml')
            root = tree.getroot()
            update = ''
            count = 0
            for child in root:
                for update_entry in child.findall("{http://www.w3.org/2005/Atom}updated"):
                    print(count)
                    date_xml = update_entry.text.split("T")
                for title_entry in child.findall("{http://www.w3.org/2005/Atom}title"):
                    title = title_entry.text.split("&quot;")
                for image_entry in child.findall("{http://www.w3.org/2005/Atom}summary"):
                    image = image_entry.text.split("https:")[1].split("\"")
                for link_entry in child.findall("{http://www.w3.org/2005/Atom}link"):
                    if date_xml[0] == today:
                        update = date_xml[0]
                        url=link_entry.attrib["href"]
                        
                        with open('dates.txt') as li:
                            
                            dates = li.readline()
                            while dates:
                                if dates.strip() == today:
                                    already_set = True
                                dates = li.readline()
                        li.close()  
                        if(not already_set):
                            send_notification(title[0], url, image[0])
                    
                    count +=1

            if(not already_set):
                file1 = open("dates.txt","a")
                file1.write("\n"+update)
                file1.close()
            print("done")
            awake = False
        mst = timezone('MST')
        current = datetime.now(mst).strftime("%H%M")
        if(int(current) >= 1559 and int(current) <= 1601):
            awake = True
            time.sleep(random.randrange(150,300)/100)
        else:
            print("sleeping 2 min")
            time.sleep(120)
            

main()
