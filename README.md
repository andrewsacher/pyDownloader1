# pyDownloader readme

The `web_data` class, found in `data_downloader.py`, is a collection of methods that can help scrape government data.   

Below is an example of how to use the `get_files` and `download_files` methods to read and download DOT data. 

First we want to specify the necessary URLs and file paths: 
```python
# Webpage containing URLs to data files
dot_url = "https://www.rita.dot.gov/bts/sites/rita.dot.gov.bts/files/publications/national_transportation_statistics/index.html"

# File path in which to save downloaded files
save_path = "C:\\Users\\jricco\\Documents\\PPI projects\\Ballmer\\pyDownloader1\\DOT_files"
```

Then we create a web_data object. Note that it is not necessary to supply the "." in a file extension.  

```python
# Instantiate class 
dot = web_data(dot_url)

# Read all Excel files on the page into memory 
raw_data = dot.get_files("xls")

# Download all CSV files on the page to the specified path
dot.download_files(save_path, "csv")
```

Note: `get_files` returns a list of `pandas` dataframes. 