#!/usr/bin/env python
# coding: utf-8

# In[1]:


#모듈 임포트
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import pandas as pd
from tqdm import notebook

#최대로 스크롤 내리는 함수 정의
def doScrollDown(whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(0.5)
        if datetime.datetime.now() > end:
            break

#브라우저 설정 및 새 브라우저 열기
options = webdriver.ChromeOptions()
options.add_argument('--start-fullscreen')
driver = webdriver.Chrome('./chromedriver', options = options) 
driver.maximize_window()
driver.get('https://brunch.co.kr/keyword/프랑스여행')

#50초 동안 스크롤 내리기
doScrollDown(50)

#글 제목과 본문을 저장할 리스트 생성
title_list =[]
article_list = []

#제목을 수집해 title_list에 저장 -> 클릭해 새탭에서 열기 -> 본문 글 수집 -> 탭 종료 및
#검색결과 화면으로 돌아감 -> 반복
title = driver.find_elements_by_class_name("tit_subject")
for k in notebook.tqdm(title, desc = 'progress bar'):
    title_list.append(k.text)
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).click(k).key_up(Keys.CONTROL).perform()
    driver.switch_to.window(driver.window_handles[-1])
    
    article = driver.find_elements_by_class_name("item_type_text")
    join_article_list = []
    for j in article:
        join_article_list.append(j.text)
        fully_combined = " ".join(map(str, join_article_list))
    article_list.append(fully_combined)
    time.sleep(1)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    doScrollDown(1)

#데이터프레임으로 정리, export
brunch_df = pd.DataFrame(data = {'Title' : title_list, 'Article' : article_list})
brunch_df.to_csv('brunch_df.csv', index=False, encoding="utf-8-sig")


# In[ ]:




