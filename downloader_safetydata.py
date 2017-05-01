home      = "D:\pyDownloader1-master"
file_path = "D:\Table_Downloaded"
ssa_url  = "https://www.dhs.gov/immigration-statistics/yearbook/2014"

import os 
os.chdir(home)

# Load module
from data_downloader import data_downloader as dd 

for i in range(1,5):

    ssa_url  = "https://catalog.data.gov/dataset?q=&ext_location=&ext_prev_extent=-100.92041015625%2C19.72534224805787%2C-98.32763671875%2C21.779905342529645&sort=views_recent+desc&ext_bbox=&groups=safety3175&_groups_limit=0&_groups_sortAlpha=asc&page=" + str(i)

    # Instantiate class 
    ssa = dd(ssa_url)
    # Dowload Excel files
    ssa.download_files(save_path = file_path, ext = "csv")
    ssa.download_files(save_path = file_path, ext = "xls")
    ssa.download_files(save_path = file_path, ext = "xlsx")