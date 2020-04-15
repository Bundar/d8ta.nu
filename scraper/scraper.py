from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import csv

driver = webdriver.Chrome("/usr/lib/chromium/chromedriver")
driver.get("https://www.8a.nu/scorecard/ranking/")
content = driver.page_source
soup = BeautifulSoup(content, features="lxml")

if soup == None:
    print("Soup not working right...")

table = soup.find(id="ctl00_ContentPlaceholder_GridViewBoulder")
print("tableType: " + str(type(table)))
#print(str(table))

if table == None:
    print("Couldnt find the table... ")


i=1
csvfile = open('data/boulder-data/boulderData'+i+'.csv', 'w', newline='') 
writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['Placing', 'Score', 'Name', 'DoB', 'Country'])

for row in table.findAll("tr"):
	cells = row.findAll("td")
	if len(cells) == 8:
                placing = cells[0].find(text=True)
                score = cells[2].find(text=True)
                name = cells[4].find(text=True)
                dob = cells[5].find(text=True)
                country = cells[6].find(text=True)
                writer.writerow([placing, score, name, dob, country])
                if type(dob) != type(1):
                    dob = 0
                print(placing +": "+ name + ", " + score + ". Age: " + str(2020 - int(dob)) + " , Country: " + country)
