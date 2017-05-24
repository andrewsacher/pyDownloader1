home      = "D:\pyDownloader1-master"
file_path = "D:\Table_Downloaded"
ssa_url  = "https://www.dhs.gov/immigration-statistics/yearbook/2015"

import os 
os.chdir(home)

# Load module
from data_downloader import data_downloader as dd 

    # Instantiate class 
ssa = dd(ssa_url)
    # Dowload Excel files
ssa.download_files(save_path = file_path, ext = "csv")
ssa.download_files(save_path = file_path, ext = "xls")
ssa.download_files(save_path = file_path, ext = "xlsx")
ssa.download_files(save_path = file_path, ext = "zip")
ssa.download_files(save_path = file_path, ext = "rar")