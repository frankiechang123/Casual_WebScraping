import requests
import re
from bs4 import BeautifulSoup

URL="https://www.imdb.com/chart/top/"
imdbURL="https://www.imdb.com"
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

#look into each link
#for obj in movieList:
obj=movieList[0]
link=obj["link"]
moviePage=requests.get(link)
print(moviePage.status_code)
print(moviePage.url)
moviePage=BeautifulSoup(moviePage.text,"html.parser")
overview=moviePage.find("div",class_="heroic-overview")
year=overview.find("span",attrs={"id":"titleYear"}).string
overview=[string for string in overview.find(class_="subtext").stripped_strings]

rate=overview[0]
length=overview[2]
genre=overview[4]
release=overview[6]
obj["rate"]=rate
obj["length"]=length
obj["genre"]=genre
obj["release"]=release

slate_wrapper=moviePage.find("div",class_="slate_wrapper")
poster=imdbURL+slate_wrapper.div.a["href"]
trailer=imdbURL+slate_wrapper.find("div",class_=re.compile("videoPreview.*")).div.a["href"]

summary=moviePage.find("div",class_="plot_summary")
summary_children=[child for child in summary.children]

plot=summary_children[1].string.strip()
director=summary_children[3].a.string
writers=summary_children[5].find_all("a")
temp=""
for i,writer in enumerate(writers):
    temp+=writer.string
    if(not i==len(writers)-1):
        temp+=" | "
    
writers=temp

print(plot)
print(writers)
print(director)






    

