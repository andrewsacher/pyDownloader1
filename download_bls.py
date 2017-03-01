#=============================================
# SCRIPT TO DOWNLOAD BLS DATA FROM TEXT FILES
#=============================================

import requests
import urllib
from bs4 import BeautifulSoup 

# Parameters
save_path = "C:\\Users\\jricco\\Documents\\PPI projects\\Ballmer\\Data\\BLS data\\Raw data\\" # Where you want to output files

#==========================
# GET INFO ON EACH CONCEPT
#==========================

# Get HTML  
base_url = "http://download.bls.gov"
r = requests.get(base_url + "/pub/time.series")
raw_html = r.text
soup = BeautifulSoup(raw_html)

# Get list of URLS for concept codes
concept_urls = list()
for link in soup.find_all("a"):
    this_link = link.get("href")
    if len(this_link) == 20:
        concept_urls.append(link.get("href"))

# Get list of data file URLs 
data_urls = list()
for i in range(0, len(concept_urls)):
    r = requests.get(base_url + concept_urls[i])
    raw_html = r.text
    soup = BeautifulSoup(raw_html)
    
    for j in soup.find_all("a"):
        this_string = j.get("href")
        if this_string.find("data") >= 0:
            data_urls.append(this_string)

# Get list of series info file URLs 
series_info_urls = list()
for i in range(0, len(concept_urls)):
    concept_code = concept_urls[i][17:19]
    series_info_urls.append(base_url + concept_urls[i] + concept_code + ".series")

#===================
# PULL DATA TO DISK
#===================

# Download data files
data_path = save_path + "data\\"
for i in range(0, len(data_urls)):
    series_name = data_urls[i][20:]
    file_name = data_path + series_name + ".txt"
    try:
        urllib.request.urlretrieve(base_url + data_urls[i], filename = file_name)
    except:
        print("No data available for " + data_urls[i] + ".")

# Download series info files
series_info_path = save_path + "series_info\\"
for i in range(0, len(series_info_urls)):
    series_name = series_info_urls[i][-9:]
    file_name = series_info_path + series_name + ".txt"
    try:
        urllib.request.urlretrieve(series_info_urls[i], filename = file_name)
    except:
        print("No data available for " + series_info_urls[i] + ".")


