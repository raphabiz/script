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
    time.sleep(5)
    name = self.driver.find_element(By.XPATH,f'//*[@id="fundraisingListTable"]/tbody/tr[{i}]/td[1]/a/span').get_attribute("innerHTML") 
    time.sleep(5)
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
       project_info=self.driver.find_element(By.CSS_SELECTOR,'#detailContent > div.cryptocurrentcies-info.mt-1 > p').get_attribute('innerHTML')
    except :
       project_info=self.driver.find_element(By.XPATH,'//*[@id="detailContent"]/div[6]/p').get_attribute('innerHTML')
    
    company ={
       "name":name,
       "logo":logo,
       "project_info":project_info,
       "financing_amount":financing_amount,
       "valuation":valuation,
       "category":category,
       "subcategory":subcategory,
       "links":self.get_links(),
       "investors":self.get_investors()
      }
    
    pprint.pprint(company)
    print("------")
   
    # go back to the main page 
    self.driver.back()
    # End timer
    end = time.time()
    # Evaluate execution time
    elapsed_time = end - start
    print('Execution time:', elapsed_time, 'seconds')
    """ columns=["name","logo","project_info","financing_amount","valuation","category","subcategory","links","investors"]

    self.save_to_csv(company,columns,"coincarp") """

  def get_links(self):
    links={}
    try: 
      all= self.driver.find_element(By.CSS_SELECTOR,'#detailContent > div.social-list.d-flex') 
      # Iterate on all links
      for i in range(len(all.find_elements(By.XPATH,'./*'))):       
       key = self.driver.find_element(By.CSS_SELECTOR,f'#detailContent > div.social-list.d-flex > a:nth-child({i+1})').get_attribute('data-original-title')
       value = self.driver.find_element(By.CSS_SELECTOR,f'#detailContent > div.social-list.d-flex > a:nth-child({i+1})').get_attribute('href')
       links[key] = value
    except:
       print("error")
    return links
  
  def get_investors(self):
   investors={}
   time.sleep(5)
   try :
     all= self.driver.find_element(By.CSS_SELECTOR,'#tableInvestorList > tbody')
     size = len(all.find_elements(By.XPATH,'./*'))
   except :
     size =0
   if  size > 0 :
      # iterate on all investors
      for i in range(len(all.find_elements(By.XPATH,'./*'))): 
       time.sleep(5)
       try:
          self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[4]/span').get_attribute("innerHTML")
          year_founded = "" 
       except:
          year_founded = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[4]').get_attribute("innerHTML")
       
       logo = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[1]/div/a/img').get_attribute("src")
       name = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[1]/div/a/span').get_attribute("innerHTML")
       links =self.get_investors_links(i+1)
       
       # change url 
       newurl = self.driver.find_element(By.XPATH,f'//*[@id="tableInvestorList"]/tbody/tr[{i+1}]/td[1]/div/a').get_attribute('href')
       self.driver.get(newurl)
       
       # Scrap about data of each investors 
       about = ""
       abouts = self.driver.find_element(By.ID,'projectInfo')
       for i in range(len(abouts.find_elements(By.XPATH,'./*'))-1): 
          about = about + " " + self.driver.find_element(By.XPATH,f'//*[@id="projectInfo"]/p[{i+1}]').get_attribute("innerHTML")
          
       # Scrap investor portfolio
       portfolio =self.get_investors_portfolio()
       
       investor ={
          "logo" : logo,
          "name": name,
          "year_founded":year_founded,
          "about":about,
          "portfolio":portfolio,
          "links":links
       }
       investors[f"investor {i+1}"] = investor 

       # go back to the company page 
       time.sleep(2)
       self.driver.back()
   else:
       investors = ""

   return investors
  
  def get_investors_portfolio(self):
      portfolio={}
      table = self.driver.find_element(By.CSS_SELECTOR,'#tableFundRaisingList > tbody')
      # iterate on all portfolios project
      print(len(table.find_elements(By.XPATH,'./*')))
      for i in range(len(table.find_elements(By.XPATH,'./*'))): 
       try: 
          name = self.driver.find_element(By.CSS_SELECTOR,f'#tableFundRaisingList > tbody > tr:nth-child({i+1}) > td.sticky > a > span').get_attribute("innerHTML")
          amount = self.driver.find_element(By.CSS_SELECTOR,f'#tableFundRaisingList > tbody > tr:nth-child({i+1}) > td:nth-child(5)').get_attribute("innerHTML")
          coinvestor =self.driver.find_element(By.CSS_SELECTOR,f'#tableFundRaisingList > tbody > tr:nth-child({i+1}) > td:nth-child(6)').get_attribute("innerHTML")
          funding_date= self.driver.find_element(By.CSS_SELECTOR,f'#tableFundRaisingList > tbody > tr:nth-child({i+1}) > td:nth-child(7)').get_attribute("innerHTML")
          project ={
            "name": name,
            "amount":amount,
            "coinvestor":coinvestor,
            "funding_date":funding_date
          }
          portfolio[f"project {i+1}"] = project
       except:
          print("ERROR")
      return portfolio

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
       print(len(list))
       for i in range(len(list)):
         print("Element "+str(i+1))
         self.process_page(i+1)
         """ self.driver.back() """
       if self.is_disable(type="class",locator='paginate_button.page-item.next disabled') == True:
          break
       self.driver.find_element(By.CLASS_NAME,'paginate_button.page-item.next').click()

  def get_investors_links(self,j):
    links={}
    try: 
      all= self.driver.find_element(By.CSS_SELECTOR,f'#tableInvestorList > tbody > tr:nth-child({j}) > td:nth-child(7) > div') 
      # Iterate on all links
      for i in range(len(all.find_elements(By.XPATH,'./*'))):       
       key = self.driver.find_element(By.CSS_SELECTOR,f'#tableInvestorList > tbody > tr:nth-child({j}) > td:nth-child(7) > div > a:nth-child({i+1})').get_attribute('data-original-title')
       value = self.driver.find_element(By.CSS_SELECTOR,f'#tableInvestorList > tbody > tr:nth-child({j}) > td:nth-child(7) > div > a:nth-child({i+1})').get_attribute('href')
       links[key] = value
    except:
       print("error")
    return links
  
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

