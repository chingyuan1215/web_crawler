# selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.action_chains import ActionChains
from pandas.core.frame import DataFrame

import time
import pandas as pd


options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
options.add_experimental_option('prefs', prefs)
options.add_argument("disable-infobars")

# ------ 設定要前往的網址 ------
url = 'https://www.facebook.com'  

# ------ 登入的帳號與密碼 ------
username = ''
password = ''


# ------ 透過Browser Driver 開啟 Chrome ------
driver = webdriver.Chrome('C:/Users/user/Downloads/chromedriver.exe')        


# -------------------------------無頭-------------------------------------------
# ------------------------------------------------------------------------------
# ---------------  無頭模式   ---------------------
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# # ---------------            ---------------------
# options.add_experimental_option('prefs', prefs)
# options.add_argument("disable-infobars")
# # ------ 設定要前往的網址 ------
# url = 'https://www.facebook.com/moea.gov.tw'
# # ------ 登入的帳號與密碼 ------
# username = '0919039153'
# password = 'Moose66728140'
# # ------ 透過Browser Driver 開啟 Chrome ------
# driver = webdriver.Chrome(chrome_options=options)
# # ------ 前往該網址 ------
# driver.get(url)
# time.sleep(1)
# # ------------------------------------------------------------------------------
# # ------------------------------------------------------------------------------
# for i in range(3):
#     js = 'window.scrollTo(0, document.body.scrollHeight);'
#     driver.execute_script(js)
#     time.sleep(6)
# time.sleep(6)
# catchLike()

# ------ 前往該網址 ------
driver.get(url)        

# ------ 賬號密碼 ------
# time.sleep(1)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
elem = driver.find_element_by_id("email")
elem.send_keys(username)

elem = driver.find_element_by_id("pass")
elem.send_keys(password)        

elem.send_keys(Keys.RETURN)
time.sleep(5)


#檢查有沒有被擋下來
if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
    driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()


spec_url = 'https://www.facebook.com/USTARTFans/'
driver.get(spec_url)

def collection(url):
    # 切換頁面
    driver.get(url)
    time.sleep(5)

    # 手動 點除封鎖 通知
    # 滑動
    for i in range(10):
        js = 'window.scrollTo(0, document.body.scrollHeight);'
        driver.execute_script(js)
        time.sleep(3)
    
    article_like = catchLike()
    length = len(article_like)

    article_share = catchShare(length)
    article_comment_nums = catchCommentNums(length)
    article_time = catchPostTime(length)
    article_content = catchArticleContent(length)
    article_link = catchLink(length)
    article_comment = catchComment(length)

    result={"article_content" : article_content , 
            "article_time" : article_time ,
            "numbers of like" : article_like ,
            "numbers of share" : article_share,
            "numbers of comment" : article_comment_nums,
            "article_link" : article_link,
            "article_comment" : article_comment
           }
    # print(len(article_like),article_like)
    # print(len(article_share),article_share)
    # print(len(article_comment_nums),article_comment_nums)
    # print(len(article_link),article_link)
    # print(len(article_content),article_content)

    result = DataFrame(result)
    result.to_csv('FBcrawler.csv', encoding = 'utf-8-sig')
    # 輸出dataframe    
    return result


def tocsv(url):
    # 匯出csv檔
    collection(url).to_csv('FBcrawler.csv', encoding = 'utf-8-sig')


def catchLike():
    like = []
    time.sleep(3)
    soup = Soup(driver.page_source,"lxml")
    # 抓取按讚數
    for ii in soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'): #讀取每一篇文
        thumb = ii.find('span',class_="gpro0wi8 pcp91wgn")
        if(thumb == None):
            like.append('0')
        else:
            like.append(thumb.text)  
    # like資料處理
    for i in range(len(like)):
        if(like[i].find('\xa0萬') != -1):
            like[i] = int(float(like[i][:like[i].find('\xa0萬')])*10000)
        else:
            like[i] = int(like[i].replace(',',''))
    return like


