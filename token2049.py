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

""" driver = webdriver.Chrome()
driver.get("https://token2049.brella.io/events/token2049singapore/people")
driver.set_window_size(1280, 680) """


class Token2049():
  def __init__(self):
    self.driver = webdriver.Chrome()
    self.driver.get("https://token2049.brella.io/events/token2049singapore/people")
    self.driver.set_window_size(1280, 680)

  def process_page(self):
    # start timer
    start = time.time()
    time.sleep(random.randint(5,10)) 
    #click on Chat button
    ## to do 

    name = self.driver.find_element(By.CLASS_NAME,'css-1f4536o.efx8l0f2').get_attribute("innerHTML") 
    company = self.driver.find_element(By.CLASS_NAME,'css-1xxa55e.efx8l0f1').get_attribute("innerHTML")
    position= self.driver.find_element(By.CLASS_NAME,'css-w5xx65.efx8l0f0').get_attribute("innerHTML")
    joining_date=self.driver.find_element(By.CLASS_NAME,'css-ltu1lh.e7do1940').get_attribute('innerHTML')
      
    try :
        introduction = WebDriverWait(self.driver, random.randint(10, 20)).until(EC.presence_of_element_located((By.CLASS_NAME,'css-1cgtjyh.ee7qfm0'))).get_attribute('innerHTML')
    except :
        introduction =""
      
    attendee ={
       "name":name,
       "company":company,
       "position":position,
       "joinig_date":joining_date,
       "introduction":introduction,
       "links": self.get_links()
      }
    print(attendee)

    # End timer
    end = time.time()
      # Evaluate execution time
    elapsed_time = end - start
    print('Execution time:', elapsed_time, 'seconds')
    """ columns=["name","company","position","joining_date","introduction","offering"]

    self.save_to_csv(attendee,columns,"token2049") """

  # not done
  def get_list(self):
     dict={}
     all=self.driver.find_elements(By.CLASS_NAME,'css-wmoc0c.e1837n183')
     print(len(all))
     for j in range (len(all)):
        list= self.driver.find_elements(By.CLASS_NAME,'css-undnwh.e1837n182')
        print(len(list))
        for i in range (len(list)):
           time.sleep(2)
           key= self.driver.find_element(By.CLASS_NAME,'css-wmoc0c.e1837n183').get_attribute('innerHTML')
           value = self.driver.find_element(By.XPATH,f'/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[4]/ul/li[{i+1}]').get_attribute('innerHTML')
           dict[self.driver.find_element(By.CLASS_NAME,'css-wmoc0c.e1837n183').get_attribute('innerHTML')].append(self.driver.find_element(By.XPATH,f'/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[4]/ul/li[{i+1}]').get_attribute('innerHTML'))
           print(key)
           print(value)
     return dict
  
  #not done
  def get_links(self):
     list=self.driver.find_elements(By.CLASS_NAME,'ant-btn.ant-btn-default.ant-btn-sm')
     array=[]
     for i in range (len(list)):
        array.append(list[i].get_attribute('href'))
     return array   
  
    
  def get_logged_in(self):
    WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/div/button[2]'))).click()
    input_email =self.driver.find_element(By.XPATH,'//*[@id="sign-in_email"]')
    input_email.send_keys(os.getenv('email'))
    self.driver.find_element(By.XPATH,'//*[@id="sign-in"]/button').click()
    time.sleep(random.randint(2, 5)) 
    input_password =self.driver.find_element(By.XPATH,'//*[@id="sign-in_password"]')
    input_password.send_keys(os.getenv('password'))
    self.driver.find_element(By.XPATH,'//*[@id="sign-in"]/button').click()

  def get_data(self):
     # Connect to account
     self.get_logged_in()
     time.sleep(random.randint(2, 5)) 
     # Remove popup
     WebDriverWait(self.driver, random.randint(15, 20)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onesignal-slidedown-cancel-button"]'))).click() 
     # Click on All Attendees sub section
     WebDriverWait(self.driver, random.randint(10, 20)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/section/section/div/main/div[1]/a[2]'))).click() 
     # Click on number results selector 
     time.sleep(random.randint(2, 5)) 
     self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div/section/section/div/main/div[2]/ul/li[10]/div/div[1]/span[2]').click()
     # Select 120 results per page
     time.sleep(random.randint(2, 5)) 
     self.driver.find_element(By.XPATH,'//*[@id="root"]/div/div/section/section/div/main/div[2]/ul/li[10]/div/div[2]/div/div/div/div[2]/div/div/div/div[3]').click()

     page=0
     time.sleep(5)
     while True:
       time.sleep(3)
       list= self.driver.find_elements(By.CLASS_NAME,'css-uc83ol.eud73665')
       page=page+1
       print("Page "+str(page))
       for i in range(len(list)):
         print("Element "+str(i+1))
         """ self.process_page(i+1)
         self.driver.back() """
       if self.is_disable(type="class",locator='ant-pagination-next.ant-pagination-disabled') == True:
          break
       self.driver.find_element(By.CLASS_NAME,'ant-pagination-next').click()
     """   def get_profile_id_and_get_profile_url(self):
     print("test")
     ids=[]
     for element in self.driver.find_elements(By.CLASS_NAME,'css-uc83ol.eud73665'):
       id = element.get_attribute("data-test").split('-')[-1]
       self.driver.get("https://token2049.brella.io/events/token2049singapore/people?profile="+id)
       self.process_page()
       self.driver.back() """

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
token2049 = Token2049()
token2049.get_data() 

