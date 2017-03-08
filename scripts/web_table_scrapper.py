import xlwt
import urllib2
wiki = "https://www.w3schools.com/html/html_tables.asp"  # change the url of website here
page = urllib2.urlopen(wiki)
from bs4 import BeautifulSoup
soup = BeautifulSoup(page)
all_tables=soup.find_all('table')
book = xlwt.Workbook()
i=0
for table in all_tables:  # table loop		
	i=i+1
	sh = book.add_sheet('Table'+str(i))
	j = -1
	for th in table.find_all('th'):
		j = j + 1
		sh.write(0,j,th.text)
	row = -1
	for tr in table.find_all('tr'):   # row loop
		row = row + 1
		tds = tr.find_all('td')  
		col = -1
		for k in tds:  # column loop
			col = col + 1
			sh.write(row,col,k.text)

book.save('Scrapped Tables.xls')