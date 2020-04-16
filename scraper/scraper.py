from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import csv
import time

driver = webdriver.Chrome("/usr/lib/chromium/chromedriver")
driver.get("https://www.8a.nu/scorecard/ranking/")

i = 0
startI = 7
while(i < 10):
    time.sleep(5)
    print("i: " + str(i))
    content = driver.page_source
    soup = BeautifulSoup(content, features="lxml")
    table = soup.find(id="ctl00_ContentPlaceholder_GridViewBoulder")
    

    if table == None:
        print(str(i) + ": Couldnt find the table... ")
        print(table)

    if i >= startI:
        csvfile = open('data/boulder-data/boulderData'+str(i)+'.csv', 'w', newline='') 
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
        csvfile.close()
    
    if i > 0:
        driver.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr[101]/td/table/tbody/tr/td[2]/a').click()
    else:
        driver.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/table/tbody/tr[101]/td/table/tbody/tr/td/a').click()
    
    i = i + 1
    driver.refresh()
    time.sleep(3)
