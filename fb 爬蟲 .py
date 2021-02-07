
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

# 切換頁面
spec_url = 'https://www.facebook.com/moea.gov.tw'
driver.get(spec_url)






### ************************手動 點除封鎖 通知*****************
# 
#           滑動次數 #網路慢可加長time sleep加載時間-------

for i in range(5):
    js = 'window.scrollTo(0, document.body.scrollHeight);'
    driver.execute_script(js)
    time.sleep(5)

#          移至最上面 讓畫面可以被點擊--------
weblink = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
action = ActionChains(driver)
action.move_to_element(weblink[0]).perform()

#          定位文章中"更多..."按鈕--------
more_button = driver.find_elements_by_css_selector("div[class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p'][role='button'][tabindex='0']")

for i in range(0,len(more_button)):
    more_button[i].click()
    #time.sleep(1)
    
#          滑鼠觸碰日期產生網站連結  *---------------
weblink = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
le = len(weblink)
le = range(0,le)
for i in le:
    action = ActionChains(driver)
    weblink = driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
    action.move_to_element(weblink[i]).perform()




###########
#           分解網站
soup = Soup(driver.page_source,"lxml")
article_time = []
article_content = []
like = []
share = []
article_link = []


#    控制迴圈數量
control_num = 0

#    文章架構
article_frame = soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')

#藉由文章架構將一篇一篇文章抓取出來
for ii in soup.find_all(class_ ='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'): #讀取每一篇文
    # 按讚數
    thumb = ii.find('span',class_="gpro0wi8 pcp91wgn")
    if(thumb == None):
        like.append('0')
    else:
        like.append(thumb.text)


    # 分享數
    read = ii.find('span',class_="oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql a8c37x1j muag1w35 enqfppq2 jq4qci2q a3bd9o3v knj5qynh m9osqain")
    if(read == None):
        share.append('0次')
    elif('分享' in read.text):
        share.append(read.text)
    else:
        share.append(ii.find_all('span',class_="oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql a8c37x1j muag1w35 enqfppq2 jq4qci2q a3bd9o3v knj5qynh m9osqain")[1].text) 

    #文章內容
    post = ii.find_all(dir='auto',style="text-align: start;")
    le = len(post)
    content =""
    for i in (range(0,le )) :
        icon = post[i].find_all('img')
        for ic in range(0,len(icon)):
            content = content + icon[ic]['alt']
        content = content + post[i].text
    article_content.append(content)
    #article_content為文章內容


    #文章時間.
    postime = ii.find_all(class_ ='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw')
    date =postime[0].select('span > span > b ')
    le = len(date)
    for i in (range(0,le )) :
        article_time.append(date[i].text.strip('='))
        
    
        
    #文章連結
    link = ii.find(class_="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw")
    li= link.get('href')
    article_link.append(li)
    control_num = control_num + 1
    if control_num == len(more_button):
        break
    #article_time為文章時間
    

result={"article_content" : article_content , 
        "article_time" : article_time ,
        "numbers of like" : like,
        "numbers of share" : share,
        "article_link" : article_link,
        }#將列表a，b轉換成字典


article_data=DataFrame(result)
article_data
article_data.to_csv('88.csv',encoding = 'utf-8-sig')




# share資料處理
for i in range(len(share)):
    index = share[i].find('次')
    share[i] = int(share[i][:index])



len(article_content)
len(article_time)
len(like)
len(share)
len(article_link)



##點所有留言-----------------------------------------------------------------------------------------------------------

#    滑到最上面
driver.execute_script('window.scrollTo(0, 0);')
#    點最相關
relative_bottom=driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l')
for i in range(len(relative_bottom)):
    print(relative_bottom[i].text)
    b=relative_bottom[i].text
    if b.find('最相關')!=-1:
        relative_bottom[i].click()
        #   點所有留言
        time.sleep(2)
        allcomment=driver.find_elements_by_class_name('oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.j83agx80.p7hjln8o.kvgmc6g5.oi9244e8.oygrvhab.h676nmdw.pybr56ya.dflh9lhu.f10w8fjw.scb9dxdr.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l.bp9cbjyn.dwo3fsh8.btwxx1t3.pfnyh3mw.du4w35lb')
        time.sleep(2)
        allcomment[2].click()
        

