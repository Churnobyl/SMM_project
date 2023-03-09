import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # 브라우저의 응답을 기다릴 수 있게 하기 위해
# html요소의 상태를 체크할 수 있게 하기 위해
from selenium.webdriver.support import expected_conditions as EC
import os
import chromedriver_autoinstaller as AutoChrome
import shutil
import time


def chromedriver_update():  # 크롬드라이버 자동 업데이트
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]  # 현재 크롬 버전 확인
    current_list = os.listdir(os.getcwd())  # 현재 디렉토리 파일,폴더 리스트
    chrome_list = []
    for i in current_list:
        path = os.path.join(os.getcwd(), i)  # 현재 디렉토리에 파일,폴더를 더해 주소를 만듦
        if os.path.isdir(path):  # 폴더만 추린다.
            # 'chromedriver.exe'가 해당 폴더에 있는지 확인
            if 'chromedriver.exe' in os.listdir(path):
                chrome_list.append(i)

    # 크롬드라이버가 있는 폴더중에 최신폴더 제외
    old_version = list(set(chrome_list) - set([chrome_ver]))

    for i in old_version:
        path = os.path.join(os.getcwd(), i)  # 구버전 폴더 경로
        shutil.rmtree(path)                    # 구버전 폴더 삭제

    if not chrome_ver in current_list:     # not 최신버전 in 현재 경로:
        AutoChrome.install(True)           # 크롬 드라이버 설치
    else:
        pass                             # pass


youtube_link = 'https://www.youtube.com/watch?v=nfWlot6h_JM&ab_channel=TaylorSwiftVEVO'


class youtube:
    def crawling(link):  # youtube 크롤링
        chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
        path = os.path.join(os.getcwd(), chrome_ver)
        path = os.path.join(path, 'chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_argument("headless")  # 백그라운드 실행
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        driver.get(url=link)

        driver.implicitly_wait(100) # 최대 100초 대기
        try:
            music_crawling = driver.find_elements(
                By.ID, 'default-metadata')[0]  # 제목
            artist_crawling = driver.find_elements(
                By.ID, 'default-metadata')[1]  # 가수
            album_crawling = driver.find_elements(
                By.ID, 'default-metadata')[2]  # 앨범
            music = music_crawling.get_attribute('innerText')
            artist = artist_crawling.get_attribute('innerText')
            album = album_crawling.get_attribute('innerText')

            print(music)
            print(artist)
            print(album)
            return music, artist, album, driver.close()
        except:
            return "error"

    # while(True): # 브라우저 닫힘 방지
    #     pass


if __name__ == "__main__":
    chromedriver_update()  # 크롬드라이버 자동 업데이트
    youtube.crawling(youtube_link)

