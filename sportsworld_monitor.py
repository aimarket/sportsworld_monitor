import json 
import requests
import time
import os
import random
from datetime import datetime
from pytz import timezone
 

webhook="YOURWEBHOOK GOES HERE"
global new_data,old_data
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
    global new_data,old_data
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
    
    with open("new.oembed","wb") as f:
        f.write(new.content)

    try:
        new_inventory = open("new.oembed", encoding="utf8")
        old_inventory = open("old.oembed", encoding="utf8")
    except Exception as e:
        send_Error("Error trying to read the file", e)
    
    try:
        new_data = json.load(new_inventory)
        old_data = json.load(old_inventory)
    except Exception as e:
        send_Error("Catastrophic Error in JSON!", e)
        raise SystemExit(e)

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

def send_notification(product,stock,varient):
    data = {"embeds":[]}
    embed = {}
    if stock:
        embed["title"]=product["title"]
        embed["image"]={"url":"https:"+product["thumbnail_url"]}
        embed['color']= 65301
        data['username']= 'SportsWorld Monitor'
        embed["url"] = "https://sportsworld165.com/products/"+product["product_id"]+"?variant="+str(varient)
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"].append(embed)
    requests.post(webhook,data=json.dumps(data), headers={"Content-Type": "application/json"})
    #print(product["title"])
    time.sleep(1.5)
def main():
    awake = False
    while(True):
        
        while(awake):
            print("inside main loop")
            global new_data, old_data
            fetchinfo()
            for new_product, old_product in zip(new_data["products"], old_data["products"]):
                if("FITTED" in new_product["title"].upper()):
                    if(new_product["product_id"] != old_product["product_id"]):

                        break
                    in_stock = False

                    for offer, old_offer in zip(new_product["offers"], old_product["offers"]):
                        if bool(offer["in_stock"]) == True and offer["title"] == "7 1/8" and old_offer["in_stock"] == False and old_offer["title"] == "7 1/8":
                            in_stock = True
                            varient = offer["offer_id"]
                            send_notification(new_product, in_stock, varient)


            os.remove("old.oembed")
            os.rename("new.oembed","old.oembed")

            print("done")
            awake = False
        mst = timezone('MST')
        current = datetime.now(mst).strftime("%H%M")
        if(int(current) >= 1558 and int(current) <= 1630):
            awake = True
            time.sleep(random.randrange(150,300)/100)
        else:
            print("sleeping 2 min")
            time.sleep(120)
            

main()
