"""

@RAPHABIZ

"""

import csv
import os
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

driver = webdriver.Chrome()
driver.get("https://www.alchemy.com/dapps")
driver.set_window_size(1280, 680)


class Alchemy():
  def __init__(self):
        """ self.driver = webdriver.Chrome()
        self.driver.get("https://www.alchemy.com/dapps")
        self.driver.set_window_size(1280, 680) """

  def process_page(self,i):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'/html/body/div[1]/main/section[1]/div/div/div/div/div/div[2]/header/div/div[2]/div[1]/div[{i}]'))).click()
    time.sleep(1)
    title = driver.find_element(By.XPATH,'//*[@id="w-node-_8e8f92b4-41cd-c97d-c0c2-f11963c19fa0-551a0e8a"]/div[1]/div[2]/h1[2]').get_attribute("innerHTML")
    image_url = driver.find_element(By.XPATH,'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab962-551a0e8a"]/img').get_attribute("src")
    twitter= driver.find_element(By.XPATH,'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab977-551a0e8a"]/div[1]/a[2]').get_attribute("href")
    website=driver.find_element(By.XPATH,'//*[@id="w-node-a6e2b1fc-baea-8113-f670-112998a3fa78-551a0e8a"]/a[2]').get_attribute('href')
    description = driver.find_element(By.XPATH,'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab990-551a0e8a"]/p').get_attribute('innerHTML')
    chains = driver.find_element(By.XPATH,'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab966-551a0e8a"]/div[3]/div[2]').get_attribute('innerHTML')
    dapps ={
       "title":title,
       "image":image_url,
       "twitter":twitter,
       "website":website,
       "tags": self.get_tags(),
       "chains":chains,
       "description":description
    }
    columns=["title","image","twitter","website","tags","chains","description"]

    self.save_to_csv(dapps,columns,"alchemy")

  def get_tags(self):
     list= driver.find_elements(By.CLASS_NAME,'item-header_tag.is--parent.w-inline-block')
     list2= driver.find_elements(By.CLASS_NAME,'item-header_tag.is--child.w-inline-block')
     array=[]
     for i in range(len(list)):
        array.append(driver.find_element(By.XPATH,f'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab968-551a0e8a"]/div[1]/div/div[{i+1}]/a/div').get_attribute("innerHTML"))
     for i in range(len(list2)):
        array.append(driver.find_element(By.XPATH,f'//*[@id="w-node-_0b28749b-1df0-9158-e12d-ade7d09ab968-551a0e8a"]/div[2]/div/div[{i+1}]/a/div').get_attribute("innerHTML"))
     return array 
  

  def is_element_present(self,driver, locator):
    try :
      WebDriverWait(driver, 20).until(EC.element_to_be_clickable(By.CLASS_NAME, locator))
      print("Element exists")
      return True
    except : 
      print("Element does not exist")
      return False
    """  try:
        driver.find_element(By.CLASS_NAME,locator)
    except:
        return False
    return True """
    
  def get_data(self):
     page=0
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
     print("done")
      
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

