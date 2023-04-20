from OpenHtml import *
#import lxml.html
import json
import sys,re
class J_qq:
    def __init__(self):
        pass
    def get(self,url):
        try:
            n=url.rfind(r'/')
            va_url=url[:n+1]
            
            html=open_html(url)
            html=re.compile(r'"listData":\[{"list":\[(.*?}\])\]').findall(html)
            html=html[0]
            html=html.replace('undefined','""')
            html=json.loads(html)
            pname=[]
            for i in range(len(html)):
                pname.append((html[i]['playTitle'],
                          f"{va_url}{html[i]['vid']}.html"))
        except:
            pname=[]
        return  pname
        
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
#print(J_qq().soso('东八区的先生们'))     
#print(J_qq().get('https://v.qq.com/x/cover/37q36y4w9bf8c9f/x0041cqsgck.html'))

