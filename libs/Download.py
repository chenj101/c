import requests
import re
import os
import subprocess
os.environ['path']=f"{os.environ.get('path')};{os.getcwd()}\\ffmpeg\\bin"#配置ffmpeg环境,只对本程序有效
def download_video(m3u8_url): #下载ts文件并整合为mp4文件
    for i,cc in enumerate(m3u8_url):
       print(i) 
       results = requests.get(cc)
       results.encoding = "utf8"
       with open(f"./ts_path/{i}.ts", "wb") as file:
            file.write(results.content)
       results.close()
    #os.system('copy /b ./ts_path/*.ts  ./ts_path/aa.mp4')
path='f:\\python\\st1\\libs\\ts_path\\'
#os.system(f'copy /b {path}*.ts  {path}aa.mp4')

com = f'ffmpeg -f concat -safe 0 -i name.txt -c copy -strict -2 -pass 2 aa.mp4 -y'
print(com)
subprocess.run(com)

print('ok')    
