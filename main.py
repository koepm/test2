from webbrowser import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os

"""
    [수정할 점]
    
    00시 이후 페이지 란이 없는 경우 있으므로 예외처리 필요

"""

os.chmod('/home/g1/source_code/chromedriver', 755)

chrome_path = '/home/g1/source_code/chromedriver'

#search_date = input(" 검색하고 싶은 날짜 입력 ex)20220101, 오늘 = t : ")
search_date = "20220901"

year, month, day = str(datetime.datetime.today())[:10].split('-')
 
if "t" in search_date:
    search_date = year+month+day

url = 'https://sports.news.naver.com/wfootball/news/index?isphoto=N' + "&date=" + search_date

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_path, chrome_options = options)
driver.get(url)

from bs4 import BeautifulSoup


html_1 = driver.page_source
soup_1 = BeautifulSoup(html_1, "html.parser")
pageList = soup_1.find('div', 'paginate').find_all(attrs={"data-id": True})
pageList_1 = []
news_keyword = []

for item in pageList:
    pageList_1.append(int(item['data-id'])-1)

pageList_1.append(len(pageList_1))
pageList_1.reverse()

print("\n")

search_way = input("자동 탐색 : 1 \n키워드 검색 : 2\n입력 : " )

if search_way == "1":
    with open('Hello.txt', 'r') as file:
        for word_1 in file:
            news_keyword.append(word_1.strip("\n"))
            
    for word_2 in news_keyword:
        print("="*50 + " [ " + word_2 + " ] " + "="*50)
        print("\n")

        for page in pageList_1:   
            driver.find_element(By. XPATH, '//*[@id="_pageList"]/'+ 'a[' + str(page) +']').click()
            html_1 = driver.page_source
            soup_1 = BeautifulSoup(html_1, "html.parser")
            content_1 = soup_1.find('div', 'news_list').find_all('li')
            
            for i in content_1:
                if word_2 in i.get_text().split(sep = '\n')[6]:
                    print(i.get_text().split(sep = '\n')[6])
                    print("https://sports.news.naver.com/news?" + i.find("a")["href"].split(sep ="?")[1])
                    print('\n')
                         
elif search_way == "2":
    word_2 = input("검색할 키워드 입력 : ")
    for page in pageList_1:
            
        driver.find_element(By. XPATH, '//*[@id="_pageList"]/'+ 'a[' + str(page) +']').click()
        html_1 = driver.page_source
        soup_1 = BeautifulSoup(html_1, "html.parser")
        content_1 = soup_1.find('div', 'news_list').find_all('li')
    
        for i in content_1:
            if word_2 in i.get_text().split(sep = '\n')[6]:
                print(i.get_text().split(sep = '\n')[6])
                print("https://sports.news.naver.com/news?" + i.find("a")["href"].split(sep ="?")[1])
                print('\n')
    
driver.quit()    

