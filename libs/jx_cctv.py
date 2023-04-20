import requests
import re
import os
from OpenHtml import *
from Download_video import * 
class jx_cctv(): 
    def get_ts(self,url): #获取章节名和路径
        text =open_html(url)
        if text==None:return '解码失败....'
        itemguid=re.compile(r'var itemguid="(.*)";').findall(text)[0]
        episode_urls=f'https://dh5.cntv.myalicdn.com/asp/h5e/hls/1200/0303000a/3/default/{itemguid}/1200.m3u8'
        text=requests.get(episode_urls).text.split(r'#')
        m3u3_url=[]
        for cc in text:
            if cc.find(r'.ts')!=-1:
                ts=re.compile(r'\n(.*)\n').findall(cc)[0]
                URL=f'https://dh5.cntv.myalicdn.com/asp/h5e/hls/1200/0303000a/3/default/{itemguid}/{ts}'
                m3u3_url.append(URL)
        return m3u3_url

s=jx_cctv().get_ts('https://v.cctv.com/2023/03/26/VIDE8BriEhm12C04qMpq0qh7230326.shtml?spm=C90324.PE6LRxWJhH5P.S23920.93')
download_video(s)
#print(jx_cctv().get_ts(s,))
#s=get_ts('https://dh5.cntv.myalicdn.com/asp/h5e/hls/1200/0303000a/3/default/71a9e92410514092a81108b20073afea/1200.m3u8')
#download_video(s)