def catchShare(length):
    share = []
    soup = Soup(driver.page_source,"lxml")
    # 抓取分享數
    for ii in soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'): #讀取每一篇文
        read = ii.find_all('span',class_="oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql a8c37x1j muag1w35 enqfppq2 jq4qci2q a3bd9o3v knj5qynh m9osqain")
        if(len(read) == 0):
            share.append('0次')
        elif(len(read) == 1):
            if('分享' in read[0].text):
                share.append(read[0].text)
            elif('留言' in read[0].text):
                share.append('0次')
        else:
            share.append(read[1].text)
    # share資料處理
    for i in range(len(share)):
        index = share[i].find('次')
        share[i] = int(share[i][:index].replace(',',''))
    return share[:length]


def catchCommentNums(length):
    comment_nums = []
    soup = Soup(driver.page_source,"lxml")
    # 抓取留言數
    for ii in soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'): #讀取每一篇文
        read = ii.find_all('span',class_="oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql a8c37x1j muag1w35 enqfppq2 jq4qci2q a3bd9o3v knj5qynh m9osqain")
        if(len(read) == 0):
            comment_nums.append('0則')
        elif(len(read) == 1):
            if('留言' in read[0].text):
                comment_nums.append(read[0].text)
            elif('分享' in read[0].text):
                comment_nums.append('0則')
        else:
            comment_nums.append(read[0].text)
    # comment_nums資料處理
    for i in range(len(comment_nums)):
        index = comment_nums[i].find('則')
        comment_nums[i] = int(comment_nums[i][:index].replace(',',''))
    return comment_nums[:length]


def catchPostTime(length):
    time = []
    soup = Soup(driver.page_source,"lxml")
    for ii in soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'): #讀取每一篇文
        postime = ii.find_all(class_ ='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw')
        # date =postime[0].select('span > span > b > b')
        date = postime[0].select('span') 
        for i in (range(len(date))):
            if date[i].text != '=': 
                time.append(date[i].text)
    return time[:length]


def catchArticleContent(length):
    driver.execute_script('window.scrollTo(0, 0);')
    time.sleep(2)
    article = driver.find_elements_by_class_name('du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0')
    # 按所有的"更多"
    for i in range(len(article)):
        button = article[i].find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.oo9gr5id.gpro0wi8.lrazzd5p')
        for j in range(len(button)):
            if('更多' in button[j].text):
                button[j].click()
    # 抓取內文 
    article_content = []
    soup = Soup(driver.page_source,"lxml")
    for ii in soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'): #讀取每一篇文
        post = ii.find_all(dir='auto',style="text-align: start;")
        content = ""
        for i in (range(len(post))) :
            icon = post[i].find_all('img')
            for ic in range(len(icon)):
                content += icon[ic]['alt']
            content +=  post[i].text
        article_content.append(content)
    return article_content[:length]


