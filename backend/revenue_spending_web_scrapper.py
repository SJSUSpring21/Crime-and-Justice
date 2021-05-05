#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from gazpacho import Soup
import csv


url = 'https://usafacts.org/data/topics/government-finances/spending/?state=00&state=26&state=02&state=53&state=30&state=44&state=29&state=18&state=16&state=49&state=47&state=37&state=12&state=04&state=31&state=27&state=35&state=45&state=51&state=09&state=25&state=38&state=55&state=56&state=46&state=19&state=15&state=41&state=05&state=23&state=50&state=33&state=11&state=08&state=22&state=48&state=54&state=10&state=36&state=39&state=42&state=34&state=01&state=17&state=06&state=32&state=40&state=28&state=21&state=20&state=13&state=24'


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

divs = soup.findAll("table")
years = []
data_val = []
states = []
result = []
for div in divs:
    j = 0
    row = ''
    rows = div.findAll('tr')
    for row in rows:
        j = j + 1
        start = 0
        end = 0
        if(row.text.find("Establish Justice and Ensure Domestic Tranquility") > -1):
            start = j
        if(row.text.find("Provide for the Common Defense") > -1):
            end = j
            break
    for y in range(start,end):
        cells = rows[y].find_all(['th'], recursive=True)
        datas = rows[y].find_all(['td'], recursive=False)
        i = 0
        for cell in cells:
            if cell.string and cell.string!='Spending By Mission': years.append(cell.string)
        for data in datas:
            if data.string:
                data_val.append(data.string)
            else:
                if(len(data.text)>0 and data.text!='Establish Justice and Ensure Domestic Tranquility'
                  and data.text!='Provide for the Common Defense' and data.text!='United States'):
                    states.append(data.text)
fields = ['year', 'state', 'amount']
for i in range(0,39):
    data_val.pop(0)
    i = i + 1
for state in states:
    for year in years:
        if(start<len(data_val)):
            result.append([year, state,data_val[start]])
            start = start + 1;
with open('spending.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(result)

url = 'https://usafacts.org/data/topics/government-finances/revenue/?state=00&state=26&state=02&state=53&state=30&state=44&state=29&state=18&state=16&state=49&state=47&state=37&state=12&state=04&state=31&state=27&state=35&state=45&state=51&state=09&state=25&state=38&state=55&state=56&state=46&state=19&state=15&state=41&state=05&state=23&state=50&state=33&state=11&state=08&state=22&state=48&state=54&state=10&state=36&state=39&state=42&state=34&state=01&state=17&state=06&state=32&state=40&state=28&state=21&state=20&state=13&state=24'


driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

divs = soup.findAll("table")
years = []
data_val = []
states = []
result = []
for div in divs:
    j = 0
    row = ''
    rows = div.findAll('tr')
    for row in rows:
        j = j + 1
        start = 0
        end = 0
        if(row.text.find("Annual Deficit / Surplus") > -1):
            break;
        if(row.text.find("Tax Revenue") > -1 and row.text.find("Non-Tax Revenue")<0):
            start = j
        if(row.text.find("Non-Tax Revenue") > -1):
            end = j
            break
    for y in range(start,end):
        cells = rows[y].find_all(['th'], recursive=True)
        datas = rows[y].find_all(['td'], recursive=False)
        for cell in cells:
            if cell.string and cell.string!= 'Revenue': years.append(cell.string)
        for data in datas:
            if data.string:
                data_val.append(data.string)
            else:
                if(len(data.text))>0 and data.text!='Tax Revenue' and data.text!='United States' and data.text!='Non-Tax Revenue':
                    states.append(data.text)

fields = ['year', 'state', 'Revenue']
for i in range(0,39):
    data_val.pop(0)
    i = i + 1
for j in range(0,51):
    states.pop(0)
    j = j + 1
print(states)
print(years)
for state in states:
    for year in years:
        if(start<len(data_val)):
            result.append([year, state,data_val[start]])
            start = start + 1;
with open('revenue.csv', 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(result)




