import requests
import re
import os
import inspect
cur_name = inspect.getfile(inspect.currentframe())#当前文件
cur_path = os.path.dirname(cur_name)#当前目录
def download_video(m3u8_url): #下载ts文件并整合为mp4文件
    for i,cc in enumerate(m3u8_url):
       print(i) 
       results = requests.get(cc)
       results.encoding = "utf8"
       with open(f"{cur_path}/ts_path/{i}.ts", "wb") as file:
            file.write(results.content)
       results.close()
    os.system(f'copy /b {cur_path}\\ts_path\\*.ts  {cur_path}\\ts_path\\aa.mp4')
    
