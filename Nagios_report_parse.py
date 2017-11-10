#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import urllib3
import sys


# import the pool Manager of urllib3 and store it in http

http = urllib3.PoolManager()

# Url build-up. Modify this one so to reflect your values

url = "$nagiosurl/nagios/cgi-bin/avail.cgi?show_log_entries=&servicegroup=$SERVICEGROUP&timeperiod=$TIMEPERIOD&backtrack=0"

# passing Username and PWD parameters

headers = urllib3.util.make_headers(basic_auth='username:password')

# getting Nagios page
r = http.request('GET', url, headers=headers)


# Building the soup object to parse html

soup = BeautifulSoup(r.data, "html.parser")

# finding the table with the report data

table = soup.findAll("table")[4]

#table2 = table.prettify()   outcomment to see the prettified table 

# Initiate the dictionary records, where we'll store the table's data

found = False
f = open('output.csv','w')

for row in table.findAll('tr')[1:]:   # Cicle over the html document to find tr class datEven

    cols = row.findAll('td')      # scan deeper in the table
     
    cols = [ele.text.strip() for ele in cols]  # Grab values from the table 
    
    header = cols[0].strip()   # Get the header to perform the control check
    
    if header == 'URLS CHECKS PROD':
        found = True    # Change the value of found so to print all the rows after URL CHECKS PROD
        
    if found:
        f.write(','.join(cols[1:]))    #print to the file, removing first column
        f.write("\n")


f.close()
