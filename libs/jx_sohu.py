#播放页无信息，在搜索页取
from OpenHtml import *
import  pandas  as pd
import json
import sys,re
class J_sohu:
    def __init__(self):
        pass
    def get(self,url):
        html=open_html(url)
        print(html)
        html=html.replace('"',"\'")
        html = lxml.html.fromstring(html)
        pinfo=html.xpath('//script[@type="text/javascript"]/text()')[0]
        if not bool(pinfo):
            return  pp
        sname=re.compile(r'wd :(.*?),').findall(pinfo)#搜索页片名
        if bool(sname):
            title=sname[0].replace("\'","")
            return  self.soso(title)
        vid=re.compile(r'vid:(.*?),').findall(pinfo)[0].strip()#播放页
        #burl=re.compile(r'url:(.*?)},').findall(pinfo)#播放页
        totalcount=re.compile(r'totalcount:(.*?),').findall(pinfo)[0]#播放页
        totalcount=totalcount.replace("\'","")
        title=re.compile(r"title:(.*?),").findall(pinfo)[0]
        title=title.replace("\'","")
        if int(totalcount)!=1:#电视剧
            return  self.soso(title)
        else:#电影
           return [[title,f"http://www.le.com/ptv/vplay/{vid}.html#vid={vid}"]]
        
    def soso(self,name):#按影名搜
        url=f"http://so.tv.sohu.com/mts?wd={name}"
        html=open_html(url)
        html = lxml.html.fromstring(html)
        #电视剧
        try:
            href=html.xpath('//div[@class="series cfix"]//a/@href')
            title=html.xpath('//div[@class="series cfix"]//a/@title')
            p1=[[title[i],f"http:{href[i]}"] for i in range(len(title))]
        except:
            p1=[]
        if bool(p1):
           return p1
        #电影
        try:
            ptitle=html.xpath('//dl[@class="video-info"]//a/@title')
            phref=html.xpath('//dl[@class="video-info"]//a/@href')
            p1=[[ptitle[0],f"https:{phref[0]}"]]
        except:
            p1=[]
        return p1
#print(J_sohu().soso('从爱情到幸福'))     
#print(J_sohu().get('http://tv.sohu.com/s2022/dsjcaqdxf/'))
print(J_sohu().get('https://tv.sohu.com/v/MjAyMjA2MTYvbjYwMTE5MDc4NC5zaHRtbA==.html'))    

