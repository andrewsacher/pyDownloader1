import os
setting_path = os.path.dirname(os.path.realpath('data_downloader.py'))
os.chdir(setting_path)
file_path = setting_path + "\\Table_Downloaded"
ssa_url  = "https://www.dhs.gov/immigration-statistics/yearbook/2015"

 

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