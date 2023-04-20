from OpenHtml import *
#import lxml.html
import json
import sys,re
class J_wasu:
    def __init__(self):
        pass
    def get(self,url):#
        html=open_html(url)
        html = lxml.html.fromstring(html)
        try:
            #电视剧       
            pid=html.xpath('//div[@class="play_items2"]//a/text()')
            va_url=html.xpath('//div[@class="play_items2"]//a/@href')
            pname=html.xpath('//div[@class="play_items2"]//li/@title')
            pva=[]
            for i in range(len(pname)):
                pva.append((f'第{pid[i]:0>3}集 {pname[i]}',va_url[i]))
        except:
            pva=[]
        
        if bool(pva):
           return  pva
        try:
            #电影
            va_url=html.xpath('//div[@class="ws_body tab_box play_group"]//p/a/@href')
            pname=html.xpath('//div[@class="ws_body tab_box play_group"]//p/a/@title')
            if len(pname)==0:
                va_url=html.xpath('//div[@class="play_information_t"]//a/@href')
                pname=html.xpath('//div[@class="play_information_t"]//img/@alt')

            pva=[]
            for i in range(len(pname)):
                pva.append((pname[i],f'https://www.wasu.cn{va_url[i]}'))                
        except:
            pva=[]    
        return  pva
    
#print(eval("J_iqiyi().soso('苍兰诀')"))
#print(J_wasu().get('https://www.wasu.cn/Play/show/id/10262561'))
#https://so.iqiyi.com/so/q_苍兰诀?source=hot
