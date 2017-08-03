# coding=utf-8
import mySqlDB
import session
import os
import Global_Variables
from docx import Document

"""
----------handle_scipt.py-------------
             记录整个剧本信息
"""
if not os.path.exists('out'):
    os.mkdir('out')


class Script:
    '''
    记录整个剧本的信息，包含多个场景的类的实例
    '''

    def __init__(self, filename, script_id,mode=1,):
        self.mode = mode
        if self.mode == 1:
            self.find_main_charactor(filename)
        self.script_id = script_id  # 此处不应为固定值，而应该是获取id值，只是测试用设定为固定值
        self.script_name = ''
        self.session_list = []
        self.charactor_overrall_word_count_dic = {}
        self.charactor_overral_apear_in_session = {}
        self.charactor = Global_Variables.name_list  # 暂时读文件、后续会改
        for i in Global_Variables.name_list:
            self.charactor_overrall_word_count_dic[i] = 0
        self.all_charactor_count = {}
        self.read_script_file(filename)
        self.cal_overrall_count()
        self.cal_all_character()
        self.cal_character_apear_count()
        self.write_to_the_sql()

    '''
    当传入的是mode=1也就是简版剧本的时候，暂时的操作是先读取一遍剧本，寻找主要角色
    '''
    def find_main_charactor(self, filename):
        document = Document(filename)
        script = ''
        user_dic = {}
        for para in document.paragraphs:
            script += para.text + '\n'
        session_list = script.split('\n\n')
        for session in session_list:
            session = session.split('\n')
            for line in session:
                line = line.replace('：', ":").replace(' ', '').replace('\n', '').replace('\ufeff', '')
                if ':' in line:
                    charactor = line.split(':')[0]
                    user_dic.setdefault(charactor, 0)
                    user_dic[charactor] += 1
        user_dic = sorted(user_dic.items(), key=lambda x: x[1], reverse=True)
        Global_Variables.name_list = []
        for i in range(0, 7):
            Global_Variables.name_list.append(user_dic[i][0])
            # print(Global_Variables.name_list)

    def read_script_file(self, filename):
        name = os.path.splitext(filename)[0]
        self.script_name = name.split('\\')[len(name.split('\\')) - 1]
        script = ""
        # script=open(filename,encoding='utf-8').read()
        document = Document(filename)
        for para in document.paragraphs:
            script += para.text + '\n'
        # print(script)
        split_script = script.split('\n\n')  # 以双回车判断是否为一个场
        for s in split_script:
            ss = session.Session(s, self.mode)
            self.session_list.append(ss)

    def cal_overrall_count(self):
        """
        统计每个角色的台词数
        """
        for session in self.session_list:
            for keys, session_charactor_info in session.session_charactor_dic.items():
                self.charactor_overrall_word_count_dic[keys] += session_charactor_info.charactor_world_amount

    def cal_all_character(self):
        """
        计算角色（包含非主要角色）出场次数
        """
        for session in self.session_list:
            for name in session.session_all_charactor_set:
                self.all_charactor_count.setdefault(name, 0)
                self.all_charactor_count[name] += 1

        '''输出所有角色出现次数的排序（未分词）到屏幕，可以发现主要人物'''
        # print(sorted(self.all_charactor_count.items(), key=lambda x: x[1], reverse=True))

    def cal_character_apear_count(self):
        """
        计算主要角色的出场次数
        """
        for session in self.session_list:
            for name, apear in session.session_charactor_dic.items():
                self.charactor_overral_apear_in_session.setdefault(name, 0)
                if apear.appearance:
                    self.charactor_overral_apear_in_session[name] += 1
                    # print(self.charactor_overral_apear_in_session)

    def cal_script_detail(self):
        script_detail_args = []
        for session in self.session_list:
            '''此处变量名与数据库中字段名对应，方便使用'''
            script_id = self.script_id  # 剧本id暂时为0，稍后修改
            script_number = session.session_number
            content = session.session_content
            role = ""
            role_number = 0
            for name in session.session_charactor_dic.keys():
                if session.session_charactor_dic[name].appearance:
                    role += name + '|'
                    role_number += 1
            if len(session.session_time) > 0:
                Global_Variables.time.setdefault(session.session_time, max(Global_Variables.time.values()) + 1)
                period = Global_Variables.time[session.session_time]
            else:
                period = 0
            scene = session.session_location
            if len(session.session_place) > 0:
                Global_Variables.place.setdefault(session.session_place, max(Global_Variables.place.values()) + 1)
                surroundings = Global_Variables.place[session.session_place]
            else:
                surroundings = 0
            # role_number = len(session.session_all_charactor_set)
            script_detail_args.append(
                (script_id, script_number, content, role, period, scene, surroundings, role_number))
        # for i in script_detail_args:
        #     print(i)
        return script_detail_args

    def cal_script_role(self):
        script_roles = []
        for role_name, word_count in self.charactor_overrall_word_count_dic.items():
            # print(role_name,self.charactor_overral_apear_in_session[role_name],word_count)
            script_roles.append(
                (role_name, int(word_count), self.script_id,int(self.charactor_overral_apear_in_session[role_name])))
        # for i in script_roles:
        #     print(i)
        return script_roles

    def cal_participle(self):
        participle_args = []
        verson = self.script_id  # 剧本版本暂时定位0，以后会改
        for session in self.session_list:
            words = []
            for word_list in session.session_emotion_words_dic.values():
                words.extend(word_list)
            words = set(words)
            for word in words:
                participle_args.append((word, session.session_number, verson))
        # for i in participle_args:
        #     print(i)
        return participle_args

    def write_to_the_sql(self):
        script_detail_args = self.cal_script_detail()
        script_roles = self.cal_script_role()
        participle_args = self.cal_participle()
        print('写入数据库')
        print('写入剧本信息表')
        mySqlDB.write_script_detail_info(script_detail_args)
        print("写入剧本角色表")
        mySqlDB.write_script_role_info(script_roles)
        print("写入中间词表")
        mySqlDB.write_participle_info(participle_args)
        print("写入完成")

    def showinfo(self, show_session_detail=0, show_line_detail=0):
        for k, v in self.charactor_overrall_word_count_dic.items():
            print(k + str(v))
        if show_session_detail == 1:
            for i in self.session_list:
                i.show_info(show_line_detail=show_line_detail)


if __name__ == "__main__":
    # print(1)
    script0=Script('白鹿原_改.docx',0,mode=1)
    script0 = Script('疯狂的石头_改.docx', 1, mode=1)
    script = Script('让子弹飞、新、改.docx', 2,mode=1)
    # script.write_info_to_mysql()
    # print(script.script_name)
    # script.showinfo(show_session_detail=1)
    # script.write_character_total_words()
    # script.write_charactor_overral_apear()
    # script.write_session_emotion()
    # script.write_session_words()
