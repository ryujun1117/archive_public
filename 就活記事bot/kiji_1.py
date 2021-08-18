import json
from requests_oauthlib import OAuth1Session

CONSUMER_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
ACCESS_TOKEN_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
url = 'https://api.twitter.com/1.1/statuses/update.json'

#就活記事！
import requests
from bs4 import BeautifulSoup
#import slackweb
import datetime

dt_date = datetime.datetime.now()
Y = dt_date.year
M = dt_date.month
D = dt_date.day -1
time= str(Y)+"/"+str(M)+"/"+str(D)

date_list = []
title_list = []
url_list = []
name_list = []
count = []

kiji = {
    "onecareer":"https://www.onecareer.jp/articles",
    "nhk_syukatu":"https://www3.nhk.or.jp/news/special/news_seminar/syukatsu/",
    "nikkei":"https://r.nikkei.com/topics/topic_DF_TB_17090316",
    "dentsu-ho":"https://dentsu-ho.com/latest_articles",
    "ainow":"https://ainow.ai/new/"
}

def onecareer():
    name_list.append("ONECAREER")
    r = requests.get(kiji["onecareer"])
    soup = BeautifulSoup(r.content, "html.parser")
    url_under = soup.select("[class='is-pickup v2-article-list__title'] a" )
    title = soup.select("[class='is-pickup v2-article-list__title']")
    date = soup.select("[class = 'is-pickup v2-article-list__publish-at']")
    for i in range(len(date)):
        url = "https://www.onecareer.jp" + url_under[i].get('href')
        d = date[i].getText()
        d = d.replace("\n", "")
        date_list.append(d)
        t = title[i].getText()
        t = t.replace('\n', '')
        title_list.append(t)
        url_list.append(url)

        
def nhk():
    name_list.append("NHK_就活")
    r = requests.get(kiji["nhk_syukatu"])
    soup = BeautifulSoup(r.content, "html.parser")

    block = soup.select("dd")
    for i in range(len(block)):
        elem = block[i]
        #投稿日
        date = elem.select(".date")
        d = date[0].getText()
        d = d.replace('\n', '')
        d = d.replace('n', '')
        d = d.replace('t', '')
        d = d.replace('\t', '')
        d = d.replace('年', '/')
        d = d.replace('月', '/')
        d = d.replace('日', '')
        date_list.append(d)

        #記事名
        title = elem.select(".name")
        title_list.append(title[0].getText())

        #リンク
        under_link = elem.select("a")
        link = "https://www3.nhk.or.jp"+under_link[0].get("href")
        url_list.append(link)
        
        
def dentu():
    name_list.append("電通報")
    r = requests.get(kiji["dentsu-ho"])
    soup = BeautifulSoup(r.content, "html.parser")
    article = soup.select(".people-list-item")
    for i in range(len(article)):
        #date
        date = article[i].select(".date")
        date = date[0].getText()
        date_list.append(date)
        #title
        title = article[i].select(".article-title")
        title = title[0].getText()
        title_list.append(title)
        #url
        url = article[i].select(".article-title .wfjm")
        url_under = url[0].get("href")
        url = "https://dentsu-ho.com/" + url_under
        url_list.append(url)
        
def ainow():
    name_list.append("AI-NOW")
    r = requests.get(kiji["ainow"])
    soup = BeautifulSoup(r.content, "html.parser")
    article = soup.select(".article_list")
    article_1 = article[0].select(".article")
    for i in range(len(article_1)):
            #date
            date_next = article_1[i].select(".article_date")
            date = date_next[0].getText()
            date = date.replace('.', '/')
            date_list.append(date)

            #title
            title = article_1[i].select(".article_title h2" )
            title = title[0].getText()
            title_list.append(title)

            #url
            url = article_1[i].select(".article_link")
            url = url[0].get("href")
            url_list.append(url)
        
def push():
    for i in range(len(date_list)):
        if date_list[i] == time:
            #スラックで送信する処理
            print(date_list[i])
            print(title_list[i])
            print(url_list[i])
            set_date.append(date_list[i])
            set_title.append(title_list[i])
            set_url.append(url_list[i])
            count.append("1")
            
        else:
            continue
        
def post():
    #send_message
    #text_1_5 ="【"+name_list[0]+"】"
    #slack.notify(text = text_1_5)
    for i in range(len(set_date)):
        text_2 = "更新日："+set_date[i]+"\n"
        title = set_title[i] +"\n"+set_url[i] 
        text_all = text_2 + title +"\n"+"#就活 #22卒"
        params = {'status': text_all}
        twitter.post(url, params = params)

        
    #text_3 = "-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-"
    #slack.notify(text = text_3)

      
#text_1 = "【"+time+"】"+"\n"+"最新の記事だよ" + ":meow-party:" +"\n" 

#slack.notify(text = text_1)

date_list = []
title_list = []
url_list = []
name_list = []
set_date = []
set_title = []
set_url = []
count = []

nhk()
push()
if len(count) != 0:
    post()


date_list = []
title_list = []
url_list = []
name_list = []
set_date = []
set_title = []
set_url = []
count = []

dentu()
push()
if len(count) != 0:
    post()

date_list = []
title_list = []
url_list = []
name_list = []
set_date = []
set_title = []
set_url = []
count = []

ainow()
push()
if len(count) != 0:
    post()

date_list = []
title_list = []
url_list = []
name_list = []
set_date = []
set_title = []
set_url = []
count = []

onecareer()
push()
if len(count) != 0:
    post()


print("success!")
