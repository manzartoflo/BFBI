#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 01:47:37 2019

@author: manzars
"""

import requests
from bs4 import BeautifulSoup

urls = "https://www.bfbi.org.uk/members/?wpv_view_count=2153-TCPID977&wpv-member-class=0&wpv_post_search=&wpv_paged="

links = []
for i in range(1, 7):
    url = urls + str(i)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'lxml')
    ul = soup.findAll('ul', {'class': 'wpv-loop'})
    lis = ul[0].findAll('li')
    for li in lis:
        links.append(li.a.attrs['href'])
    
file = open('assignment.csv', 'w')
header = 'Company Name, Email, Telephone, Fax, Website\n'
file.write(header)
for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    name = soup.findAll('h1', {'class': 'elementor-heading-title elementor-size-default'})[0].text
    ul = soup.findAll('ul')
    li = ul[14].findAll('li')
    if(len(li) == 4):
        tel = li[-3].a.text
        email = li[-2].a.text
        web = li[-1].a.attrs['href']
        fax = 'NaN'
    elif(len(li) == 5):
        tel = li[-4].a.text
        fax = li[-3].text.replace('Fax:', '').lstrip()
        email = li[-2].a.text
        web = li[-1].a.attrs['href']
    file.write(name.replace(',', '') + ', ' + email + ', ' + tel.replace(',', '') + ', ' + fax + ', ' + web + '\n')
    print(name)
file.close()