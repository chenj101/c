import streamlit as st
import sys,os
class Get_file_txt():
    def get_path(self,fpath):
        path0=os.listdir(f'{fpath}')
        path01=[]
        for cc in path0:
            if os.path.isdir(f"{fpath}/{cc}"):
                path01.append(cc)
        return path01
    
    def get_ml(self,fpath):
        path1=os.listdir(fpath)
        file11=[]
        file12=[]
        for cc in path1:
            if os.path.isfile(f"{fpath}/{cc}")\
               and cc[-4:]==r'.txt':
                file11.append(cc[:-4])
                file12.append(f"{fpath}/{cc}")
        return  file11,file12
    
    def get_file(self,ml,file12):
        file=''
        for i in range(len(file12)):
            n=file12[i].rfind(r'/')
            if file12[i][n+1:]==f'{ml}.txt':
                file=file12[i]
        with open(file,'r') as f:    
             pz= f.readlines()
             pz[0]=f"&emsp;&emsp;{pz[0]}"
        return r'<br />&emsp;&emsp;'.join(pz)
    
    def sa_file(self,**kwargs):#保存
        with open(kwargs['sa_name'],'w') as f:    
           f.write(st.session_state.sa_text_values)
