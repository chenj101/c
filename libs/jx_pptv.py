#播放页无信息，在搜索页取
from libs.OpenHtml import *
import  pandas  as pd
import json
import sys,re
class J_pptv:
    def __init__(self):
        pass
    def get(self,url):
        try:
            html=open_html(url)
            html = lxml.html.fromstring(html)
            ptitle=html.xpath('//head/title/text()')
            n=ptitle[0].find(r'_')
            ptitle=ptitle[0][:n]
            pp=self.soso(ptitle)
        except:
            pp=[]
        return  pp
    def soso(self,name):#按影名搜
        url=f"http://sou.pptv.com/s_video?kw={name}&context=default" 
        html=open_html(url)
        html = lxml.html.fromstring(html)
        fl=html.xpath('//span[@class="n-label"]/text()')[0]
        if fl=='电视剧':
            ptitle=html.xpath('//div[@class="episodes-list"]//a/@title')
            phref=html.xpath('//div[@class="episodes-list"]//a/@href')
            p1=[]
            for i in range(len(ptitle)):
                pm=ptitle[i]
                pm1=re.compile(r'"*(.*?)第').findall(pm)
                pm2=re.compile(r'"*(第.*?集)').findall(pm)
                p1.append([{'分类':'电视剧','片名':pm1[0],'剧集':pm2[0],'url':f'https:{phref[i]}'}])
            return pd.DataFrame(p1)
        if fl=='电影':
            ptitle=html.xpath('//div[@class="positive-box clearfix"]/a/@title')
            phref=html.xpath('//div[@class="positive-box clearfix"]/a/@href')
            p1=[{'分类':'电影',
                  '片名':ptitle[0],
                  '剧集':ptitle[0],
                  'url':f'https://www.mgtv.com{phref[0]}'}]
            return pd.DataFrame(p1)
#print(J_pptv().soso('长津湖'))     
#print(J_pptv().get('https://v.pptv.com/show/DSgTkflfzw1w7lY.html'))

