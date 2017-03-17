# pyDownloader readme

The `web_data` class, found in `data_downloader.py`, is a collection of methods that can help scrape government data.   

## Downloading files

The method `download_files` scrapes a given webpage for files of a supplied extension and saves them to disk. The arguments are:

* `save_path`: the file path where you want to save the files; (string; no default)
* `ext`: the type of file extension (either "xls" or "csv") you want to download. (string; no default)

## Downloading HTML tables

The method `download_tables` scrapes HTML tables from a given webpage(s) and saves them to disk as CSVs. The arguments are:

* `save_path`: the file path where you want to save the files; string
* `crawl_page`: tells the scraper whether to scrape for tables on the page of the supplied URL (`False`), or to scrape tables from all of the pages found as hyperlinks on the page of the supplied URL (`True`). (logical; default = True)
* `page_type`: tells the scraper which types of pages you want to scrape tables from (for example, "cfm"). Only relevant if `crawl_page` is True. (string; default = "html")
* `row_min`: tells the scraper to ignore HTML "tables" with fewer than this many rows. This avoids downloading HTML table objects that are not actually data tables. (int; default = 1)
* `row_shift`: fixes rows that are artificially shifted due to merged HTML cells. Negative values shift rows leftward. (int; default = 0)
* `record_shift`: records which rows were shifted and how far, in a new column in the CSV. (logical; default = False)
* `remove_footnotes`: removes footnote super- or sub-scripts from numeric cells in the table. (logical; default = True) 
