import httpx
import lxml.html
import html
import sys,re,os,time
#import yaml
def open_html(chaper_url):
    if chaper_url is None:
        return None
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.192.400 QQBrowser/11.5.5250.400',
               }
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
     #         }
    if chaper_url.find('v.youku.com')!=-1:
        headers['Referer']='https://www.youku.com/channel/webhome'
        time.sleep(1)
    try:
        response =httpx.get(chaper_url,headers=headers)#获取请求的返回数据
        '''
        #response.encoding = 'GBK' if chaper_url.find('sohu.com')!=-1 else  'utf-8'
        #定义编码，不然中文输出会乱码；
        with open(f'{os.getcwd()}\配置.yml','r') as f:
            pz=yaml.safe_load(f)   
        gbk=pz['gbk']
        response.encoding ='utf-8'
        for cc in gbk:
            if chaper_url.find(cc)!=-1:
                response.encoding ='GBK'
        '''        
        if response.status_code==200:#如果请求成功，则返回；
            return response.text
        return None
    except:return None
def p_html(url):#提源码
    text =open_html(url)
    if text==None:return '解码失败....'
    else:return text
def p_title(url):#提标题
    text =open_html(url)
    if text==None:return '解码失败....'
    else:
        text=text.replace('\n','')
        title=re.compile(r'<title.*?>(.*)</title>').findall(text)
    
        title=title[0]if bool(title) else ''
        title=title.strip()
        
        tj=['-','_',' ']
        for cc in tj:
            n=title.find(cc)
            if n!=-1:
                title=title[:n]
        if title[:3]=='&#x':
            title=html.unescape(title)
        return title
#print(p_title('https://www.ruiwen.com/'))
#print(p_title('http://www.360doc.com/index.html'))
def Analysis(url,pama):#正文、图片
    try:
        html0 = open_html(url)
        # 将HTML解析为统一的格式
        tree = lxml.html.fromstring(html0)
        print(html0)
        text = tree.xpath(pama)
        return  text
    except:return ''
#print(Analysis('https://errol.blog.csdn.net/article/details/88932834','//div[@class="content"]//p//text()|//div[@class="answer-content"]//p//text()|//div[@id="content_views"]//text()|//td[@id="artContent"]//text()|//div[@class="cont wk-content"]//text()|//div[@class="content Hidden"]//text()|//div[@class="ssr-container pageNo-1"]//text()|//div[@class="con_article f16 c6"]/p//text()|//div[@class="con_article con_main"]/p//text()|//div[@class="con_article"]/p//text()|//div[@class="con_main"]/p//text()'))  

#print(p_html('https://www.soyoung.com/p30591525'))
