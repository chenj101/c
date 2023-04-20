#音乐接口
#url = http://www.kuwo.cn/api/v1/www/music/playUrl?mid=149121488&type=convert_url3
#数据接口
from PyQt5.QtCore import *
#from PyQt5.QtWidgets import *
#from PyQt5.QtGui import *
import httpx
#import hashlib
#import random
import lxml.html
import os,sys
import re
import time
import json
class jx_kuwo(QThread):#mp3下载
    finished = pyqtSignal(str)
    def __init__(self,*url):
        QThread.__init__(self)
        self.url=url[0]
        print(self.url)
    def run(self):
        def mp3_down(name1,name2,rid):
            finame=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',name1)#删除文件名特殊字符
            if not os.path.exists(f'{os.getcwd()}/mp3/{finame}'):
               os.makedirs(f'{os.getcwd()}/mp3/{finame}')
            headers = get_header()   
            try:
                self.finished.emit(f'正在下载《{finame}》_{name2}.....')
                save_file = f"{os.getcwd()}/mp3/{finame}/{name2}.mp3"
                dataurl =f"http://www.kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=convert_url3"
                text =httpx.get(dataurl, headers=headers).text
                text=json.loads(text)
                rr=httpx.get(text['data']['url'])
                rr.raise_for_status()
                with open(save_file, 'wb') as (f):
                    f.write(rr.content)
            except:
                 pass    
            self.finished.emit(f'《{finame}》下载完成.....')
        def get_header():
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63",
                "Cookie":"_ga=GA1.2.1771259403.1676946491; _gid=GA1.2.1267099804.1677116034; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1676946491,1677116034; kw_token=Z8BGWFAOXHP; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1677117521",
                #"Referer": "http://kuwo.cn/singer_detail/336",
                "Referer": "http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6",
                "csrf": "Z8BGWFAOXHP",
               }
            return  headers
        '''
        #这只能下载第一页
        def kuwo_gs(name1):#歌手
            headers = get_header()
            n=self.url.rfind(r'/')
            gsid=self.url[n+1:]
            url=f'http://kuwo.cn/api/www/artist/artistMusic?artistid={gsid}&pn=1&rn=20&httpsStatus=1&reqId=b7ef9a30-b31d-11ed-9133-33332d3eeee2'
            text =httpx.get(url, headers=headers).text
            text=json.loads(text)
            for m in text["data"]["list"]:
                #name1=m["artist"]
                name2=m['name']
                rid=m['rid']
                mp3_down(name1,name2,rid)
        '''        
        def kuwo_gs(name1):#歌手,歌名
            headers = get_header()
            url = f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={name1}&pn=1&rn=1000&reqId=c06e0e50-fe7c-11eb-9998-47e7e13a7206'
            text =httpx.get(url, headers=headers).text
            #print(text)
            text=json.loads(text)
            for m in text["data"]["list"]:
                name2=m['name']
                rid=m['rid']
                mp3_down(name1,name2,rid)
                
        self.finished.emit(f'正在解析{self.url}，请稍候....')
        headers = get_header()
        text = httpx.get(self.url, headers=headers).text
        text = lxml.html.fromstring(text)
    
        if self.url.find('kuwo.cn/singer_detail')!=-1:#歌手,歌名
            name=text.xpath('//span[@class="name"]/text()')[0]
            kuwo_gs(name)
        
        if self.url.find('www.kuwo.cn/playlist_detail')!=-1:#歌单
            name=text.xpath('//p[@class="song_name"]/text()')
            mp3_name=text.xpath('//div[@class="song_name flex_c"]/a/@title')
            mp3_href=text.xpath('//div[@class="song_name flex_c"]/a/@href')
            for i in range(len(mp3_name)): 
                mp3_down(name[0],mp3_name[i],mp3_href[i][13:])
            
        if self.url.find('www.kuwo.cn/play_detail')!=-1:#单曲播放页
           n=self.url.rfind(r"/")
           mp3_id=self.url[n+1:]
           name=text.xpath('//span[@class="tip album_name"]//text()')
           mp3_down(name[0],name[0],mp3_id)

       
            

#print(kuwo_gs('最伟大的作品'))
#print(jx_kuwo().run('http://www.kuwo.cn/singer_detail/683'))
