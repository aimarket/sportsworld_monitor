
import requests
import json
"""
proxy_dict = {}
proxy_dict[0] = {"https":"http://168.80.98.126:3128"}
new = None
while new == None:
    try:
        new = requests.get("https://sportsworld165.com/collections/new-arrivals/fitted.oembed",proxies=proxy_dict[0], timeout=10.0)
    except requests.exceptions.RequestException as e:
        proxy_dict[0] = {"https":"http://20.69.69.212:3128"}
        print("Trying new proxy")
        print(str(new))
print(str(new))

print("done")
"""

import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import date

'''new = requests.get("https://sportsworld165.com/collections/new-arrivals/fitted.atom")

with open("updates.xml","wb") as f:
        f.write(new.content)
'''
'''tree = ET.parse('updates.xml')
root = tree.getroot()
count = 0


for child in root:
    for update_entry in child.findall("{http://www.w3.org/2005/Atom}summary"):
        print(count)
        date = update_entry.text.split("https:")[1].split("\"")
        print(date[0])
        count+=1
    
'''

today = str(date.today())
print(today)