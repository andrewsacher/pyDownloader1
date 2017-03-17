import os
import requests
import urllib
import math
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup 

class web_data(object):
    
    def __init__(self, url):
        
        self.url      = url
        self.r        = requests.get(self.url)
        self.raw_html = self.r.text
        self.url_soup = BeautifulSoup(self.raw_html)

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
                        crawl_page = True, 
                        page_type = "html", 
                        row_min = 1, 
                        row_shift = 0, 
                        record_shifts = False, 
                        remove_footnotes = True):
        
        self.save_path        = save_path
        self.crawl_page       = crawl_page
        self.page_type        = page_type
        self.row_min          = row_min
        self.row_shift        = row_shift
        self.record_shifts    = record_shifts
        self.remove_footnotes = remove_footnotes
        
        self.pages       = list()
        self.tables      = list()
        self.file_names  = list()
        
        # Crawl page to find all links to pages with tables
        if self.crawl_page == True:
            for link in self.url_soup.find_all("a"):
                this_link = link.get("href")
                if not this_link == None:
                    if this_link[-(len(page_type) + 1):] == "." + self.page_type:
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
                    if len(table) >= self.row_min:
                        self.tables.append(table)
                        file_name = os.path.join(self.save_path, page[page.rfind("/") + 1: -(len(page_type) + 1)] + "_" + str(counter) + ".csv")
                        self.file_names.append(file_name)
                        counter += 1
                    else:
                        next
            except:
                next
                
        # Fix rows
        if self.row_shift != 0:
            for n in range(0, len(self.tables)):
                self.shift_index = list()
                for i in range(0, len(self.tables[n])):
                    this_row = self.tables[n].iloc[i, ]
                    if this_row.isnull()[0]:
                        if all(this_row.isnull()):
                            self.shift_index.append(0)
                        else:
                            self.shift_index.append(self.row_shift)
                        for j in range(0, len(this_row)):
                            self.tables[n].iloc[i, j] = this_row.shift(periods = self.row_shift)[j]
                    else:
                        self.shift_index.append(0)
                if all(np.array(self.shift_index) == 0):
                    next
                else:
                    self.tables[n] = self.tables[n].assign(shift = self.shift_index)
                    
        # Remove footnotes
        if self.remove_footnotes:
            
            def strip_footnotes(x):
                if isinstance(x, str):
                    end = x[-2:]
                    match_obj = re.match("([0-9])\D", end)
                    if match_obj:
                        return(x[:-1])
                    else:
                        return(x)
                else:
                    return(x)

            for n in range(0, len(self.tables)):
                for i in range(0, len(self.tables[n].columns)): 
                    if str(self.tables[n].iloc[:, i].dtype) == "float64":
                        next
                    else:
                        self.tables[n].iloc[:, i] = self.tables[n].iloc[:, i].apply(strip_footnotes)
                
        # Save tables
        for i in range(0, len(self.tables)):
            self.tables[i].to_csv(self.file_names[i], index = False)


        
    
