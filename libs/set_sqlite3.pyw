import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *#QColor, QFont, QIcon,QPixmap
from PyQt5.QtCore import *#Qt, QSize
from a_sqlite3 import *
class setdbpg(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Sqlite3数据库管理")
        self.resize(500,500)
        pcolor="background-color:cyan;color: rgb(0,0,255);"
        self.lab1 = QLabel("数据表列表")
        self.lab1.setStyleSheet("rgb(0,0,255);")
        self.lab2 = QLabel("")
        self.lab2.setStyleSheet("rgb(0,0,255);")
        self.table = QTableWidget()
        self.tablist = QListWidget(self)  #实例化列表控件
        self.tablist.doubleClicked.connect(lambda: self.tabshow())
        self.getdb()
        self.initUI()
             
        self.setup_centralWidget()
        self.tablist.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
        self.tablist.customContextMenuRequested.connect(self.list_fun)  # 绑定事件

          
    def initUI(self): #工具栏,菜单栏
        menubar = self.menuBar()
        ftab = menubar.addMenu('数据表维护')
        ftab_1 = ftab.addAction('新建表')
        ftab_2 = ftab.addAction('修改表')
        ftab_2.triggered.connect(lambda :self.set_tab(self.tablist.currentItem().text()))
        ftab_1.triggered.connect(lambda :self.set_tab(''))
        
      
        t1 =QAction(QIcon('images/exit.png'),'保存',self)
        t1.triggered.connect(lambda :self.sa())
       # t1.triggered.connect(lambda :os.system("pythonw pyqt5_main.py"))
        tad= QAction('增加一行',self)
        tad.triggered.connect(lambda :self.addr(0))
        tin= QAction('插入一行',self)
        tin.triggered.connect(lambda :self.addr(1))
        tdl= QAction('删除一行',self)
        tdl.triggered.connect(lambda :self.addr())
        td2= QAction('清空',self)
        td2.triggered.connect(lambda :self.del_all())
        self.toolbar = self.addToolBar('')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # 文字图片垂直排列
       # self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # 文字图片水平排列
    
        self.toolbar.addAction(t1)
        self.toolbar.addAction(tad)
        self.toolbar.addAction(tin)
        self.toolbar.addAction(tdl)
        self.toolbar.addAction(td2)
        self.toolbar.setVisible(False)
                
    def create_table(self,zd):
        self.table.clear()#清空表含表头 = QTableWidget()
        #self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #SelectedClicked #AllEditTriggers
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        HorizontalHeaderLabels = zd#["字段","类型"]
        columns = len(HorizontalHeaderLabels)
       # self.table.setRowCount(100)
        self.table.setColumnCount(columns)
        self.table.setHorizontalHeaderLabels(HorizontalHeaderLabels)
        #self.table.setVerticalHeaderLabels(["显示文本颜色","显示图标","空空如也"])
        headItem = self.table.horizontalHeaderItem(2)
        #headItem.setIcon(QIcon(":ICON/ICON/retest.png"))#设置headItem的图标
        self.headerWidth = (40,40,50,52,54,52,54,70)
        #self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止修改内容
        #self.table.setSortingEnabled (True)  #设定可自动排序（点击水平表头时，各行按该列数据自动排序）#默认为False
        #self.table.doubleClicked.connect(self.tab_dbClick)
       # self.table.setCellWidget(0,1,self.combox)
            
    def setup_centralWidget(self):
        #设置主窗口中心部件
       # self.tabWidget = QTabWidget()#分页page
       # self.tabWidget.addTab(self.table,"数据表结构")
        grid = QGridLayout()
        #grid.setSpacing(10)
        grid.setColumnStretch(0, 1);
        grid.setColumnStretch(1, 9);
        #grid.setColumnStretch(4, 0.5);
        #grid.setColumnStretch(1, 2);
        #grid.setColumnStretch(3, 9);
        grid.addWidget(self.lab1, 1, 0)
        grid.addWidget(self.lab2, 1,1) 
        grid.addWidget(self.tablist, 2, 0)
        grid.addWidget(self.table, 2,1) 

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
    def addr(self,inn):
        if inn==0:
            i=self.table.rowCount()
        else:
            i= self.table.currentIndex().row()
        self.table.insertRow(i)    
    def getdb(self):
        sql="select name from sqlite_master where type='table'"
        cc=s3db_q_list(sql)
        #print(s3db_q_pd(f"select * from sqlite_master"))
        for it in cc:
            self.tablist.addItem(it[0])
        #QMessageBox.critical(self,'提示',str(cc))    
        
        
    def tabshow(self):
       self.toolbar.setVisible(True) 
       #获取表的列名（字段名），保存在col_names列表,每个表的字段名集为一个元组
       tabname=self.tablist.currentItem().text()#表名
       sql='pragma table_info({})'.format(tabname)
       cc=s3db_q_list(sql)#字段列表，含名称（1），类型（2）
       #QMessageBox.critical(self,'提示',str(cc[0][1]))
       zd=[]
       for i in range(len(cc)):
           zd.append(cc[i][1])
       self.create_table(zd)#修改表及表头
       self.lab2.setText(tabname)
       sql="select * from "+tabname
       cc=s3db_q_list(sql)
       #QMessageBox.critical(self,'提示',str(cc))
       self.table.setRowCount(len(cc))#
       for i in range(len(cc)):
           sc=cc[i]
           for j in range(len(sc)):
               self.table.setItem(i,j,QTableWidgetItem(str(cc[i][j]))) 

           

    def set_tab(self,tabname):
        self.wid=settabpg()
        self.wid.fname.setText(tabname)
       # if tabname=='':
        #    print(1)
         #   self.wid.table.setColumnHidden(len(HorizontalHeaderLabels)-1,True)#隐藏列

        self.wid.tab_n()
        
        #self.wid.bok.clicked.connect(self.listtodb)
       
        self.wid.exec_()#show()
    #定义右键界面
    def list_fun(self,pos):
        
        self.tname=self.tablist.currentItem().text()
        popMenu = QMenu()
        popMenu.addAction(QAction(u'浏览表', self))
        popMenu.addAction(QAction(u'修改表', self))
        popMenu.addAction(QAction(u'删除表', self))
        popMenu.addAction(QAction(u'重命名', self))
        popMenu.triggered[QAction].connect(self.processtrigger)
        popMenu.exec_(QCursor.pos())

    def processtrigger(self,q):
        try:
            if q.text()=='浏览表':
               self.tabshow()      
            if q.text()=='修改表':
               self.set_tab(self.tname)
            if q.text()=='删除表':
                res_2 = QMessageBox.question(self, "删除表", "是否删除表:"+self.tname, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if res_2 ==QMessageBox.No:
                    return
                try:
                    s3db_u('drop TABLE {}'.format(self.tname))
                except:
                    s3db_u(f"delete from sqlite_master where name='{self.tname}'")
                item = self.tablist.currentItem()
                self.tablist.takeItem(self.tablist.row(item)) 

            if q.text()=='重命名':
                self.r_mw=r_pg()
                self.r_mw.tab1.setText(self.tname)
                self.r_mw.exec_()
        except:
            QMessageBox.about(self,'','表错误.....')
    def del_all(self):
        tabname=self.tablist.currentItem().text()#表名
        res_2 = QMessageBox.question(self, "删除表", "是否删除表:"+tabname, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if res_2 ==QMessageBox.No:
                return
        s3db_u(f'delete from {tabname}')
        self.table.setRowCount(0)#
        
    def sa(self):
        tabname=self.tablist.currentItem().text()#表名
        #sql='pragma table_info({})'.format(tabname)
        #cc=s3db_q_list(sql)#字段列表，含名称（1），类型（2）
        #print(cc)
        #return
        s_col=self.table.columnCount()#总列数
        s_row=self.table.rowCount()
        #print(self.table.horizontalHeaderItem(0).text())#列标题
        va={}
        for j in range(s_col):
            name=self.table.horizontalHeaderItem(j).text()
            va[name]=[]
            for i in range(s_row):
               rva='' if self.table.item(i,j)==None else self.table.item(i,j).text() 
               va[name].append(rva)
        df = pd.DataFrame(va)
       # del df['编号']
        
        pd_retab(df,tabname) #pd生成表
    
class r_pg(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("数据表重命名")
        self.resize(260,100)      
        self.tab1=QLineEdit('')
        self.tab1.setReadOnly(True)
        self.tab2=QLineEdit('')        
        self.but=QPushButton('确定')
        self.but.clicked.connect(lambda :self.r_tab())
        f= QFormLayout()
        f.addRow(QLabel("原表名"),self.tab1)
        f.addRow(QLabel("新表名"),self.tab2)
        f.addRow(QLabel(""))
        f.addRow(QLabel(""),self.but)
        self.setLayout(f)
            
    def r_tab(self):
         if self.tab2.text().strip()=='':
             QMessageBox.about(self,'','请录入新表名.....')
             return
         if self.tab2.text()[:1].isdigit():
            QMessageBox.about(self,'','表名第一位不能是数字.....')
            return 
             
         sql="ALTER TABLE {} RENAME TO {};".format(self.tab1.text(),self.tab2.text())
         s3db_u(sql)
         mw.tablist.currentItem().setText(self.tab2.text())
         self.close()
class settabpg(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Sqlite3数据库管理_数据表")
        
        self.lab1= QLabel("表名",self)
        self.fname=QLineEdit('')
        self.but=QPushButton('保存')
        self.but.clicked.connect(lambda :self.satab())
        self.but_ad=QPushButton('增加一行')
        self.but_ad.clicked.connect(lambda :self.addr(0))
        self.but_in=QPushButton('插入一行')
        self.but_in.clicked.connect(lambda :self.addr(1))
        self.but_dl=QPushButton('删除一行')
        self.but_dl.clicked.connect(lambda :self.delr())

        
        self.hd = ["字段","类型",'原字段名']
        self.create_table()
        #self.tab_n()
        #self.initUI()
        
        self.setup_centralWidget()
        self.resize(500,500)

           
       
    def tab_n(self):
        self.but.setText('新建保存')
        self.fname.setReadOnly(False)
        
        if self.fname.text()!='':
            self.fname.setReadOnly(True)
            self.tabshow(self.fname.text())
            self.but.setText('修改保存')
        else:
           self.table.setColumnHidden(len(self.hd)-1,True)#隐藏列
               
    def create_table(self):
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        
        columns = len(self.hd)
       # self.table.setRowCount(100)
        self.table.setColumnCount(columns)
        self.table.setHorizontalHeaderLabels(self.hd)
        headItem = self.table.horizontalHeaderItem(2)
        self.headerWidth = (40,40,50,52,54,52,54,70)
        #self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止修改内容      
            
    def setup_centralWidget(self):
        #设置主窗口中心部件
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(0,1);
        grid.setColumnStretch(1,1);
        grid.setColumnStretch(2,1);
        grid.setColumnStretch(3,1);
        #grid.setColumnStretch(3, 9);
        grid.addWidget(self.lab1, 1, 0)
        grid.addWidget(self.fname, 1, 1)
        grid.addWidget(self.but, 1, 2)
        grid.addWidget(self.but_ad, 2,0)
        grid.addWidget(self.but_in, 2,1)
        grid.addWidget(self.but_dl, 2,2)
        
        grid.addWidget(self.table, 3, 0,1,10)
        self.setLayout(grid)
    def delr(self):
        row= self.table.selectedItems()[0].row()
        self.table.removeRow(row)
       # QMessageBox.critical(self,'提示',str(row))    
        
    def addr(self,inn):
        if inn==0:
            i=self.table.rowCount()
        else:
            i= self.table.currentIndex().row()
        self.table.insertRow(i)
        self.combox=QComboBox()
        self.combox.addItems(['integer','real','varchar','text','blob','INTEGER PRIMARY KEY AUTOINCREMENT'])
        self.table.setCellWidget(i,1,self.combox)
          
        
    def satab(self):
        f1=[]
        f2=[]
        for i in range(self.table.rowCount()):
            if self.table.item(i,0)==None:
               continue
            if self.table.item(i,0).text().strip()=='':
               continue 
            fe1=self.table.item(i,0).text()+' '+self.table.cellWidget(i,1).currentText()
            fe=fe1 if i==0 else fe+','+fe1
            if self.table.item(i,2)!=None:
                if self.table.item(i,2).text().strip()!='':
                    f1.append(self.table.item(i,0).text())
                    f2.append(self.table.item(i,2).text())

        if len(f1)>0:
           sql='select {} from {}'.format(','.join(f2),self.fname.text())
           va=s3db_q_list(sql)#原表数据数据
           s3db_u('drop TABLE {}'.format(self.fname.text()))
          # print(va)   
        sql='CREATE TABLE {0}({1});'.format(self.fname.text(),fe)
        #print(sql)
        s3db_u(sql)
       # print('qqq')
        if len(f1)>0:#导入原表
           sql='INSERT INTO {}({}) VALUES({})'.format(self.fname.text(),','.join(f1),','.join(['?']*len(f1)))
           s3db_pu(sql,va) 
        QMessageBox.critical(self,'提示','保存成功....')
    def tabshow(self,tabname):
       
       #获取表的列名（字段名），保存在col_names列表,每个表的字段名集为一个元组
       sql='pragma table_info({})'.format(tabname)
       cc=s3db_q_list(sql)#字段列表，含名称（1），类型（2）
       #QMessageBox.critical(self,'提示',str(cc[0][1]))
       for i in range(len(cc)):
           self.addr(0)
           self.table.setItem(i,0,QTableWidgetItem(cc[i][1]))
           self.combox.setCurrentText(cc[i][2])
           self.table.setItem(i,2,QTableWidgetItem(cc[i][1]))
           
    def che(self):
        s=ss.sss('检查')
        QMessageBox.critical(self,'检查',s) 
        #print('combox1.currentIndex()')
       # if self.combox.currentIndex()>=0:
        #   self.table.setItem(self.tab_r,self.tab_c, QTableWidgetItem(self.combox.currentText()))
     
                      
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw =setdbpg()
    mw.show()
    sys.exit(app.exec_())
