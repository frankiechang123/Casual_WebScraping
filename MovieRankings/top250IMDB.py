import requests
import re
from bs4 import BeautifulSoup
import csv

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
for obj in movieList:
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
    try:
        poster=imdbURL+slate_wrapper.div.a["href"]
    except:
        poster=""
    try:
        trailer=imdbURL+slate_wrapper.find("div",class_=re.compile("videoPreview.*")).div.a["href"]
    except :
        trailer=""
    summary=moviePage.find("div",class_="plot_summary")
    summary_children=[child for child in summary.children]
    try:
        plot=summary_children[1].string.strip()
    except :
        plot=""
    director=summary_children[3].a.string
    writers=summary_children[5].find_all("a")
    try:
        temp=""
        for i,writer in enumerate(writers):
            temp+=writer.string
            if(not i==len(writers)-1):
                temp+=" | "
            
        writers=temp
    except:
        writers=""
    
    try:
        stars=summary_children[7].find_all("a")
        temp=""
        for i,star in enumerate(stars):
            if(i==len(stars)-1):
                break
            temp+=star.string
            if(not i==len(stars)-2):
                temp+=" | "
        stars=temp

    except:
        stars=""
    
    obj["poster"]=poster
    obj["trailer"]=trailer
    obj["plot"]=plot
    obj["writers"]=writers
    obj["director"]=director
    obj["stars"]=stars


with open("imdb_top250.csv","w", newline="") as csvfile:
    catagories=["rank","title","link","rate","length","genre","release","poster","trailer","plot","writers","director","stars"]
    writer=csv.DictWriter(csvfile,catagories)
    writer.writerows(movieList)





    

