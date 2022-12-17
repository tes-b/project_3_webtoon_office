import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

class Crawler:
    def __init__(self):
        pass

    def get_page(self,page_url):
        soup = None
        page = None

        with requests.get(page_url) as page:
            try:
                page.raise_for_status()
            except HTTPError as Err:
                print(Err)
            else:
                soup = BeautifulSoup(page.content, 'html.parser')

        return soup, page

    def collect_naver_data(self):
        print("naver_webtoon_crawling starts.")
        BASE_URL = "https://comic.naver.com"    
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        # day = "mon"
        webtoons = []        
        
        for day in days:
            
            FULL_URL = BASE_URL + f"/webtoon/weekdayList?week={day}&order=ViewCount&view=list"
            # print(FULL_URL)
            soup, page = self.get_page(FULL_URL)    
            
            trs = soup.select("tr")
            for i, tr in enumerate(trs):
                # if i > 5: break
                # print(tr)
                # print("======================================")
                wt = {}
                if None == tr.select_one("a"): continue
                wt["title"] = tr.select_one("a").string
                wt["platform"] = "naver"
                wt["link"] = BASE_URL + tr.select_one("a")["href"]
                wt["rate"] = float(tr.select_one(".rating_type > strong").string)
                wt["site_id"] = int(re.findall(r"\d+", wt["link"])[0])
                soup_into, page_into = self.get_page(wt["link"])
                author = soup_into.select_one(".wrt_nm").string.strip()
                wt["artist"] = str.split(author," / ")
                genre = soup_into.select_one(".genre").string.strip()
                wt["genre"] = str.split(genre,", ")
                age = soup_into.select_one(".age").string.strip()
                wt["for_adult"] = True if age == "18세 이용가" else False
                wt["day"] = day
                wt["views_rank"] = i
                wt["synopsis"] = soup_into.select_one("div.comicinfo > div.detail > p").get_text()
                wt["thumbnail_link"] = soup_into.select_one("div.comicinfo > div.thumb > a > img")["src"]
                # print(wt)
                webtoons.append(wt)
                
                # print(toon)
            print(day + " DONE")
            
        print(len(webtoons))
        return webtoons

    def save_html(name, filename):
        file = open(filename, 'w')
        file.write(str(name))
        file.close()
        print(f"Save {filename}")






"""
카카오 웹툰 크롤러
카카오 웹툰 페이지 구조 다소 복잡
시스템 및 평가 지표도 네이버와 다소 달라
프로젝트 마감까지 완료하기 힘들 것으로 보임
차후 추가
"""

# ====================================================== 
# def collect_kakao_data():
#     from selenium import webdriver
#     import os 
#     import time

#     PATH = os.getcwd() + "/flask_app/chromedriver"

#     BASE_URL = "https://webtoon.kakao.com"
#     days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
#     webtoons = []

#     for day in days:
#         FULL_URL = BASE_URL + f"/original-webtoon?tab={day}"

#         browser = webdriver.Chrome(PATH)
#         browser.maximize_window()
    
#         print(FULL_URL)
#         browser.get(FULL_URL)
#         time.sleep(1)
#         html = browser.page_source
#         soup = BeautifulSoup(str(html),'html.parser')
#         body = soup.find("body")
#         next = body.select_one("#__next > .h-full > main > div > div")
#         uniqueid = next.find(__uniqueid="2")
#         div6 = uniqueid.select_one("div > .swiper-slide.swiper-slide-active > div > div")
#         div7 = div6.select_one(".relative.day-section")
#         div8 = div7.select("div")[19]
#         relatives = div8.select("div")
    
#         for rel in relatives:
        
#             links = []
#             bg = rel.select_one(".relative.w-full.bg-transparent")
#             if None != bg:
#                 # GET LINK
#                 a = bg.select_one("a")
#                 if None != a:
#                     link = BASE_URL + a["href"]
#                     print(link)
#                     links.append(link)
#                     # wt = {}
#                     # wt["link"] = BASE_URL + a["href"]
#                     # print(wt["link"])
                
#                     # GET FOR ADULT
#                     # wt["for_adult"] = False
#                     # divs = bg.select_one("div").select("div")
                
#                     # for div in divs:
#                     #     div2 = div.select_one("div")
#                     #     if None != div2:
#                     #         img = div2.select_one("img")
#                     #         if None == img:
#                     #             # print(img["alt"])
#                     #             # webtoons.append(wt)
#                     #             links.append(link)
    

#         for link in links:
#             print(link)
#             wt = {}
#             content, page = get_page(link)
#             if None == content: continue
#             wt["link"] = link

#             main = content.select_one("main")
#             strings = list(main.stripped_strings)
#             wt["title"] = strings[1]
#             wt["platform"] = "kakao"
#             wt["site_id"] = int(re.findall(r"\d+", wt["link"])[0])
        
#             wt["author"] = str.split(strings[2],", ")
#             wt["genre"] = str.split(strings[3],"/")

#             wt["day"] = day
        
#             wt["views"] = strings[4]
#             wt["likes"] = strings[5]

#             webtoons.append(wt)

#     for wt in webtoons:
#         print(wt["title"])
#     # print(webtoons)

#     return webtoons

# collect_kakao_data()
# ======================================================

# naver_webtoons = collect_naver_data()