# pyDownloader readme

The `web_data` class, found in `data_downloader.py`, is a collection of methods that can help scrape government data.   

Below is an example of how to use the various methods to read and download DOT data. 

First we want to specify the necessary URLs and file paths, and create a `web_data` object: 

```python
# Webpage containing URLs to data files
dot_url = "https://www.rita.dot.gov/bts/sites/rita.dot.gov.bts/files/publications/national_transportation_statistics/index.html"

# File path in which to save downloaded files
my_path = "C:\\Users\\jricco\\Documents\\PPI projects\\Ballmer\\pyDownloader1\\DOT_files"

# Instantiate class 
dot = web_data(dot_url)
```

The method `read_files` reads all files of the supplied extension into memory (either "xls" or "csv") and returns a list of `pandas` dataframes:
```python
# Read all Excel files on the page into memory 
raw_data = dot.read_files(ext = "xls")
```
`download_files` downloads these files to disk:
```python
# Download all CSV files on the page to the specified path
dot.download_files(ext = "csv", save_path = my_path)
```

The method `read_tables` scrapes HTML tables and returns them as `pandas` dataframes. The `crawl_page` argument tells the scraper whether to scrape for tables on the page of the supplied URL (`False`), 
or to scrape tables from all of the pages found as hyperlinks on the page of the supplied URL (`True`). The `page_type` argument tells the scraper which types of pages you want to scrape tables from (for example, "cfm"):

```python
# Search the DOT data page for hyperlinks that contain HTML tables, and read those into memory
dot_tables = dot.read_tables(crawl_page = True, page_type = "html")
```

`download_tables` works just like the above method, but instead of reading the HMTL tables into memory, it downloads them to disk as CSV files:

```python
# Search the DOT data page for hyperlinks that contain HTML tables, and save those as CSVs
dot.download_tables(save_path = my_file, crawl_page = True, page_type = "html")
```