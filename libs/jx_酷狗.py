#数据接口
#import requests
from PyQt5.QtCore import *
import httpx
import lxml.html
import os,sys
import re
import time
import json
class jx_kugou(QThread):
    finished = pyqtSignal(str)
    def __init__(self,*url):
        QThread.__init__(self)
        self.url=url[0]
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
            for i in range(len(mp3_name)):
                n=mp3_href[i].rfind(r'/')
                rid=mp3_href[i][n+1:-5]
                n=mp3_name[i].find(r'|')
                name=mp3_name[i][:n]
                n=name.find(r' ')
                name1=name[:n]
                name2=name[n+1:]
                name1=name1.replace('-','')
                name2=name2.replace('-','')
                mp3_down(name1,f'{name2}_{i:0>4d}',rid) 
            self.finished.emit(f'{name1}:下载完成....')
        def gd_list(url):#歌单
            headers = get_header()
            text = httpx.get(url, headers=headers).text
            text = lxml.html.fromstring(text)
            mp3_href=text.xpath('//div[@id="songs"]/ul/li//@href')
            mp3_name=text.xpath('//div[@id="songs"]/ul/li/a/@title')
            name1=text.xpath('//div[@id="songs"]/strong/text()')
            name1=re.compile(r'\<(.*?)\>').findall(name1[0])[0]
            for i in range(len(mp3_name)):
                n=mp3_href[i].rfind(r'/')
                rid=mp3_href[i][n+1:-5]
                name2=mp3_name[i].replace('-','_')
                name2=name2.replace(' ','')
                mp3_down(name1,f'{name2}_{i:0>4d}',rid)
            self.finished.emit(f'{name1}:下载完成....')    
        def ts_list(page):#听书
            url=ts_url if page==1 else f'{ts_url}/p{page}.html'
            headers = get_header()
            text = httpx.get(url, headers=headers).text
            text = lxml.html.fromstring(text)
            mp3_href=text.xpath('//div[@class="tsa_d3_d2_li_d1"]//a/@href')
            mp3_name=text.xpath('//div[@class="tsa_d3_d2_li_d1"]//a/text()')
            name1=text.xpath('//span[@class="ts_comm_nav_sp3"]/text()')[0]
            if len(mp3_href)>0:
                for i in range(len(mp3_name)):
                    n=mp3_href[i].rfind(r'/')
                    rid=mp3_href[i][n+1:-5]
                    name2=mp3_name[i].replace('-','_')
                    name2=name2.replace(' ','')
                    mp3_down(name1,f'{name2}_{page}{i:0>3d}',rid)
                page+=1
                ts_list(page)
            self.finished.emit(f'{name1}:下载完成....')    
        def mp3_down(name1,name2,rid):
            finame=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',name1)#删除文件名特殊字符
            finame=finame.strip()
            if not os.path.exists(f'{os.getcwd()}/mp3/{finame}'):
                os.makedirs(f'{os.getcwd()}/mp3/{finame}')
            
            p['encode_album_audio_id']=rid
            try:
                mp3data=httpx.get(data_url,params=p, headers=data_headers).text#.content.decode()
                #print(name2,mp3data)
                mp3url=re.compile(r'"play_url":"(.*?)",').findall(mp3data)
                mp3url=mp3url[0].replace('\\','')
                self.finished.emit(f'正在下载《{finame}》_{name2}.....')
                rr=httpx.get(mp3url)
                rr.raise_for_status()
                name2=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',name2)#删除文件名特殊字符
                save_file = f"{os.getcwd()}/mp3/{finame}/{name2.strip()}.mp3"
                
                #print(save_file)
                with open(save_file, 'wb+') as (f):
                     f.write(rr.content)
            except:
                 pass
             
        
        self.finished.emit(f'正在解析{self.url}，请稍候....')
        data_url="https://wwwapi.kugou.com/yy/index.php"
        data_headers = get_header()
        data_headers['Cookie']='kg_mid=92f43c1ca98aeef7f805654bc16b687e; kg_dfid=10GOa11RqXIo2jvJbD3jt3BN; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1676853310,1677027739; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; kg_mid_temp=7f78edda94881688da59d2c7ffa6ce07; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1677047356'
        p={}
        p['r']='play/getdata'
        p['callback']='jQuery191012623039926757973_1677115077132'
        p['dfid']='3MnSiw25Vyxm3CNI0t4PrH8h'
        p['appid']='1014'
        p['mid']='7f78edda94881688da59d2c7ffa6ce07'
        p['platid']='4'
        p['_']='1677115077133'
        p['from']='112'
        if self.url.find(r'singer/info')!=-1:#歌手
            mp3list=gs_list(self.url)
        if self.url.find(r'special/single')!=-1:#歌单
            mp3list=gd_list(self.url)
        if self.url.find(r'ts')!=-1:#听书
            n=self.url.rfind(r'/')
            ts_url=self.url[:n]
            ts_list(1)
            
               
       
        
        
         
       
   

#print(get_mp3list('https://www.kugou.com/singer/info/7EHK63C0B716/'))
#print(get_url('凤凰传奇'))
#print(jx_kugou('https://www.kugou.com/singer/info/7EHK63C0B716/'))
