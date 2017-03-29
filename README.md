# pyDownloader readme

The modules `html_tables` and `data_downloader` contain methods that can help scrape and download government data. 

## data_downloader 

This module contains two methods that can download data to disk:

### download_files

This method scrapes a supplied webpage and downloads all files of a given extension. It takes two arguments: 

* `save_path`: the file path where you want to save the files; (string; no default)
* `ext`: the type of file extension (either "xls" or "csv") you want to download. (string; no default)

As an example, let's download all the Excel files from the SSA's 2015 Annual Statistic Supplement:

```python
home      = "local file path of your github project"
file_path = "file path where you want to save your data"
ssa_url  = "https://www.ssa.gov/policy/docs/statcomps/supplement/2015/index.html"

import os 
os.chdir(home)

# Load module
from data_downloader import data_downloader as dd 

# Instantiate class 
ssa = dd(fwha_url)

# Dowload Excel files
ssa.download_files(save_path = file_path, ext = "xls")
```

### download_tables

This method calls `html_tables`, which scrapes HTML tables into memory as pandas dataframes, then saves each table as a CSV. The arguments are: 

* `save_path`: the file path where you want to save the files; string
* `crawl_page`: tells the scraper whether to scrape for tables on the page of the supplied URL (`False`), or to scrape tables from all of the pages found as hyperlinks on the page of the supplied URL (`True`). (logical; default = `True`)
* `page_type`: tells the scraper which types of pages you want to scrape tables from (for example, "cfm"). Only relevant if `crawl_page` is True. (string; default = "html")
* `row_min`: tells the scraper to ignore HTML "tables" with fewer than this many rows. This avoids downloading HTML table objects that are not actually data tables. (int; default = 1)
* `remove_footnotes`: removes footnote super- or sub-scripts from numeric cells in the table. (logical; default = True) 
* `indent_dict`: takes a dictionary of html classes (found in a page's CSS stylesheet) that correspond to indents in the first column of a table. It records the value of these indents in a separate column. (dicctionary; default = `None`) 
* `remove_blanks`: removes rows and/or columns that are completely blank. It takes a list in the form of [row = {0, 1}, col = {0, 1}]. (list; default = `None`)

Building on the example above:

```python
# Set up indentation dictionary
ssa_indents = {"stub0": 0, "stub1" : 1, "stub2": 2, "stub3": 3}

# Download all HTML files
ssa.download_tables(save_path = file_path, indent_dict = ssa_indents)
```