def catchLink(length):
    # 滑鼠觸碰日期產生網站連結
    weblink = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
    for i in range(len(weblink)):
        action = ActionChains(driver)
        weblink = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
        action.move_to_element(weblink[i]).perform()
    # 抓取文章連結
    article_link = []
    soup = Soup(driver.page_source,"lxml")
    for ii in soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'): #讀取每一篇文    
        link = ii.find(class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw")
        li= link.get('href')
        article_link.append(li)
    return article_link[:length]
    

def catchComment(length):
    # 滑到最上面
    driver.execute_script('window.scrollTo(0, 0);')
    # 點最相關
    relative_bottom = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l')
    print('click round 1')
    for i in range(len(relative_bottom)):
        if relative_bottom[i].text.find('最相關') != -1:
            try:
                relative_bottom[i].click()
                time.sleep(1)
            except:
                print('文章',i,'[最相關] click error')
            try:
                allcomment = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.j83agx80.p7hjln8o.kvgmc6g5.oi9244e8.oygrvhab.h676nmdw.pybr56ya.dflh9lhu.f10w8fjw.scb9dxdr.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l.bp9cbjyn.dwo3fsh8.btwxx1t3.pfnyh3mw.du4w35lb')
                time.sleep(1)
                allcomment[2].click()
            except:
                print('文章',i,'[所有留言] click error')

    # 滑到最上面
    driver.execute_script('window.scrollTo(0, 0);')
    # 點擊查看更多留言 檢視另 則留言 則回覆 (展開所有回復)
    morecomment = driver.find_elements_by_class_name('oi732d6d.ik7dh3pa.d2edcug0.qv66sw1b.c1et5uql.a8c37x1j.muag1w35.enqfppq2.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
    print('click round 2')
    for i in range(len(morecomment)):
        try:
            m = morecomment[i].text
            if m.find('檢視另')!=-1:
                try:
                    morecomment[i].click()
                except:
                    print('文章',i,'[檢視另] click error')
            if m.find('則回覆')!=-1:
                try:
                    morecomment[i].click()
                except:
                    print('文章',i,'[則回覆] click error')
            if m.find('查看更多留言')!=-1:
                try:
                    morecomment[i].click()
                except:
                    print('文章',i,'[查看更多留言] click error')
            time.sleep(1)
        except:
            continue

    # 滑到最上面
    driver.execute_script('window.scrollTo(0, 0);')
    # 點剩下的回覆
    morecomment = driver.find_elements_by_class_name('oi732d6d.ik7dh3pa.d2edcug0.qv66sw1b.c1et5uql.a8c37x1j.muag1w35.enqfppq2.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
    print('click round 3')
    for i in range(len(morecomment)):
        try:
            m2 = morecomment[i].text
            if m2.find('則回覆') != -1:
                try:
                    morecomment[i].click()
                except:
                    print('文章',i,'[則回覆] click error')
            time.sleep(1)
        except:
            continue

    # 滑到最上面
    driver.execute_script('window.scrollTo(0, 0);')
    # 點擊更多(留言長)
    print('click more')
    more_button = driver.find_elements_by_css_selector("div[class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p'][role='button'][tabindex='0']")
    for i in range(len(more_button)):
        try:
            more_button[i].click()
        except:
            print('文章',i,'[更多] click error')

    # 抓取留言內容
    str = ' '
    author = []
    comment = []
    comment2 = driver.find_elements_by_class_name('tw6a2znq.sj5x9vvc.d1544ag0.cxgpxx05') 
    for k in range(len(comment2)): 
        string = comment2[k].text
        stringlist=string.split('\n')
        author.append(stringlist[0]) # 作者list
        del (stringlist[0])
        if(len(stringlist) == 0):
            comment.append('貼圖')
        else:
            comment.append(str.join(stringlist)) # 留言list
        stringlist=[]

    # 滑到最上面
    driver.execute_script('window.scrollTo(0, 0);')
    # 有無留言
    comment_data = []
    art_num = []
    count = -1
    num = 0
    for ii in driver.find_elements_by_class_name('du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0'):
        count += 1
        article = ii.find_elements_by_class_name('tw6a2znq.sj5x9vvc.d1544ag0.cxgpxx05')
        if(len(article) == 0):
            comment_data.append('none')
            art_num.append(count)         
            author.insert (num,'no author') # append none
            comment.insert (num,'no comment')
            num += 1
        else:
            for i in range(len(article)):
                comment_data.append('exist')
                art_num.append(count)
                num += 1

    comment_dataset={"article_num" : art_num,
                    "comment_author" : author, 
                    "comment_content" : comment}
    dataset=DataFrame(comment_dataset)  

    # 依照文章分類
    df=dict(list(dataset.groupby("article_num")))
    listauthor=[]
    for i in range(len(df)):  #作者轉為list
        a = list(df[i]["comment_author"])
        listauthor.append(a)
    listcomment=[]
    for i in range(len(df)):  #留言內容轉為list
        c = list(df[i]["comment_content"])
        listcomment.append(c)

    # 變成字典
    combinedlist=[]
    for i in range(len(listauthor)): 
        combined = {}
        for j in range(len(listauthor[i])):
            combined[listauthor[i][j]]= listcomment[i][j]
        combinedlist.append(combined)
    
    return combinedlist[:length]



   

#collection('https://www.facebook.com/InstitutionalResearchTaiwan/')
#tocsv( 'https://www.facebook.com/InstitutionalResearchTaiwan/')
collection('https://www.facebook.com/USTARTFans/')
tocsv( 'https://www.facebook.com/USTARTFans/')

