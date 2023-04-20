from libs.OpenHtml import *
import  pandas  as pd
import json
import sys,re
class J_mgtv:
    def __init__(self):
        pass
    def get(self,url):#
        #电视剧
        try:
            html=open_html(url)
            html = lxml.html.fromstring(html)
            ptitle=html.xpath('//div[@data-emergence="hidden"]//a/@title')
            phref=html.xpath('//div[@data-emergence="hidden"]//a/@href')
            p1=[]
            for i in range(len(ptitle)):
                pm=ptitle[i]
                if pm.find('《')!=-1:continue
                if pm.find('花絮')!=-1:continue
                if pm.find('预告')!=-1:continue
                if pm.find('回顾')!=-1:continue
                if pm.find('看点')!=-1:continue
                pm1=re.compile(r'"*(.*?) 第').findall(pm)
                pm2=re.compile(r'"*(第.*?集)').findall(pm)
                p1.append([{'分类':'电视剧',
                  '片名':pm1[0],
                  '剧集':pm2[0],
                  'url':f'https:{phref[i]}'}])
        except:
            p1=[]
        if bool(p1):
           return pd.DataFrame(p1) 
        #电影
        try:
            html=open_html(url)
            html = lxml.html.fromstring(html)
            ptitle=html.xpath('//div[@class="movie clearfix m-aside-header-ie"]//a/@title')
            phref=html.xpath('//div[@class="movie clearfix m-aside-header-ie"]//a/@href')
            p1=[{'分类':'电影',
                  '片名':ptitle[0],
                  '剧集':ptitle[0],
                  'url':f'https://www.mgtv.com{phref[0]}'}]
        except:
            p1=[]    
        return pd.DataFrame(p1)
    def soso(self,name):#按影名搜
        try:
            url=f"https://so.mgtv.com/so?k={name}&lastp=v_play"
            html=open_html(url)
            html = lxml.html.fromstring(html)
                        
        except:
            p1=[]    
#print(J_mgtv().soso('东八区的先生们'))    
#print(J_mgtv().get('https://www.mgtv.com/b/450993/18469712.html?fpa=1261&fpos=&lastp=ch_tv&cpid=4'))
