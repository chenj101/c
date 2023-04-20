from PyQt5.QtCore import *
import httpx
import lxml.html
import os,sys
import re
import time
import json
#import math
import hmac
import js2py
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.192.400 QQBrowser/11.5.5250.400',
 #          'Host':'www.qingting.fm',
  #         'Cookie':'HWWAFSESID=d84f67394af7a40350; HWWAFSESTIME=1677547943691; Hm_lvt_bbe853b61e20780bcb59a7ea2d051559=1676530275,1677127238,1677210096,1677547956; Hm_lpvt_bbe853b61e20780bcb59a7ea2d051559=1677547956',
           }
class jx_qingting(QThread):    
    finished = pyqtSignal(str)
    def __init__(self,*url):
        QThread.__init__(self)
        self.url=url[0]
    def run(self):
        def get_sign():
            timestamp=str(round(time.time()*1000))
            data=f"/audiostream/redirect/{bookid}/{rid}?access_token=&device_id=MOBILESITE&qingting_id=&t={timestamp}"
            message=data.encode('utf-8')
            key="fpMn12&38f_2e".encode('utf-8')
            sign=hmac.new(key, message, digestmod='MD5').hexdigest()
            #sign='1be34422c23bc0f11c9ebcf2d3f3c1c5'
            return sign
            
        def mp3_down(bookid,rid):
            name1=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',bookname)#删除文件名特殊字符
            name2=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',rname)#删除文件名特殊字符
            if not os.path.exists(f'{os.getcwd()}/mp3/{name1}'):
                  os.makedirs(f'{os.getcwd()}/mp3/{name1}')
            timestamp=str(round(time.time()*1000))
            data=f"/audiostream/redirect/{bookid}/{rid}?access_token=&device_id=MOBILESITE&qingting_id=&t={timestamp}"
            message=data.encode('utf-8')
            key="fpMn12&38f_2e".encode('utf-8')
            sign=hmac.new(key, message, digestmod='MD5').hexdigest()
            whole_url=f'https://audio.qingting.fm{data}&sign={sign}'
            text =httpx.get(whole_url, headers=headers).text
            text = lxml.html.fromstring(text)
            d_url=text.xpath('//a/@href')
            
            if len(d_url)==0:
                return
            try:
                self.finished.emit(f'正在下载《{name1}》_{name2}.....')
                save_file = f"{os.getcwd()}/mp3/{name1}/{name2}.mp3"
                rr=httpx.get(d_url[0])
                rr.raise_for_status()
                with open(save_file, 'wb') as (f):
                    f.write(rr.content)
            except:
                 pass    

        if self.url.find('programs')!=-1:#(单曲)播放页
            text =httpx.get(f'{self.url}/', headers=headers).text
            text = lxml.html.fromstring(text)
            s=text.xpath('//script[@id="trans-layer"]/text()')[0]
            flist=str(js2py.eval_js(s))
            flist=(dict(eval(flist)))
            bookname=flist['ProgramStore']['channel']['name']
            bookid=flist['ProgramStore']['channel']['id']
            rid=flist['ProgramStore']['comments']['topic']['program_id']
            rname=flist['ProgramStore']['comments']['topic']['title']
            mp3_down(bookid,rid)
        else:#专集
            for i in range(1,1000):
                #多页面，取bookid重新建url
                u=self.url[33:]
                n=u.find(r'/')
                u=u[:n]
                u=f'https://www.qingting.fm/channels/{u}/'
                url_0=u if i==1 else f'{u}{i}/'
                text =httpx.get(url_0, headers=headers).text
                text = lxml.html.fromstring(text)
                s=text.xpath('//script[@id="trans-layer"]/text()')[0]
                flist=str(js2py.eval_js(s))
                flist=(dict(eval(flist)))
                bookname=flist['AlbumStore']['album']['name'] 
                bookid=flist['AlbumStore']['album']['id']
                plist=flist['AlbumStore']['plist']
                if len(plist)==0:
                    break
                for m in plist:
                    rname=m['name']
                    mp3_down(bookid,m['id'])
        self.finished.emit(f'下载完成.....')            

#run('https://www.qingting.fm/channels/293411/')
#url='https://www.qingting.fm/channels/293411/'
#url='https://www.qingting.fm/channels/293411/programs/11569182/'
