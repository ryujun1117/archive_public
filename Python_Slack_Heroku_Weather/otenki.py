#yahoo天気から次の日のお天気をとって来てくれるぼっと
import requests
from bs4 import BeautifulSoup
r = requests.get("https://weather.yahoo.co.jp/weather/jp/1b/1400.html")
soup = BeautifulSoup(r.content, "html.parser")
first = soup.select("[class ='forecastCity']")
sapporo_date = soup.select("[class = 'date']")
sapporo_pict = soup.select("[class = 'pict']")
sapporo_high = soup.select("[class = 'high']")
sapporo_low = soup.select("[class = 'low']")
sapporo_time = soup.select("[class = 'time']")
sapporo_precip = soup.select("[class = 'precip']")
for i in sapporo_date:
    sapporo_date = i.getText()
for i in sapporo_pict:
    sapporo_pict = i.getText()
for i in sapporo_high:
    sapporo_high = i.getText()
for i in sapporo_low:
    sapporo_low = i.getText()
for i in sapporo_time:
    sapporo_time = i.getText()
for i in sapporo_precip:
    sapporo_precip = i.getText()
s = sapporo_precip
l = s.split("\n")
del l[0]
del l[-1]
line = [":sunny:", ":mostly_sunny:", ":partly_sunny:", ":barely_sunny:",":cloud:",":snow_cloud:"]
list =[]
k=1
for k in range(4):
    if l[k] == "0％":
        emoji = line[0]
    elif l[k] == "10％":
        emoji = line[1]
    elif l[k] == "20％":
        emoji = line[2]
    elif l[k] == "30％":
        emoji = line[3]
    elif l[k] == "40％" or l[1] =="50％" or l[1] =="60％":
        emoji = line[4]
    else:
        emoji = line[5]
    list.append(emoji)

import slackweb
slack = slackweb.Slack(url = "https://hooks.slack.com/services/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")
#slack.notify(text = "test", channel="@SETO", username="coffee")
message_2 = "時間 | "+"降水率"+"\n"+"0:00-："+l[1]+" "+list[0]+"\n"+"6:00-："+l[2]+" "+list[1]+"\n"+"12:00-："+l[3]+" "+list[2]+"\n"+"18:00-："+l[4]+" "+list[3]
message = sapporo_date+ " / " +sapporo_pict+" (札幌)"+"\n"+":thermometer:"+ "max："+ sapporo_high+" / "+"min："+ sapporo_low+"\n\n"+message_2

slack.notify(text = "おつかれさま～\nさむいね～")
slack.notify(text = "明日の天気をお知らせするよぅ:party-blob:")
slack.notify(text = message)
