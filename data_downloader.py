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
        
    def get_excel(self):
        
        # Get links to Excel files
        self.links = list()
        for link in self.url_soup.find_all("a"):
            this_link = link.get("href")
            if not this_link == None: 
                if this_link.find("xls") >= 0:
                    self.links.append(this_link)
        
        # Bring data into memeory
        self.excel_data = list()
        self.failed_links = list()
        for link in self.links:
            try:
                self.excel_data.append(pd.read_excel(link))
            except:
                self.failed_links.append(link)
        if len(self.failed_links) > 0:
            print("The following spreadsheets could not be read into memory:")
            for s in self.failed_links:
                print(s)
        
        return(self.excel_data)
        
    def download_excel(self, save_path):
        
        # Get links to Excel files
        self.links = list()
        for link in self.url_soup.find_all("a"):
            this_link = link.get("href")
            if not this_link == None: 
                if this_link.find("xls") >= 0:
                    self.links.append(this_link)
        
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
            print("The following spreadsheets could not be downloaded:")
            for s in self.failed_links:
                print(s)


# An example
dot_url = "https://www.rita.dot.gov/bts/sites/rita.dot.gov.bts/files/publications/national_transportation_statistics/index.html"
path = "C:\\Users\\jricco\\Documents\\PPI projects\\Ballmer\\pyDownloader1\\DOT_excel_files"

dot = web_data(dot_url)

dot.download_excel(path)
raw_data = dot.get_excel()
