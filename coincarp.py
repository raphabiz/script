"""

@RAPHABIZ

"""

import csv
import os
import random
from dotenv import load_dotenv
import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException

class Coincarp():
  def __init__(self):
    self.driver = webdriver.Chrome()
    self.driver.get("https://www.coincarp.com/fundraising/")
    self.driver.set_window_size(1280, 680)

  def process_page(self,i):
    # start timer
    start = time.time()
    time.sleep(random.randint(2,5)) 

    name = self.driver.find_element(By.XPATH,f'//*[@id="fundraisingListTable"]/tbody/tr[{i}]/td[1]/a/span').get_attribute("innerHTML") 

    # change page
    newurl=self.driver.find_element(By.XPATH,f'//*[@id="fundraisingListTable"]/tbody/tr[{i}]/td[1]/a').get_attribute('href')
    self.driver.get(newurl)

    try :
        subcategory=self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[1]/div[5]/p[2]/span/a').get_attribute('innerHTML')
    except :
        subcategory =""
    try :
        valuation=self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[1]/div[3]/p[2]/span/a').get_attribute('innerHTML')
    except :
        valuation =""
    try :
        self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[1]/div[2]/p[2]/span').get_attribute("innerHTML")
        financing_amount= ""
    except :
        financing_amount= self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[1]/div[2]/p[2]').get_attribute("innerHTML")
      
    logo = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div[2]/div[3]/div/div/div[1]/img').get_attribute("src")
    category=self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[1]/div[4]/p[2]/span/a').get_attribute('innerHTML') 
    try :
       project_info=self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[7]/p').get_attribute('innerHTML')
    except :
       project_info=self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[6]/p').get_attribute('innerHTML')

    company ={
       "name":name,
       "logo":logo,
       "project_info":project_info,
       "financing_amout":financing_amount,
       "valuation":valuation,
       "category":category,
       "subcategory":subcategory,
       "links":self.get_links(),
       "investors":self.get_investors()
      }
    pprint.pprint(company)

    # go back to the main page 
    self.driver.back()
    # End timer
    end = time.time()
      # Evaluate execution time
    elapsed_time = end - start
    print('Execution time:', elapsed_time, 'seconds')
    """ columns=["name","company","position","joining_date","introduction","offering"]

    self.save_to_csv(attendee,columns,"token2049") """

  def get_links(self):
    links={}
    try: 
      all= self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[6]')
      # Iterate on all links
      for i in range(len(all.find_elements(By.XPATH,'./*'))):
       key = self.driver.find_element(By.XPATH,f'//*[@id="detailContent"]/div[6]/a[{i+1}]').get_attribute('data-original-title')
       value = self.driver.find_element(By.XPATH,f'//*[@id="detailContent"]/div[6]/a[{i+1}]').get_attribute('href')
       links[key] = value
    except:
      all= self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[5]')
      # Iterate on all links
      for i in range(len(all.find_elements(By.XPATH,'./*'))):
       key = self.driver.find_element(By.XPATH,f'//*[@id="detailContent"]/div[5]/a[{i+1}]').get_attribute('data-original-title')
       value = self.driver.find_element(By.XPATH,f'//*[@id="detailContent"]/div[5]/a[{i+1}]').get_attribute('href')
       links[key] = value
    return links
  
  def get_investors(self):
    investors={}
    try:
      all= self.driver.find_element(By.CSS_SELECTOR,'#tableInvestorList > tbody')
      # iterate on all investors
      for i in range(len(all.find_elements(By.XPATH,'./*'))): 
       try:
          self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[4]/span').get_attribute("innerHTML")
          year_funded = ""
       except:
          year_funded = ""
          year_funded = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[4]').get_attribute("innerHTML")
       
       logo = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[1]/div/a/img').get_attribute("src")
       name = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[1]/div/a/span').get_attribute("innerHTML")
       
       # change url 
       """  newurl = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[1]/div/a').get_attribute('href')
       self.driver.get(newurl)
       about = ""
       abouts = self.driver.find_element(By.ID,'projectInfo')
       for i in range(len(abouts.find_elements(By.XPATH,'./*'))): 
          print(i)
          about = about + " " + self.driver.find_element(By.XPATH,f'//*[@id="projectInfo"]/p[{i+1}]').get_attribute("innerHTML")
          print(about) """

       # go back to the company page 
       """ self.driver.back()
       time.sleep(2) """

       investor ={
          "logo" : logo,
          "name": name,
          "year_funded": year_funded
       }
       investors[f"investor {i+1}"] = investor 
    except:
       investors = ""

    return investors
  
  def get_data(self):
     page=0
     time.sleep(2)
     # Remove banner 
     self.driver.find_element(By.CLASS_NAME,'btn-close.close').click()
     while True:
       time.sleep(1)
       odd = self.driver.find_elements(By.CLASS_NAME,'odd')
       even = self.driver.find_elements(By.CLASS_NAME,'even')
       list= odd + even
       page=page+1
       print("Page "+str(page))
       for i in range(len(list)):
         print("Element "+str(i+1))
         self.process_page(i+1)
         """ self.driver.back() """
       if self.is_disable(type="class",locator='paginate_button.page-item.next disabled') == True:
          break
       self.driver.find_element(By.CLASS_NAME,'paginate_button.page-item.next').click()

  def is_disable(self,type,locator):
     if type == "xpath":
      try :
        WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.XPATH,locator)))
        return True
      except:
        return False
     else :
      try :
        WebDriverWait(self.driver,3).until(EC.visibility_of_element_located((By.CLASS_NAME,locator)))
        return True
      except:
        return False

  def verify_duplicate_in_csv(self, dapps,csvfilename):
    with open(f"{csvfilename}.csv",encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        # Skip the headers
        next(reader, None)
        data_read = [row for row in reader]
    # Check for duplicate IDs in the data_read list
    for row in data_read:
        if row[0] == dapps.get('title'):
            print(f"Duplicate ID found: {dapps.get('title')}")
            return True  # Duplicate found
    print("No duplicate found.")
    return False  # No duplicate found
        
  def create_csv_if_not_exists(self,filepath, header):
    if not os.path.exists(filepath+'.csv'):
        with open(filepath+'.csv', 'w', newline='') as csv_file:
            if header:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
        print(f"CSV file '{filepath}' created.")
    else:
        print(f"CSV file '{filepath}' already exists.")

  def save_to_csv(self,dapps,columns,csvfilename):
    # Verify if csv file exists
    self.create_csv_if_not_exists(csvfilename,columns)
    # Verify if participant is alredy in file
    if self.verify_duplicate_in_csv(dapps,csvfilename=csvfilename) == False:
       # Append data to the CSV file
       with open(f'{csvfilename}.csv', 'a', newline='', encoding='UTF-8') as f:
          w = csv.DictWriter(f, fieldnames=columns)
          print(dapps)
          w.writerow(dapps)

# Instantiate Token2049 class and call get_data method
coincarp = Coincarp()
coincarp.get_data() 

