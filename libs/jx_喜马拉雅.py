#数据接口
#https://www.ximalaya.com/revision/play/album
# 'http://m.ximalaya.com/m-revision/page/album/queryAlbumPage/%s?pageSize=%s'%(albumId,pageSize)
from PyQt5.QtCore import *
import httpx
import hashlib
import random
import lxml.html
#from lxml import etree
import os,sys
import re
import time
import json
class jx_ximalaya(QThread):
    finished = pyqtSignal(str)
    def __init__(self,*url):
        QThread.__init__(self)
        self.url=url[0]
    def run(self):  
        def get_sign(headers):# 获取sign签名
            serverTimeUrl = "https://www.ximalaya.com/revision/time"
            response = httpx.get(serverTimeUrl,headers=headers,verify=False)
            serverTime = response.text
            nowTime = str(round(time.time()*1000))
            sign = str(hashlib.md5("ximalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + serverTime + "({})".format(str(round(random.random()*100))) + nowTime
            # 在这里添加入请求头
            headers["xm-sign"] = sign
            return headers

        def get_header():
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
                    'Host': 'www.ximalaya.com',
                   'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, br',
                   'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   'Upgrade-Insecure-Requests': '1',
                   'Connection': 'keep-alive',
                   'Cache-Control': 'max-age=0',
            
                    }
            headers = get_sign(headers)
            return headers
        def mp3_down(name1,name2,playPath):
            finame=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',name1)#删除文件名特殊字符
            finame=finame.strip()
            if not os.path.exists(f'{os.getcwd()}/mp3/{finame}'):
                os.makedirs(f'{os.getcwd()}/mp3/{finame}')
            try:
                self.finished.emit(f'正在下载《{finame}》_{name2}.....')
                rr=httpx.get(playPath)
                rr.raise_for_status()
                name2=re.sub('\\|:|\*|\?|\"|<|>|/|\|','X',name2)#删除文件名特殊字符
                save_file = f"{os.getcwd()}/mp3/{finame}/{name2.strip()}.mp3"
                with open(save_file, 'wb+') as (f):
                     f.write(rr.content)
            except:
                 pass
 
        self.finished.emit(f'正在解析{self.url}，请稍候....')
        if self.url.find('www.ximalaya.com/album')!=-1:#专集
            n=self.url.rfind(f'/')
            albumId=self.url[n+1:]
            headers = get_header()
            albumURL =f'https://m.ximalaya.com/m-revision/page/album/queryAlbumPage/{albumId}?pageSize=1000'
            text = httpx.get(albumURL, headers=headers).text
            text=json.loads(text)
            name1=text['data']['albumDetailInfo']['albumInfo']['title']
            for m in text['data']['typeSpecData']['freeOrSingleAlbumData']['albumPageTrackRecords']['trackDetailInfos']:
                name2=m['trackInfo']['title']
                playPath=m['trackInfo']['playPath']
                mp3_down(name1,name2,playPath)
                
            
            #totalCount = text['data']['typeSpecData']['freeOrSingleAlbumData']['albumPageTrackRecords']['totalCount']
            #print(f'专集名:《{albumTitle}》,共有{totalCount}个音频')
        if self.url.find('www.ximalaya.com/sound')!=-1:#播放页
            pass
            '''
            n=self.url.rfind(f'/')
            albumId=self.url[n+1:]
            headers = get_header()
            albumURL =f'https://www.ximalaya.com/revision/play/v1/audio?id=559128135&ptype=1'
            albumURL =f'https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1669862585749?device=web&trackId=559128135&trackQualityLevel=1'
            text = httpx.get(albumURL, headers=headers).text
            #text=json.loads(text)
            print(text)
            '''
        self.finished.emit('下载完成....')
'''
:authority: www.ximalaya.com
:method: GET
:path: /revision/play/v1/audio?id=570796287&ptype=1
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cookie: _xmLog=h5&8f83fe82-12a7-49c7-ba10-59bc071c2ef3&process.env.sdkVersion; xm-page-viewid=ximalaya-web; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1663678783,1663682026; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1663714471
referer: https://www.ximalaya.com/sound/570796287
sec-ch-ua: ";Not A Brand";v="99", "Chromium";v="94"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.175.400 QQBrowser/11.1.5155.400
xm-sign: e25dfcab06ce90c155c131113fdf209b(12)1663715904290(0)1663715987714
'''
