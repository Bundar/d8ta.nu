from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import csv
import time

def calc_bmi(ht, wt):
    try:
        bmi = int(wt)/(int(ht)/100)**2
    except:
        bmi = ''
    finally:
        return bmi

driver = webdriver.Chrome("/usr/lib/chromium/chromedriver")
driver.get("https://www.8a.nu/scorecard/ranking/")
time.sleep(1)

i = 0
startI = 0
while(i < 10):
    print("LOG: Processing data file #" + str(i))
    content = driver.page_source
    soup = BeautifulSoup(content, features="lxml")
    table = soup.find(id="ctl00_ContentPlaceholder_GridViewRankingRoute")
    
    if table == None:
        print(str(i) + ": Couldnt find the table... ")
        print(table)

    if i >= startI:
        csvfile = open('data/route-data/routeData'+str(i)+'.csv', 'w', newline='') 
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Placing', 'Score', 'Name', 'DoB', 'Country', 'Height', 'Weight', 'Started Climbing', 'BMI'])
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            if len(cells) == 8:
                placing = cells[0].find(text=True)
                score = cells[2].find(text=True)
                name = cells[4].find(text=True)
                dob = cells[5].find(text=True)
                country = cells[6].find(text=True)
                
                ## Go To Persons Page and get more data
                print("LOG: attempting to reach site: "+str(cells[4].find('a')['href']))
                driver2 = webdriver.Chrome("/usr/lib/chromium/chromedriver")

                driver2.get("https://www.8a.nu/"+str(cells[4].find('a')['href']))
                time.sleep(1)
                height = ''
                weight = ''
                yrsclimbing = ''

                retires = 0
                while not (height and weight and yrsclimbing):
                    try:
                        height =  driver2.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[2]/td[2]/div/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/span').text
                        print("Height: " + str(height))
                        weight = driver2.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[2]/td[2]/div/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[3]/td[2]/span').text
                        print("Weight: " + str(weight))
                        yrsclimbing = driver2.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[2]/td[2]/div/div[1]/table[2]/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/span').text
                        print("Started Climbing: " + str(yrsclimbing))
                    except:
                        print("Error")

                    retires = retires + 1
                    if retires > 3:
                        break
                driver2.close()
                driver2.quit()
                ## Write to CSV:

                bmi = calc_bmi(height, weight)

                print("LOG: Writing to CSV. placing: " + str(placing))
                writer.writerow([placing, score, name, dob, country, height, weight, yrsclimbing, bmi])
        csvfile.close()
    
    if i > 0:
        driver.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/div/table/tbody/tr[101]/td/table/tbody/tr/td[2]/a').click()
    else:
        driver.find_element_by_xpath('/html/body/form/div[3]/table/tbody/tr[2]/td[2]/div/div[1]/div[2]/table/tbody/tr[2]/td[1]/div/table/tbody/tr[101]/td/table/tbody/tr/td/a').click()
    
    i = i + 1
    driver.refresh()
    time.sleep(1)
