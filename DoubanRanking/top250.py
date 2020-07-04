import copy
import requests
from bs4 import BeautifulSoup
import csv


def getInfo(html):
    dir_list = []
    soup = BeautifulSoup(html, "html.parser")
    for div in soup.find_all("div", class_="item"):
        url = div.find("a", class_="")
        url = url["href"]
        # print(url)
        num = div.em.text.strip()
        title_html = div.find_all("span", class_="title")
        name = ""
        for stuff in title_html:
            name += stuff.text.strip()
        other_title_html = div.find_all("span", class_="other")
        for stuff in other_title_html:
            name += stuff.text.strip()
        # print(name)
        info_html = div.find("div", class_="bd")
        description = info_html.find("p", class_="")
        description = description.text.strip()
        try:
            director = description[4:description.index("主")]
            director = director.strip()
        except:
            director = "not found"
        # print(director)
        temp = description.index("\n")
        time = description[temp:description.index("/", temp)]
        time = time.strip()
        # print(time)
        timepos = description.index(time)
        origin = description[timepos+6:description.index("/", timepos+6)]
        origin = origin.strip()
        # print(origin)

        temppos = description.index("/", timepos+6)+1
        genre = description[temppos:]
        genre = genre.strip()
        # print(genre)
        review = info_html.find("div", class_="star")
        rating = review.find("span", class_="rating_num").text.strip()
        # print(rating)
        spanlist = review.find_all("span")
        num_review = spanlist[len(spanlist)-1].text.strip("人评价")
        # print(num_review)
        dir_list.append({
            "rank": num,
            "name": name,
            "director": director,
            "time": time,
            "origin": origin,
            "genre": genre,
            "rating": rating,
            "num_review": num_review,
            "url": url
        })
    return dir_list


req_header = {"Host": "movie.douban.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"}
start = 0
movies = []
while(start <= 250):
    req_params = {"start": start}
    r = requests.get("https://movie.douban.com/top250",
                     headers=req_header, params=req_params)
    print(r.status_code)
    print(r.url)

    page_html = r.text
    movielist = getInfo(page_html)
    movies += copy.deepcopy(movielist)

    start += 25

with open("movies.csv", "w", newline="", encoding="utf-8") as csvfile:
    catagories = ["rank", "name", "director", "time",
                  "origin", "genre", "rating", "num_review", "url"]
    writer = csv.DictWriter(csvfile, catagories)
    writer.writerows(movies)
