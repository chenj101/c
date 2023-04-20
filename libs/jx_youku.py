from libs.OpenHtml import *
#import lxml.html
import  pandas  as pd
import json
import sys,re
class J_youku:
    def __init__(self):
        pass
    def get(self,url):
        text0=open_html(url)
        text = lxml.html.fromstring(text0)
        fl=text.xpath('//meta[@name="irCategory"]/@content')[0]
        pm=text.xpath('//meta[@name="irAlbumName"]/@content')[0]
        if fl=='电影':
            purl=text.xpath('//meta[@itemprop="url"]/@content')[0]
            n=purl.find('?')
            purl=purl[:n]
            pname=[{'分类':fl,'片名':pm,'剧集':pm,'url':purl}]
        else:
            text=re.compile(r'"title":"选集".*"nodes":\[(.*?}\]).*"nodes":\[').findall(text0)
            text=json.loads(f'[{text[0]}')
            pname=[]
            for cc in text:
                jn=cc["data"]["title"]
                jn=re.compile(r'(第.*?集)').findall(jn)
                value=cc["data"]["action"]["value"]
                pname.append([{'分类':fl,'片名':stitle,'剧集':jn[0],'url':f'{url}{value}'}])
        return  pd.DataFrame(pname)
    def soso(self,name):#按影名搜
        try:
            url=f"https://v.qq.com/x/search/?q={name}&stag=0&smartbox_ab="
            html=open_html(url)
            html = lxml.html.fromstring(html)
            #item_type=Analysis(url,'//h3[@class="qy-search-result-tit title-score"]//span[@class="item-type"]//text()')
            ptitle=html.xpath('//div[@class="_playlist"]//a/@dt-params')
            phref=html.xpath('//div[@class="_playlist"]//a/@href')
            p1=self.get(phref[0])
        except:
            p1=[]    
        return p1
#print(J_youku().soso('东八区的先生们'))     
#print(J_youku().get('https://v.youku.com/v_show/id_XNTk0MTYwMzU4MA==.html?spm=a2hja.14919748_WEBTV_JINGXUAN.app.5~5!2~5!7~A&s=cedb16eeafc841058fb4&scm=20140719.manual.5295.show_cedb16eeafc841058fb4_%E9%A2%84%E8%A7%88'))
#print(J_youku().get('https://v.youku.com/v_show/id_XNTk1MjIwMzg2NA==.html?spm=a2hja.14919748_WEBMOVIE_JINGXUAN.app.5~5!2~5!9~A&scm=20140719.manual.4422.video_XNTk1MjIwMzg2NA%3D%3D_%E9%A2%84%E8%A7%88'))

