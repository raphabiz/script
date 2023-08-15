"""

@RAPHABIZ

"""

import csv
import os
import random
from dotenv import load_dotenv

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

load_dotenv()

driver = webdriver.Chrome()
driver.get("https://token2049.brella.io/events/token2049singapore/people")
driver.set_window_size(1280, 680)


class Alchemy():
  def __init__(self):
     ""

  def process_page(self):
    time.sleep(random.randint(2, 5)) 
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/section/section/div/main/div[2]/div[2]/div[1]'))).click()
    time.sleep(random.randint(2, 5)) 
    name =driver.find_element(By.CLASS_NAME,'css-1f4536o.efx8l0f2').get_attribute("innerHTML") 
    company = driver.find_element(By.CLASS_NAME,'css-1xxa55e.efx8l0f1').get_attribute("innerHTML")
    position= driver.find_element(By.CLASS_NAME,'css-w5xx65.efx8l0f0').get_attribute("innerHTML")
    joining_date=driver.find_element(By.CLASS_NAME,'css-ltu1lh.e7do1940').get_attribute('innerHTML')
    try :
      introduction = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'css-1cgtjyh.ee7qfm0'))).get_attribute('innerHTML')
    except :
      introduction =""
    try :
      offering =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'css-17wcctt.e1837n181')))
    except :
       offering = ""
      
    attendee ={
       "name":name,
       "company":company,
       "position":position,
       "joinig_date":joining_date,
       "introduction":introduction,
       "offering":offering,

    }
    print(attendee)
    """ columns=["name","company","position","joining_date","introduction","offering"]

    self.save_to_csv(attendee,columns,"token2049") """

  def get_tags(self):
     list= driver.find_elements(By.CLASS_NAME,'item-header_tag.is--parent.w-inline-block')
     list2= driver.find_elements(By.CLASS_NAME,'item-header_tag.is--child.w-inline-block')
     array=[]
     for i in range(len(list)):
        array.append(driver.find_element(By.XPATH,f'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab968-551a0e8a"]/div[1]/div/div[{i+1}]/a/div').get_attribute("innerHTML"))
     for i in range(len(list2)):
        array.append(driver.find_element(By.XPATH,f'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab968-551a0e8a"]/div[2]/div/div[{i+1}]/a/div').get_attribute("innerHTML"))
     return array 
  
  def get_logged_in(self):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/div/button[2]'))).click()
    input_email =driver.find_element(By.XPATH,'//*[@id="sign-in_email"]')
    input_email.send_keys(os.getenv('email'))
    driver.find_element(By.XPATH,'//*[@id="sign-in"]/button').click()
    time.sleep(random.randint(2, 5)) 
    input_password =driver.find_element(By.XPATH,'//*[@id="sign-in_password"]')
    input_password.send_keys(os.getenv('password'))
    driver.find_element(By.XPATH,'//*[@id="sign-in"]/button').click()

  def get_data(self):
     self.get_logged_in()
     time.sleep(random.randint(2, 5)) 
     # Click on All Attendees sub section
     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/section/section/div/main/div[1]/a[2]'))).click() 
     # Click on number results selector 
     time.sleep(random.randint(2, 5)) 
     driver.find_element(By.XPATH,'//*[@id="root"]/div/div/section/section/div/main/div[2]/ul/li[10]/div/div[1]/span[2]').click()
     # Select 120 results per page
     time.sleep(random.randint(2, 5)) 
     driver.find_element(By.XPATH,'//*[@id="root"]/div/div/section/section/div/main/div[2]/ul/li[10]/div/div[2]/div/div/div/div[2]/div/div/div/div[3]').click()
     time.sleep(random.randint(2, 5)) 
     self.process_page()
     time.sleep(random.randint(2, 5)) 
     
     """ page=0
     while driver.find_element(By.CLASS_NAME,'w-pagination-next.cms-load_next-button').is_displayed() :
       list= driver.find_elements(By.CLASS_NAME,'cms-filter_item.is--dapp.w-dyn-item')
       page=page+1
       print("Page "+str(page))
       for i in range(len(list)):
         print("Element "+str(i+1))
         self.process_page(i+1)
         driver.back()
       time.sleep(4)
       if driver.find_element(By.CLASS_NAME,'w-pagination-next.cms-load_next-button').is_displayed() :
          driver.find_element(By.CLASS_NAME,'w-pagination-next.cms-load_next-button').click() 
     list= driver.find_elements(By.CLASS_NAME,'cms-filter_item.is--dapp.w-dyn-item')
     page=page+1
     print("Page "+str(page))
     for i in range(len(list)):
         print("Element "+str(i+1))
         self.process_page(i+1)
         driver.back()
     print("done") """
      
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

# Instantiate the Alchemy class and call the get_data method
alchemy = Alchemy()
alchemy.get_data() 