#滑到最上面
driver.execute_script('window.scrollTo(0, 0);')
#點擊查看更多留言 檢視另 則留言 則回覆 (展開所有回復)
morecomment=driver.find_elements_by_class_name('oi732d6d.ik7dh3pa.d2edcug0.qv66sw1b.c1et5uql.a8c37x1j.muag1w35.enqfppq2.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
len(morecomment)
for i in range(len(morecomment)):
    print(morecomment[i].text)
    m=morecomment[i].text
    if m.find('檢視另')!=-1:
        morecomment[i].click()
    if m.find('則回覆')!=-1:
        morecomment[i].click()
    if m.find('查看更多留言')!=-1:
        morecomment[i].click()
    time.sleep(1)

driver.execute_script('window.scrollTo(0, 0);')

morecomment=driver.find_elements_by_class_name('oi732d6d.ik7dh3pa.d2edcug0.qv66sw1b.c1et5uql.a8c37x1j.muag1w35.enqfppq2.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain')
for i in range(len(morecomment)):
    print(morecomment[i].text)
    m2=morecomment[i].text
    if m2.find('則回覆')!=-1:
        morecomment[i].click()
    time.sleep(1)

#點擊更多(留言長) 錯
driver.execute_script('window.scrollTo(0, 0);')

more_button = driver.find_elements_by_css_selector("div[class = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p'][role='button'][tabindex='0']")

for i in range(0,len(more_button)):
    more_button[i].click()






#留言框架 stjgntxs ni8dbmo4 g3eujd1d 
comment2=driver.find_elements_by_class_name('tw6a2znq.sj5x9vvc.d1544ag0.cxgpxx05') 
author=[]
comment=[]
str=' '

##區分作者及留言
for k in range(len(comment2)): 
    
    string = comment2[k].text
    stringlist=string.split('\n')
    print('author=',stringlist[0])
    aut = stringlist[0]
    author.append(aut) ##作者list
    del(stringlist[0])
    print(stringlist)
    if(len(stringlist)==0):
        comment.append('貼圖')
    else:
        print('comment=',str.join(stringlist))
        com=str.join(stringlist)
        comment.append(com) #留言list
    stringlist=[]
comment





#------------------------------------------------
##每篇文章有無留言
driver.execute_script('window.scrollTo(0, 0);')

comment_data = []##有無留言
art_num=[]
count=-1
num=0
for ii in driver.find_elements_by_class_name('du4w35lb.k4urcfbm.l9j0dhe7.sjgh65i0'):
      
    count=count+1
    article = ii.find_elements_by_class_name('tw6a2znq.sj5x9vvc.d1544ag0.cxgpxx05')
    if(len(article)==0 ):
        comment_data.append('none')
        art_num.append(count)
        #print('no comment')
        #print(count)
        
        author.insert(num,'no author')##append none
        comment.insert(num,'no comment')
        num=num+1
       
   
    else:
        for i in range(len(article)):
            comment_data.append('exist')
            art_num.append(count)
            #print('yes')
            #print(count)
            num=num+1

comment_dataset={"article_num" : art_num,
         "comment_author" : author, 
         "comment_content" : comment}

dataset=DataFrame(comment_dataset)
len(art_num)
len(author)
len(comment)


##依照文章分類
df=dict(list(dataset.groupby("article_num")))

listauthor=[]
for i in range(len(df)):  ##作者轉為list
    a=list(df[i]["comment_author"])
    listauthor.append(a)

listcomment=[]
for i in range(len(df)):  ##留言內容轉為list
    c=list(df[i]["comment_content"])
    listcomment.append(c)


c={"comment_author":listauthor,
    "comment_content":listcomment}

c=DataFrame(c)
c

##變成字典
combinedlist=[]
for i in range(len(listauthor)): 
    combined = {}
    for j in range(len(listauthor[i])):
        combined[listauthor[i][j]]= listcomment[i][j]
    combinedlist.append(combined)


comment_dataset2={ "comment" : combinedlist}
comment_dataset2=DataFrame(comment_dataset2)
comment_dataset2








    

