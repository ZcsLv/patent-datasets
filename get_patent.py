# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time,random,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from faker import Faker

#google专利抓取 by申请人 or 关键词 or 发明人

def get_patents_list(word, App_or_key=True, page=1):
    '''google 专利下载专利文件及 生成专利清单，默认申请人'''
    keys = f"assignee={word}" if App_or_key else f"q={word}" # inventor=任
    main_url = r'https://patents.google.com/?{0}&language=CHINESE&num=100&page={1}'.format(keys, page)
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')  # 后台运行
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=option)
    # driver.maximize_window()  # 最大化
    # driver.set_window_size(1200, 800) # 大小
    driver.implicitly_wait(1)
    driver.get(main_url)
    # print(main_url)

    # 开始注释
    # pdf 下载接口
    pdfs = [i.get_attribute("href") for i in driver.find_elements(By.CSS_SELECTOR,'a.pdfLink.style-scope.search-result-item')]
    # print("pdfs:", pdfs)
    names = [i.text + ".pdf" for i in driver.find_elements(By.CSS_SELECTOR,'h3 span#htmlContent.style-scope.raw-html')]
    names = [x.replace("/", "") for x in names]
    # print("names:", names)
    #
    nums = [i.text for i in driver.find_elements(By.CSS_SELECTOR,'span.style-scope.search-result-item') if "CN" in i.text]
    # nums = [i.text for i in driver.find_elements(By.CSS_SELECTOR,'span.style-scope.search-result-item')]
    nums = [x for x in list(set(nums)) if len(x) != 2]
    # print("nums:", nums)
    file_name_url = zip(pdfs,names)
    # urls = [i.get_attribute("href") for i in driver.find_elements(By.CSS_SELECTOR,'state-modifier>a')]
    dl_dir = r"D:\Temp\{}".format(word)
    os.makedirs(dl_dir) if not os.path.exists(dl_dir) else None
    download(main_url,file_name_url,dl_dir)

def download(url, url_hrefs, path=""):
    ''''下载文件__url_hrefs为'''
    path = path if os.path.isdir(path) else r"D:\Temp"
    import urllib.request as req
    from urllib.parse import urljoin
    opener = req.build_opener()  # urlretrieve add header
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0')]
    req.install_opener(opener)
    urls_root = url[:url.rindex("/") + 1]
    for url_href, filename in url_hrefs:
        pathfile = os.path.join(path, filename)
        url_all = urljoin(url, url_href)
        req.urlretrieve(url_all, pathfile)
    return True    

    
def main():
    start = time.time()
    word = input('请输入公司名：')
    get_patents_list(word, App_or_key=True,page=1)
    done = time.time()
    print("用时{0:.2f}s".format(done - start))


if __name__ ==  '__main__':
    main()