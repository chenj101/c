import sys,time
import yaml
import streamlit as st

sys.path.append('../libs')
sys.path.append('../img')
from libs.a_sqlite3 import *
from libs.OpenHtml import *
#from libs.jx_vid import *
from libs.jx_iqiyi import *
#from libs.jx_qq import *
from libs.jx_mgtv import *
#from libs.jx_wasu import *
from libs.jx_pptv import *
from libs.jx_le import *
#from libs.jx_喜马拉雅 import *
#from libs.jx_酷狗 import *
#from libs.jx_酷我 import *
#from libs.jx_蜻蜓fm import *

st.set_page_config(page_title="练习",layout="wide") #设置屏幕展开方式，宽屏模式布局更好
hide_style='''
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
</style>
'''
st.markdown(hide_style, unsafe_allow_html=True)#掩藏底部链接
#cookie_manager = stx.CookieManager()
#cookie_manager.set('username','hhhhhhhh')
def log_in():#登录
   userid=st.session_state['username_dl']
   paw=st.session_state['password_dl']
   df=s3db_q_pd(f"select * from 用户 where id='{userid}'")
   if df.shape[0]==0: st.warning("用户未注册! ⚠️")
   elif paw!=df.loc[0,'口令']:st.warning("口令错误! ⚠️")
   else:
       st.session_state['name']=df.loc[0,'姓名']
       st.session_state['qx']=df.loc[0,'权限']
       st.session_state['username']=userid
       st.success("登录成功")
       st.balloons()
     
def user_in():#注册
   userid=st.session_state['username_in']
   df=s3db_q_pd(f"select * from 用户 where id='{userid}'")
   if df.shape[0]>0:
      st.warning("已存在注册用户! ⚠️")
   else:
       paw=st.session_state['password_in']
       name=st.session_state['name_in']
       s3db_u(f"INSERT INTO 用户(id,姓名,口令) values('{userid}','{name}','{paw}')")
       st.success("注册成功,请登录...")
       st.balloons()
def user_up():#修改
   up=[f"set 姓名='{st.session_state.name_up}'"]
   if st.session_state['paw_up']:
      up.append(f"口令='{st.session_state.password_new}'")
   s3db_u(f"update 用户 {','.join(up)} where id='{st.session_state.username}'")
   st.success("修改成功...")   
def qx_up(*args):#修改权限
   n=add_user.find('_')
   pid=add_user[:n]
   qx='|'.join(add_qx)
   s3db_u(f"update 用户 set 权限='{qx}' where id='{pid}'")
   
if not bool(st.session_state.get('username')):
   st.session_state['username']=''
   st.session_state['name']=''
   add_radio = st.sidebar.radio("用户",['登录','注册','网页解析'])
else:
   with st.sidebar.container():
        cols1,cols2 = st.columns(2)
        cols1.write(f'欢迎 {st.session_state.name}')
        logout=cols2.button('注销')
        if logout:
           st.session_state['username']=''
           st.session_state['qx']=''
   add_radio = st.sidebar.radio("用户",['用户资料','用户管理','网页解析'])      
if add_radio =='登录':
   with st.form('用户登录'):
       st.write('用户登录')
       username=st.text_input('用户名', key='username_dl')     
       password=st.text_input('口令', type='password', key='password_dl')
       st.form_submit_button('确定', on_click=log_in)
            
if add_radio =='注册':
   with st.form('用户注册'):
       bt=st.write('用户注册')
       username = st.text_input('用户名', key='username_in')
       name = st.text_input('姓名', key='name_in')        
       password = st.text_input('口令', type='password', key='password_in')
       st.form_submit_button('确定', on_click=user_in)

if add_radio =='用户资料':
   with st.form('用户资料'):
       bt=st.write('用户资料')
       name = st.text_input('姓名',value=st.session_state.name,key='name_up')        
       up_paw=st.checkbox('修改口令',key='paw_up')
       password_new = st.text_input('新口令', type='password',key='password_new')
       st.form_submit_button('确定', on_click=user_up)       
      
if add_radio =='用户管理':
   if add_radio not in st.session_state['qx']:
      st.warning("无权限浏览! ⚠️")
      st.stop()
   qxlist=['编辑','用户管理','Python专题','Streamlit专题','小说']
   df=s3db_q_pd(f"select * from 用户")
   df['user']=df["id"].map(str).str.cat([df["姓名"]],sep='_')#合并列
   userlist=[x for x in df['user']]
   with st.container():
        cols1,cols2,cols3 = st.columns(3)
        add_user=cols1.radio("用户列表",userlist)
        n=add_user.find('_')
        pid=add_user[:n]
        qx=df.loc[df['id']==pid,'权限'].values[0]
        if not bool(qx) or qx=='None':qx=[]
        else:
           qx1=qx.split('|')
           qx=[]
           for x in qx1:
              if x in qxlist:
                 qx.append(x)
        qxsa=cols2.button('保存权限',on_click=qx_up)         
        add_qx=cols2.multiselect("权限",qxlist,default=qx)#['用户管理','Python专题'])
#===========网页解析========================          
if add_radio =='网页解析':
   st.image(r".\img\png-0022.png") 
   st.markdown('<a href="https://www.baidu.com"><img src="img/png-0022.png"></a>',unsafe_allow_html=True)
   with st.form('网页解析'): 
       with st.container():
            w_cols1,w_cols2= st.columns(2)
            w_url=w_cols1.text_input('网址',value='')
            w_ok=w_cols2.selectbox("功能",['文字','图片','视频'])
       w_img=st.checkbox('图片网址(jpg格式不能正常显示)')
       w_butt=st.form_submit_button('确定')#, on_click=w_open)
   if (not w_butt) or (not bool(w_url)):st.stop()
   with open(f'{os.getcwd()}\pages\配置.yml','r') as f:
        pz=yaml.safe_load(f)   
   if w_ok=='文字':      
       va='|'.join(pz['txt'])
       text=Analysis(w_url,va)
       st.markdown('\n'.join(text))
   if w_ok=='图片':         
       va='|'.join(pz['img'])
       img=Analysis(w_url,va)
       img=[f"https:{x}" if x.find('http')==-1 else x for x in img]
       if w_img:
          st.markdown(r'<br />'.join(img),unsafe_allow_html=True)
       else:st.image(img)#,caption=None, width=None,use_column_width=None,clamp=False, channels="RGB",output_format="auto")
   if w_ok=='视频':
       with st.form('视频解析'):  
           with st.spinner('正在搜索，请稍候...'):
               time.sleep(1)
               u=re.compile(r'\.(.*?)\.').findall(w_url)[0]
               if u in ['iqiyi','qq','mgtv','wasu','pptv','le']:
                   pm_df=eval(f"J_{u}().get('{w_url}')")
               else:    
                  u=f'jx_{u}("{w_url}")'
                  pm_df=eval(u)
               pm_df['pm']=pm_df["片名"].map(str).str.cat([pm_df["剧集"]],sep='_')#合并列    
               pm_list=st.multiselect("片名",pm_df['pm'],default=pm_df['pm'])
               pm_butt=st.form_submit_button('保存')
               if pm_butt and len(pm_list)>0:
                   df_pm=pm_df[pm_df['pm'].isin(pm_list)]
                   df_pm=df_pm[['分类','片名','剧集','url']]
                   pdtos3tab(df_pm,'视频库')
  
    
