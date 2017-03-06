# README

The web_data class, found in data_downloader.py, is a collection of methods that can help scrape government data.   

Below is an example of how to use the `get_files` and `download_files` methods to read and download DOT data. 

```python
# Specify URL of wepage containing 
dot_url = "https://www.rita.dot.gov/bts/sites/rita.dot.gov.bts/files/publications/national_transportation_statistics/index.html"

# Save 
save_path = "C:\\Users\\jricco\\Documents\\PPI projects\\Ballmer\\pyDownloader1\\DOT_files"

# Create a web_data class for DOT data
dot = web_data(dot_url)

# Read all Excel files on the page into memory (returns a list of pandas dataframes)
# Note"
raw_data = dot.get_files("xls")

# Download all CSV files on the page to the specified path
dot.download_files(save_path, "csv")
```
