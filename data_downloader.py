import os
import requests
import urllib
import math
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 

# Import html_tables
os.chdir("D:\\pyDownloader1-master")
from html_tables import html_tables

# Define downloader class
class data_downloader(object):
    
    def __init__(self, url):
        
        self.url      = url
        self.r        = requests.get(self.url)
        self.url_soup = BeautifulSoup(self.r.text,"lxml")
        
    #=======================================
    # Method to download data files to disk
    #=======================================
        
    def download_files(self, 
                   save_path, 
                   ext):
   
        self.save_path = save_path
        self.ext = ext
         
        # Get links to files
        self.links = list()
        for link in self.url_soup.find_all("a"):
            this_link = link.get("href")
            if not this_link == None: 
                if this_link.find("." + self.ext) >= 0:
                    self.links.append(urllib.request.urljoin(self.url, this_link))
        
        # Download files to directory
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
    
    #===============================================
    # Method to scrape HTML tables and save to disk
    #===============================================
        
    def download_tables(self, 
                        save_path, 
                        crawl_page       = True, 
                        page_type        = "html", 
                        row_min          = 1, 
                        remove_footnotes = True,
                        indent_dict      = None,
                        remove_blanks    = None):
        
        self.save_path        = save_path
        self.crawl_page       = crawl_page
        self.page_type        = page_type
        self.row_min          = row_min
        self.remove_footnotes = remove_footnotes
        self.indent_dict      = indent_dict
        self.remove_blanks    = remove_blanks
        
        self.pages       = []
        self.tables      = []
        self.file_names  = []
        
        # Crawl page to find all links to pages with tables
        if self.crawl_page == True:
            for link in self.url_soup.find_all("a"):
                this_link = link.get("href")
                if not this_link == None:
                    if this_link[-(len(page_type) + 1):] == "." + self.page_type:
                        self.pages.append(urllib.request.urljoin(self.url, this_link))
            
        # Else simply use self.url 
        else:
            self.pages.append(self.url)
            
        # Scrape tables
        for page in self.pages:
            try:
                page_tables_html = html_tables(page)
                page_tables = page_tables_html.read(remove_footnotes = self.remove_footnotes, 
                                                    indent_dict      = self.indent_dict)
                counter = 1
                for table in page_tables:
                    if len(table) >= self.row_min:
                        self.tables.append(table)
                        file_name = os.path.join(self.save_path, page[page.rfind("/") + 1: -(len(page_type) + 1)] + "_" + str(counter) + ".csv")
                        self.file_names.append(file_name)
                        counter += 1
                    else:
                        next
            except:
                next

        # Remove empty columns
        if self.remove_blanks is not None:
            for n in range(0, len(self.tables)):
                self.tables[n] = self.tables[n].dropna(axis = self.remove_blanks, how = "all")
                
        # Save tables
        for i in range(0, len(self.tables)):
            self.tables[i].to_csv(self.file_names[i], header = False, index = False)








