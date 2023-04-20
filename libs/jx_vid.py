from OpenHtml import *
#import lxml.html
import json
import sys,re
def jx_sohu(url):
    va_url=Analysis(url,'//meta[@property="og:url"]/@content')[0]
    pname=Analysis(url,'//meta[@property="og:title"]/@content')[0]
    pname=[(pname,va_url)]
    return  pname
#print(jx_sohu('http://tv.sohu.com/20220616/n601190784.shtml'))


def jx_youku(url):
  #  va_url=Analysis(url,'//@href')
   # va_url=Analysis(url,'//a[@class="top-component-title "]/a/text()')
   # print(va_url)
    #pname=Analysis(url,'//div[@class="anthology-content"][@data-spm="1_3"]/@title')
    #print(pname)
  #  pva=[]
   # for i in range(len(pname)):
    #    pva.append((pname[i],va_url[i]))
    #if len(pva)==0:
    pva=[('未能完全解析，请直接播放','')] 
    return  pva
#print(jx_youku('https://v.youku.com/v_show/id_XNTg4NDExNDIwNA==.html?spm=a2hbt.13141534.1_3.1&s=efbfbd1e204e0fefbfbd'))
def jx_ixigua(url):
    '''
    print(url)
    #va_url=Analysis(url,'//div[@class="anthology-content"@data-spm="1_3"]/a/@href')
    va_url=Analysis(url,'//a[@class="top-component-title "]/text()')
    print(va_url)
    pname=Analysis(url,'//div[@class="anthology-content"]/@title')
    #print(pname)
    pva=[]
    for i in range(len(pname)):
        pva.append((pname[i],va_url[i]))
    if len(pva)==0:
    '''
    pva=[('未能完全解析，请直接播放','')] 
    return  pva
#print(jx_ixigua('https://www.ixigua.com/6709747094648783368?logTag=ad7266b3b25c717633bf'))


