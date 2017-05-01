"""
Code for downloading Education Data.
"""
home      = "/Users/yuwang/Documents/PPI/pyDownloader1-master"
file_path = "/Users/yuwang/Documents/PPI/pyDownloader1-master/Education"
import os 
os.chdir(home)

# Load module
from data_downloader import data_downloader as dd

for i in range(1,19):

    ssa_url  = "https://catalog.data.gov/dataset?groups=education2168&page=" + str(i)

    # Instantiate class 
    ssa = dd(ssa_url)
    # Dowload Excel files
    ssa.download_files(save_path = file_path, ext = "csv")
    