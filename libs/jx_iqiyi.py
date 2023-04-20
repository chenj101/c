import json
import sys,re
import  pandas  as pd
#sys.path.append('../libs')
from libs.OpenHtml import *
class J_iqiyi:
    def __init__(self):
        pass
    def ie_jj(self,url):#网页播放页面,取分集地址
        html=open_html(url)
        html = lxml.html.fromstring(html)
        #data-block-name="头部信息"
        name=html.xpath('//h1[@class="album-head-title"]/a/@title')[0]#片名
        #<!-- 数字列表 -->
        va_url=html.xpath('//li[@class="album_item"]/a/@href')
        pname=html.xpath('//li[@class="album_item"]/a/@title')
        p1=[]
        for i in pname:
           if i.isdigit():
               p2={'分类':'电视剧',
                   '片名':name,
                   '剧集':f'第{i:0>3}集',
                   'url':f'https:{va_url[int(i)-1]}'}
               p1.append(p2)
               
        return pd.DataFrame(p1)
    def dianying(self,url):#电影分类页面
        html=open_html(url)
        html = lxml.html.fromstring(html) 
        va_url=html.xpath('//div[@class="title-wrap"]//a/@href')
        pname=html.xpath('//div[@class="title-wrap"]//a/@title')
        p1=[{'分类':'电影'
             ,'片名':pname[i]
             ,'剧集':pname[i]
             ,'url':f'https:{va_url[i]}'} for i in range(len(pname))]
        return pd.DataFrame(p1)
    def get(self,url):#
        html=open_html(url)
        html=re.compile(r'"itemListElement":(.*?}\])}').findall(html)
        pname=[]
        if bool(html):#APP电视剧播放页面,取地址转网页播放页面
            html=html[0]
            html=json.loads(html)
            url=html[2]['url']
            name=html[2]['name']
            name1=html[1]['name']
            n=url.find(':')
            url=f'https{url[n:]}'#
            if name1=='电影': 
               pname=[{'分类':'电影','片名':name,'剧集':name,'url':url}]
               pname=pd.DataFrame(pname)
            else: #电视剧   
               pname=self.ie_jj(url)
        if url.find('https://www.iqiyi.com/a_')!=-1:#电视剧网页播放页面
               pname=self.ie_jj(url)
        if url.find('https://www.iqiyi.com/dianying')!=-1:#电影分类页面
               pname=self.dianying(url)       
        return pname
    def soso(self,name):#按影名搜
        try:
            url=f"https://so.iqiyi.com/so/q_{name}?source=hot"
            html=open_html(url)
            html = lxml.html.fromstring(html)
            item_type=html.xpath('//h3[@class="qy-search-result-tit title-score"]//span[@class="item-type"]//text()')
            ptitle=html.xpath('//h3[@class="qy-search-result-tit title-score"]//a/@title')
            phref=html.xpath('//h3[@class="qy-search-result-tit title-score"]//a/@href')
            p1=[]
            if item_type[0]=='电影':
                p1=[[ptitle[0],f'https:{phref[0]}']]
            
            if item_type[0]=='电视剧':
                p1=self.get(f'https:{phref[0]}')
        except:
            p1=[]    
        return p1
#print(eval("J_iqiyi().soso('苍兰诀')"))
#print(J_iqiyi().get('https://www.iqiyi.com/dianying/?vfrm=pcw_dianying&vfrmblk=712211_topNav&vfrmrst=712211_channel_dianying'))
#https://so.iqiyi.com/so/q_苍兰诀?source=hot
