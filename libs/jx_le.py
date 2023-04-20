#播放页无信息，在搜索页取
from libs.OpenHtml import *
import  pandas  as pd
import json
import sys,re
class J_le:
    def __init__(self):
        pass
    def get(self,url):
        if url.find('https://www.le.com/ptv/vplay')==-1:#非播放页,确定播放页url
            html=open_html(url)
            html=html.replace('"',"\'")
            html = lxml.html.fromstring(html)
            pinfo=html.xpath('//dt[@class="d_tit"]/a/@href')[0]
            url=f'https:{pinfo}'
            
        html=open_html(url)
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
           return pd.DataFrame([{'分类':'电影',
                                '片名':title,
                                '剧集':title,
                                'url':f"http://www.le.com/ptv/vplay/{vid}.html#vid={vid}"}])
        
    def soso(self,name):#按影名搜
        url=f"http://so.le.com/s?wd={name}&from=suggest&ref=click"
        html=open_html(url)
        html = lxml.html.fromstring(html)
        #电视剧
        try:
            data_info=html.xpath('//div[@class="So-detail Tv-so"]//@data-info')
            data_info=data_info[0]
            data_info=data_info.replace('{','{"')
            data_info=data_info.replace('\',','","')
            data_info=data_info.replace(':\'','":"')
            data_info=data_info.replace('\'}','"}')
            data_info=json.loads(data_info)
            pname=data_info['keyWord']
            n=pname.find(' ')
            pname=pname[:n]
            jj=data_info['vidEpisode'].split(",")
            p1=[]
            for cc in jj:
                n=cc.find('-')
                p1.append([{'分类':'电视剧',
                            '片名':pname,
                            '剧集':f"第{cc[:n]:0>3}集",
                            'url':f"http://www.le.com/ptv/vplay/{cc[n+1:]}.html#vid={cc[n+1:]}"}])
        except:
            p1=[]
        if bool(p1):
           return p1
        #电影
        try:
            ptitle=html.xpath('//dl[@class="video-info"]//a/@title')
            phref=html.xpath('//dl[@class="video-info"]//a/@href')
            p1=[{'分类':'电影',
                '片名':ptitle[0],
                '剧集':ptitle[0],      
                'url':f"https:{phref[0]}"}]
        except:
            p1=[]
        return  pd.DataFrame(p1)
#print(J_le().soso('丁大命'))
# 播放页   
#print(J_le().get('https://www.le.com/ptv/vplay/25600437.html'))
# 非播放页
#print(J_le().get('https://www.le.com/tv/93327.html'))    

