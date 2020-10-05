import bs4
import lxml
import openpyxl
import pandas as pd
import requests

url = 'https://en.wikipedia.org/wiki/Amr_Diab'

res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, "lxml")
soup.select('li')
a = soup.select('li')[28:62]
song = []
f = []
title = soup.select('title')[0].getText()

i = 0
while i < 34:
    data = a[i].getText()
    x = data.split(": ")
    year = x[0]
    song = x[1]
    y = song.split("(")
    album = y[0]
    translation = y[1][:-1]
    list = []
    list.append(year)
    list.append(album)
    list.append(translation)
    f.append(list)
    i = i+1

wb = openpyxl.Workbook()
ws = wb.active

for rows in f:
    ws.append(rows)

wb.save('AmrDiab.xlsx')

df = pd.read_excel('AmrDiab.xlsx', header=None)
df.columns = ['Year', 'Album', 'Translation']
df.to_excel('AmrDiab.xlsx')

# print(song)
