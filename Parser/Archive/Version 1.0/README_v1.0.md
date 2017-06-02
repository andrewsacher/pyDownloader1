# Parser.py readme

The modules `parser` contain method that can parse excel data into time series. As an example, we now parse the excel file called `sbsummar.xls` in the folder `Sample_Data` and put the result in `Parsed_Data`.

```python
#home is the directory where you put your Parser.py
home =  "/Users/yuwang/Documents/PPI/Downloader_Git/pyDownloader1/Parser"

# data_directory is the directory of the excel file you want to be parsed
data_directory = "/Users/yuwang/Documents/PPI/Downloader_Git/pyDownloader1/Parser/Sample_Data/sbsummar.xls"

#output_directory is the folder directory you want the result to be put
output_directory = "/Users/yuwang/Documents/PPI/Downloader_Git/pyDownloader1/Parser/Parsed_Data"

import os 
os.chdir(home)

# Load function
from Parser import parser as pp

# Parse the excel data
pp(data_directory,output_directory)
```
For now, the Parser.py v 1.0 made several assumptions towards the excel file:
* One table in each sheet.
* Years must be distributed in consecutive cells, no matter in rows or columns.

and there are several problems to be solved in next version:
* How to parse descriptions, units and explanations?
* How to figure out indent logic automatically?