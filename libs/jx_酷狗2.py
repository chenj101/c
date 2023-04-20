#数据接口
#import requests
from PyQt5.QtCore import *
import httpx
import lxml.html
import os,sys
import re
import time
import json
class jx_kugou(QThread):#mp3下载
    finished = pyqtSignal(str)
    def __init__(self,*url):
        QThread.__init__(self)
        self.url=url[0]
        print(self.url)
    def run(self):
        def get_header():
            headers = {"Referer":"https://www.kugou.com/",
                       "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.192.400 QQBrowser/11.5.5250.400"
                       }
            return  headers
        def gs_list(url):#歌手
            headers = get_header()
            text = httpx.get(url, headers=headers).text
            text = lxml.html.fromstring(text)
            mp3_href=text.xpath('//ul[@id="song_container"]/li//@href')
            mp3_name=text.xpath('//ul[@id="song_container"]/li//@value')  
            mp3list=['',[]]
            for i in range(len(mp3_name)):
                n=mp3_href[i].rfind(r'/')
                href=mp3_href[i][n+1:-5]
                n=mp3_name[i].find(r'|')
                name=mp3_name[i][:n]
                n=name.find(r' ')
                name1=name[:n]
                name2=name[n+1:]
                name1=name1.replace('-','')
                name2=name2.replace('-','')
                if i==0:
                    mp3list[0]=name1
                mp3list[1].append([href,name2])  
            return mp3list
        
        def gd_list(url):#歌单
            headers = get_header()
            text = httpx.get(url, headers=headers).text
            text = lxml.html.fromstring(text)
            mp3_href=text.xpath('//div[@id="songs"]/ul/li//@href')
            mp3_name=text.xpath('//div[@id="songs"]/ul/li/a/@title')
            name1=text.xpath('//div[@id="songs"]/strong/text()')
            name1=re.compile(r'\<(.*?)\>').findall(name1[0])[0]
            mp3list=[name1,[]]
            for i in range(len(mp3_name)):
                n=mp3_href[i].rfind(r'/')
                href=mp3_href[i][n+1:-5]
                name2=mp3_name[i].replace('-','_')
                name2=name2.replace(' ','')
                mp3list[1].append([href,name2])   
            return mp3list
        def ts_list(url):#听书
            headers = get_header()
            text = httpx.get(url, headers=headers).text
            text = lxml.html.fromstring(text)
            mp3_href=text.xpath('//div[@class="tsa_d3_d2_li_d1"]//a/@href')
            mp3_name=text.xpath('//div[@class="tsa_d3_d2_li_d1"]//a/text()')
            name1=text.xpath('//span[@class="ts_comm_nav_sp3"]/text()')[0]
            #print(1,name1)
            mp3list=[name1,[]]
            for i in range(len(mp3_name)):
                n=mp3_href[i].rfind(r'/')
                href=mp3_href[i][n+1:-5]
                name2=mp3_name[i].replace('-','_')
                name2=name2.replace(' ','')
                if i==0:
                    mp3list[0]=name1
                mp3list[1].append([href,name2])
            #print(mp3list)    
            return mp3list
        self.finished.emit(f'正在解析{self.url}，请稍候....')
        mp3list=[]
        if self.url.find(r'singer/info')!=-1:#歌手
            mp3list=gs_list(self.url)
        if self.url.find(r'special/single')!=-1:#歌单
            mp3list=gd_list(self.url)
        if self.url.find(r'ts')!=-1:#听书
            for i in range(1,1000):
                plist=[]
                url=self.url if i==1 else f'{self.url}p{i}.html'
                #print(url)
                plist=ts_list(url)
                if len(plist[1])==0:
                    break
                if i==1:mp3list=plist
                else:mp3list[1]+=plist[1]
        print(mp3list)        
        if len(mp3list)==0:
           return
        finame=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',mp3list[0])#删除文件名特殊字符
        finame=finame.strip()
        if not os.path.exists(f'{os.getcwd()}/{finame}'):
           os.makedirs(f'{os.getcwd()}/{finame}')
        headers = get_header()
        headers['Cookie']='kg_mid=92f43c1ca98aeef7f805654bc16b687e; kg_dfid=10GOa11RqXIo2jvJbD3jt3BN; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1676853310,1677027739; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid_temp=7f78edda94881688da59d2c7ffa6ce07; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1677047356'
        data_url="https://wwwapi.kugou.com/yy/index.php"
        p={}
        p['r']='play/getdata'
        p['callback']='jQuery191041715852408178966_1677044560754'
        p['dfid']='3MnSiw25Vyxm3CNI0t4PrH8h'
        p['appid']='1014'
        p['mid']='7f78edda94881688da59d2c7ffa6ce07'
        p['platid']='4'
        p['_']='1677044560755'
        p['from']='112'
        for cc in mp3list[1]:
            try:
                p['encode_album_audio_id']=cc[0]
                mp3data=httpx.get(data_url,params=p, headers=headers).text#.content.decode()
                mp3url=re.compile(r'"play_url":"(.*?)",').findall(mp3data)
                mp3url=mp3url[0].replace('\\','')
                self.finished.emit(f'正在下载《{finame}》_{cc[1]}.....')
                rr=httpx.get(mp3url)
                rr.raise_for_status()
                save_file = f"{os.getcwd()}\\{finame}\\{cc[1].strip()}.mp3"
                #print(save_file)
                with open(save_file, 'wb') as (f):
                     f.write(rr.content)
            except:
                 pass
        self.finished.emit(f'下载{finame}:完成....')  
       
   

#print(get_mp3list('https://www.kugou.com/singer/info/7EHK63C0B716/'))
#print(get_url('凤凰传奇'))
#print(jx_kugou('https://www.kugou.com/singer/info/7EHK63C0B716/'))
