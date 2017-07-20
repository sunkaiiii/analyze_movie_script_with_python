import session
import os
from imp import reload
import Global_Variables


class Script:
    def __init__(self,filename,mode=0):
        self.mode=mode
        self.script_name=''
        self.session_list=[]
        self.charactor_overrall_word_count_dic={}
        for i in Global_Variables.name_list:
            self.charactor_overrall_word_count_dic[i]=0
        self.read_script_file(filename)
        self.cal_overrall_count()
    def read_script_file(self,filename):
        name=os.path.splitext(filename)[0]
        self.script_name=name.split('\\')[len(name.split('\\'))-1]
        script=open(filename,encoding='utf-8').read()
        split_script=script.split('\n\n')
        for s in split_script:
            ss=session.Session(s,self.mode)
            self.session_list.append(ss)

    def cal_overrall_count(self):
        for session in self.session_list:
            for keys,session_charactor_info in session.session_charactor_dic.items():
                self.charactor_overrall_word_count_dic[keys]+=session_charactor_info.charactor_world_amount


    def showinfo(self,show_session_detail=0,show_line_detail=0):
        for k,v in self.charactor_overrall_word_count_dic.items():
            print(k+str(v))
        if show_session_detail==1:
            for i in self.session_list:
                i.show_info()
if __name__=="__main__":
    script=Script('let_bullet_fly.txt',mode=1)
    print(script.script_name)
    script.showinfo()