"""
Code for downloading Education Data.
"""
home      = "/Users/yuwang/Documents/PPI/Downloader_Git"
file_path = "/Users/yuwang/Documents/PPI/Downloader_Git/Education_Data"
import os 
os.chdir(home)

# Load module
from data_downloader import data_downloader as dd

for i in range(1,19):
    print("Dealing with page"+str(i)+"...\n")
    ssa_url  = "https://catalog.data.gov/dataset?groups=education2168&page=" + str(i)

    # Instantiate class 
    ssa = dd(ssa_url)
    # Dowload Excel files
    ssa.download_files(save_path = file_path, ext = "csv")
    ssa.download_files(save_path = file_path, ext = "xls")
    ssa.download_files(save_path = file_path, ext = "xlsx")
    ssa.download_files(save_path = file_path, ext = "zip")  
    ssa.download_files(save_path = file_path, ext = "pdf")
    ssa.download_files(save_path = file_path, ext = "txt")
    