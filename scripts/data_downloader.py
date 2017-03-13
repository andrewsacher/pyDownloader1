import os
import requests
import urllib
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 

class web_data(object):
    
    def __init__(self, url):
        
        self.url      = url
        self.r        = requests.get(self.url)
        self.raw_html = self.r.text
        self.url_soup = BeautifulSoup(self.raw_html)
    
    # Method to read data files into memory  
    def read_files(self, ext):
        
        self.ext = ext 
        
        # Get links to files
        self.links = list()
        for link in self.url_soup.find_all("a"):
            this_link = link.get("href")
            if not this_link == None: 
                if this_link.find("." + self.ext) >= 0:
                    self.links.append(urllib.request.urljoin(self.url, this_link))
        
        # Bring data into memeory
        self.mem_data = list()
        self.failed_links = list()
        for link in self.links:
            try:
                if self.ext == "xls":
                    self.mem_data.append(pd.read_excel(link))
                if self.ext == "csv":
                    self.mem_data.append(pd.read_csv(link))
            except:
                self.failed_links.append(link)
        if len(self.failed_links) > 0:
            print("The following files could not be read into memory:")
            for s in self.failed_links:
                print(s)
        
        return(self.mem_data)
    
    # Method to download data files to disk
    def download_files(self, ext, save_path):
        
        self.ext = ext
        
        # Get links to files
        self.links = list()
        for link in self.url_soup.find_all("a"):
            this_link = link.get("href")
            if not this_link == None: 
                if this_link.find("." + self.ext) >= 0:
                    self.links.append(urllib.request.urljoin(self.url, this_link))
        
        # Download files to directory
        self.save_path = save_path
        
        self.failed_links = list()
        for link in self.links:
            file_path = os.path.join(self.save_path, link[link.rfind("/") + 1: ])
            try:
                urllib.request.urlretrieve(link, file_path)
            except:
                self.failed_links.append(link)
        
        if len(self.failed_links) > 0:
            print("The following files could not be downloaded:")
            for s in self.failed_links:
                print(s)
    
    # Method to scrape HTML tables into memory
    def read_tables(self, crawl_page = False):
        
        self.crawl_page = crawl_page
        self.pages = list()
        self.tables = list()
        
        # Crawl page to find all links to pages with tables
        if self.crawl_page == True:
            for link in self.url_soup.find_all("a"):
                this_link = link.get("href")
                if not this_link == None:
                    if this_link[-5:] == ".html":
                        self.pages.append(urllib.request.urljoin(self.url, this_link))
            
        # Else simply use self.url 
        else:
            self.pages[0] = self.url
        
        # Scrape tables 
        for page in self.pages:
            try:
                page_tables = pd.read_html(page, flavor = "bs4", header = 0)
                for table in page_tables:
                    self.tables.append(table)
            except:
                next

        return(self.tables)
  
    # Method to scrape HTML tables and save to disk
    def save_tables(self, save_path,  crawl_page = False):
        
        self.save_path = save_path
        self.crawl_page = crawl_page
        self.pages = list()
        self.tables = list()
        self.file_names = list()
        
        # Crawl page to find all links to pages with tables
        if self.crawl_page == True:
            for link in self.url_soup.find_all("a"):
                this_link = link.get("href")
                if not this_link == None:
                    if this_link[-5:] == ".html":
                        self.pages.append(urllib.request.urljoin(self.url, this_link))
            
        # Else simply use self.url 
        else:
            self.pages[0] = self.url
        
        # Scrape tables
        for page in self.pages:
            try:
                page_tables = pd.read_html(page, flavor = "bs4", header = 0)
                counter = 1
                for table in page_tables:
                    self.tables.append(table)
                    file_name = os.path.join(self.save_path, page[page.rfind("/") + 1: -5] + "_" + str(counter) + ".csv")
                    self.file_names.append(file_name)
                    counter += 1
            except:
                next

        # Save tables
        for i in range(0, len(self.tables)):
            self.tables[i].to_csv(self.file_names[i])
