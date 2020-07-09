import requests
from bs4 import BeautifulSoup

URL="https://www.imdb.com/chart/top/"
imdbURL="www.imdb.com"
req_params={"ref":"nv_mv_250"}

res=requests.get(URL,params=req_params)
print(res.url)
print(res.status_code)
page_html= res.text

soup = BeautifulSoup(page_html, "html.parser")
table=soup.find("tbody",class_="lister-list")
tableRows=table.findAll("tr")
movieList=[]
for row in tableRows:
    rank=row.find("span",attrs={"name":"rk"})["data-value"]
    titleColumn=row.find("td",class_="titleColumn")
    link=imdbURL+titleColumn.a["href"]
    title=titleColumn.a.string
    movieList.append({"rank":rank,"title":title,"link":link})

print(movieList)
    

