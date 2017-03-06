import os
import requests
import urllib
import pandas as pd
from bs4 import BeautifulSoup 

class web_data(object):
    
    def __init__(self, url):
        
        self.url      = url
        self.r        = requests.get(self.url)
        self.raw_html = self.r.text
        self.url_soup = BeautifulSoup(self.raw_html)
        
    def read_files(self, type, ext):
        
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
        
    def download_files(self, save_path, ext):
        
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



