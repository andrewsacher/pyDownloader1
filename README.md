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

The method `read_tables` scrapes HTML tables and returns them as `pandas` dataframes. It takes the following arguments:

* `crawl_page`: tells the scraper whether to scrape for tables on the page of the supplied URL (`False`), or to scrape tables from all of the pages found as hyperlinks on the page of the supplied URL (`True`). 
* `page_type`: tells the scraper which types of pages you want to scrape tables from (for example, "cfm"). 
* `row_min`: filters the collection of tables to require a minimum number of rows, to avoid HTML table objects that aren't actually data tables. 
* `shift_rows`: fixes table rows that are artificially shifted due to merged HTML cells. (This does not apply to the DOT tables, and is covered in the next section.)

```python
# Search the DOT data page for hyperlinks that contain HTML tables, and read those into memory
dot_tables = dot.read_tables(crawl_page = True, page_type = "html", row_min = 1)
```

`download_tables` works just like the above method, but instead of reading the HMTL tables into memory, it downloads them to disk as CSV files. It takes the same arguments as above, plus `save_path`:

```python
# Search the DOT data page for hyperlinks that contain HTML tables, and save those as CSVs
dot.download_tables(save_path = my_file, crawl_page = True, page_type = "html", row_min = 1)
```

## Parsing data with merged cells

Some HTML tables have merged cells that `pandas` has difficulty parsing. Consider this table from SSA...

![ssa_html](https://github.com/andrewsacher/pyDownloader1/blob/master/assets/ssa_html.png)

with the cell containing "Old-Age and Survivors Insurance" being two columns merged. If downloaded as is using `download_tables`, the resulting CSV looks like this:

![ssa_csv](https://github.com/andrewsacher/pyDownloader1/blob/master/assets/ssa_csv.png)

The cells are shifted. It this occurs, use the `row_shift` argument. In this case, a value of -1 (with the default being 0) shifts the rows who are misaligned to the left by one cell. The resulting CSV now looks like:

![ssa_csv1](https://github.com/andrewsacher/pyDownloader1/blob/master/assets/ssa_csv1.png)

which is easier to parse. 

To be added: the ability to record indents for similar examples above. 


