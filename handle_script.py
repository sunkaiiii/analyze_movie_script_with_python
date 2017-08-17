# coding=utf-8
import session
import os
import Global_Variables
from docx import Document
import jieba
import hibiscusMain
from xlwt import *

jieba.load_userdict('user_dic.txt')
"""
----------handle_scipt.py-------------
             记录整个剧本信息
"""
if not os.path.exists('out'):
    os.mkdir('out')


class shunjingbiao:
    '''存储顺景表信息的类'''

    def __init__(self, script_id=-1, script_num=-1, script_content='', main_content="", time='', role=[]):
        self.script_id = script_id
        self.script_num = script_num
        self.script_content = script_content
        self.main_content = main_content
        self.time = time
        self.role = role
        self.pagenum = float(len(self.script_content.split('\n'))) / 50.0


class Script:
    '''
    记录整个剧本的信息，包含多个场景（session）的类的实例
    '''

    def __init__(self, filename, mode=1):
        '''最后时间不太够，所有的方法都放在了init上面执行了，有点乱……
        #待修改部分
        '''
        self.mode = mode
        self.script_name = ''
        print('读取剧本')
        self.file_text = self.read_script_file(filename)
        Global_Variables.name_list = []
        print('程序推测主角')
        self.find_main_charactor(self.file_text, self.mode)
        main_role = ''
        for name in Global_Variables.name_list:
            main_role += name + ","
        main_role = main_role[:-1]
        print('推测主角为' + main_role)
        self.script_id = 0
        self.session_list = []  # 存放所有场次信息的list
        self.charactor_overrall_word_count_dic = {}  # 角色台词数
        self.charactor_overral_apear_in_session = {}  # 角色出现场次数
        self.charactor_emetion_word_in_session = {}  # 角色情感词

        self.shunjingbiao = {}
        self.shunchangbiao = {}

        self.all_ad_count = []
        self.session_ad_count = []

        self.all_sensitive_word_count_dic = {}

        '''顺场景表的信息'''
        self.in_place = 0
        self.out_place = 0
        self.location_count = {}
        self.in_place_time_count = {}
        self.out_place_time_count = {}
        self.role = {}
        self.timecount = {}

        self.charactor = Global_Variables.name_list
        for i in Global_Variables.name_list:
            self.charactor_overrall_word_count_dic[i] = 0

        self.all_charactor_count = {}
        print('处理场次信息')
        self.handle_session(self.file_text)
        print('统计角色台词数')
        self.cal_overrall_count()
        print('计算非主角出场次数')
        self.cal_all_character()
        print('计算主要角色出场次数')
        self.cal_character_apear_count()
        print('生成顺场景表')
        self.shunjingbiao_args = []
        self.shunchangbiao_args = []
        self.all_page_num = 0
        self.cal_shunchangjingbiaoxinxi()
        self.create_shunchangjingbiao()
        print("计算广告信息")
        self.session_ad_count = self.cal_ad_words_count()
        print("计算敏感词信息")
        self.cal_all_senstive_word_count()


    def find_main_charactor(self, file_text, mode=0):
        """
        两种剧本模式的推测主角方法不一
        1、简版剧本使用统计剧本中说话的频次数（即xxx说中的xxx出现次数的排序，前五个即为主角）
        2、标准版剧本使用一个开源大规模预料分析的额库，可以猜测没有在词库的情况下推测词（在剧本中，主角们被提到的次数通常是最多的，所以可以用来推测主角）
        但在推测主角过程中，如果跟人物小传中所记录的内容不一样（比如万人膜拜这个剧本人物小传和剧本中姓名并不对应）会导致统计出来的结果出现问题
        所以暂时没有启用这个推测功能（人物小传中应到加入一个别名，在别名内所有的称呼、昵称都应为这个角色，功能未做）
        """
        if mode == 0:
            a = 1
            # result = hibiscusMain.Hibiscus().analyseNovel(self.file_text)
            # for c in result:
            #     Global_Variables.name_list.append(c)
        elif mode == 1:
            user_dic = {}
            session_list = file_text.split('\n\n')
            for session in session_list:
                session = session.split('\n')
                for line in session:
                    line = line.replace('：', ":").replace(' ', '').replace('\n', '').replace('\ufeff', '')
                    if ':' in line:
                        if mode == 1:
                            charactor = line.split(':')[0]
                            user_dic.setdefault(charactor, 0)
                            user_dic[charactor] += 1
                        elif mode == 0:
                            info_list = Global_Variables.session_info_title
                            info_list.extend(Global_Variables.character_biographies)
                            if line.split(':')[0] in info_list:
                                continue
                            else:
                                charactor = line.split(':')[0]
                                user_dic.setdefault(charactor, 0)
                                user_dic[charactor] += 1
                                # elif mode==0:
                                #
            user_dic = sorted(user_dic.items(), key=lambda x: x[1], reverse=True)
            # print(user_dic)
            Global_Variables.name_list = []
            character_range = 5
            for i in range(0, character_range):
                Global_Variables.name_list.append(user_dic[i][0])
                # print(Global_Variables.name_list)


        for word in Global_Variables.name_list:
            jieba.add_word(word, 10000)


    def read_script_file(self, filename):
        """
        读取剧本，并处理剧本名字（剧本名字是带有剧本名字+时间戳的）转化为 script类的script_name
        :param filename: 上传的剧本的路径
        :return: 读取的剧本文本内容
        """
        name = os.path.splitext(filename)[0]
        self.script_name = name.split('\\')[len(name.split('\\')) - 1]
        script = ""
        # script=open(filename,encoding='utf-8').read()
        document = Document(filename)
        for para in document.paragraphs:
            script += para.text + '\n'
        # print(script)
        return script

    def handle_session(self, script):
        count = 0
        split_script = script.split('\n\n')  # 以双回车判断是否为一个场
        for s in split_script:
            if (len(s) <= 7):
                continue
            ss = session.Session(s, self.mode)
            self.session_list.append(ss)
            count += 1
            # ss.show_info()
            if count % 20 == 0:
                print('已处理' + str(count) + '场')

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

    def cal_ad_words_count(self):
        """
        统计广告词广告词
        return:返回（场次编号、广告词、广告词计数）
        """
        args = []
        self.all_ad_count = {}  # 先转换为字典方便存储
        for session in self.session_list:
            for word, count in session.session_ad_word_count_dic.items():
                args.append((session.session_number, word, count))
                self.all_ad_count.setdefault(word, 0)
                self.all_ad_count[word] += 1
        self.all_ad_count = sorted(self.all_ad_count.items(), key=lambda x: x[1], reverse=True)
        # for i in self.all_ad_count:
        #     print(i)
        # print(args)
        return args

    def cal_all_senstive_word_count(self):
        for session in self.session_list:
            for key, word_count in session.session_sensitive_word_count_dic.items():
                self.all_sensitive_word_count_dic.setdefault(key, 0)
                self.all_sensitive_word_count_dic[key] += word_count

    def cal_script_detail(self):
        '''读取用于写入scrit_detal表的信息'''
        script_detail_args = []
        for session in self.session_list:
            '''此处变量名与数据库中字段名对应，方便使用'''
            script_id = self.script_id
            script_number = session.session_number
            content = session.session_content
            role = ""
            role_id = ''
            role_number = 0
            role = role[:-1]
            role_id = role_id[:-1]
            if len(session.session_time) > 0:
                if session.session_time not in Global_Variables.time:
                    Global_Variables.time.append(session.session_time)
                period = session.session_time
            else:
                period = 0
            scene = session.session_location
            if len(session.session_place) > 0:
                if session.session_place not in Global_Variables.place:
                    Global_Variables.place.append(session.session_place)
                surroundings = session.session_place
            else:
                surroundings = 0
            # role_number = len(session.session_all_charactor_set)
            script_detail_args.append(
                (script_id, script_number, role_id, content, role, period, scene, surroundings, role_number))
        # for i in script_detail_args:
        #     print(i)
        return script_detail_args

    def cal_script_role(self):
        '''读取用于写入script_role表的信息'''
        script_roles = []
        for role_name, word_count in self.charactor_overrall_word_count_dic.items():
            # print(role_name,self.charactor_overral_apear_in_session[role_name],word_count)
            character_biographies = self.character_biographies_dic[role_name]
            script_roles.append(
                (role_name, character_biographies.num, character_biographies.gender,
                 character_biographies.age, character_biographies.career, character_biographies.constellation,
                 character_biographies.temperament, character_biographies.introduction, self.script_id, int(word_count),
                 int(self.charactor_overral_apear_in_session[role_name])))
        return script_roles

    def cal_session_role_word(self):
        '''计用于写入数据库的角色情感词'''
        args = []
        for session in self.session_list:
            self.charactor_emetion_word_in_session.setdefault(session.session_number, [])
            for Charactor in session.session_charactor_dic.values():
                self.charactor_emetion_word_in_session[session.session_number].append(Charactor)
                # print(self.charactor_emetion_word_in_session)
                for key, value in Charactor.charactor_emotion_dic.items():
                    for word in value:
                        args.append((word, key, Charactor.name, self.script_id, session.session_number))
        # print(args)
        return (args)

    def cal_participle(self):
        participle_args = []
        word_dic = {}
        script_id = self.script_id
        for session in self.session_list:
            for type, word_list in session.session_emotion_words_dic.items():
                for word in word_list:
                    word_dic.setdefault((word, session.session_number, type), 0)
                    word_dic[(word, session.session_number, type)] += 1
        for word_item, count in word_dic.items():
            participle_args.append((word_item[0], word_item[1], script_id, word_item[2], count))
        # for i in participle_args:
        #     print(i)
        return participle_args

    def cal_shunchangjingbiaoxinxi(self):
        """计算用于写入excel表格的顺场景表信息"""
        for session in self.session_list:
            self.shunjingbiao.setdefault(session.session_location, [])
            self.role.setdefault(session.session_number, [])
            '''分类相关的place，并计算室内场景和室外场景的数量以及这个室内室外中的场景时间计数'''
            if (session.session_place in Global_Variables.in_place):
                self.in_place += 1
                self.in_place_time_count.setdefault(session.session_time, 0)
                self.in_place_time_count[session.session_time] += 1
            else:
                self.out_place += 1
                self.out_place_time_count.setdefault(session.session_time, 0)
                self.out_place_time_count[session.session_time] += 1
            '''计算地点计数'''
            self.location_count.setdefault(session.session_location, 0)
            self.location_count[session.session_location] += 1
            '''统计角色在场景中出现的情况'''
            for character in session.session_charactor_dic.items():
                if character[1].appearance:
                    self.role[session.session_number].append(character[0])
            '''将在一个location的放入一个字典，里面存有具体的每个场景的顺景表的类'''
            self.shunjingbiao[session.session_location].append(
                shunjingbiao(self.script_id, session.session_number, session.session_content,
                             session.session_main_content, session.session_time,
                             self.role))
        self.shunjingbiao = sorted(self.shunjingbiao.items(), key=lambda x: len(x[1]),
                                   reverse=True)  # 按场景出现多到少的顺序排序，返回一个二维list

    def cal_session_ad_args(self):
        """
        生成插入session_ad_wods表的数据
        :return: 插入数据库的数据list
        """
        args = []
        for info in self.session_ad_count:
            args.append((info[0], info[1], info[2], self.script_id))
        return args

    def cal_script_ad_args(self):
        """
        生成插入script_ad_words表的数据
        :return: 插入数据库的list
        """
        args = []
        for session in self.session_list:
            for word in session.session_ad_word_set:
                args.append((Global_Variables.ad_word[word], session.session_number, self.script_id))
        return args

    def cal_script_sensitive_args(self):
        """
        生成插入script_sensitive_word表的数据
        :return:用于插入数据库的list
        """
        args = []
        sensitive_word_sort = sorted(self.all_sensitive_word_count_dic.items(), key=lambda x: x[1], reverse=True)
        for word, count in sensitive_word_sort:
            args.append((self.script_id, word, count))
        return args

    def create_base_excel(self, table, type=0):
        '''type=0的时候为顺景表，type=1的时候是顺场表,结束后返回生成的Excel表头'''
        style = XFStyle()
        alignment = Alignment()
        alignment.horz = Alignment.HORZ_CENTER
        alignment.vert = Alignment.VERT_CENTER
        style.alignment = alignment
        if type == 0:
            table.write_merge(2, 3, 1, 1, '场景', style)
            table.write_merge(2, 3, 2, 2, '拍摄地点', style)
            table.write_merge(2, 3, 3, 3, '场次', style)
            table.write_merge(2, 3, 4, 4, '气氛', style)
            table.write_merge(2, 3, 5, 5, '页数/行', style)
            table.write_merge(2, 3, 6, 6, '主要内容', style)
            table.write(2, 7, '角色', style)
            table.write(3, 7, '演员', style)
            index = 8
        else:
            table.write_merge(2, 3, 1, 1, '场次', style)
            table.write_merge(2, 3, 2, 2, '场景', style)
            table.write_merge(2, 3, 3, 3, '气氛', style)
            table.write_merge(2, 3, 4, 4, '页数', style)
            table.write_merge(2, 3, 5, 5, '主要内容', style)
            table.write(2, 6, '角色', style)
            table.write(3, 6, '演员', style)
            index = 7
        for role in Global_Variables.name_list:
            table.write(2, index, role, style)
            index += 1
        table.write(2, index, '特约及群众演员', style)
        index += 1
        table.write(2, index, '服化道', style)
        index += 1
        table.write_merge(2, 3, index, index, '其他', style)
        index += 1
        table.write_merge(2, 3, index, index, '计划时间', style)
        index += 1
        table.write_merge(2, 3, index, index, '备注', style)
        if type == 0:
            table.write_merge(1, 1, 0, index, '《' + self.script_name + '》顺景表', style)
        else:
            table.write_merge(1, 1, 0, index, '《' + self.script_name + '》顺场表', style)
        return table, index, style

    def write_info_into_excel(self, table, style, index, type):
        '''将场景信息写入相应的列中'''
        '''type=0的时候为顺景表，type=1的时候是顺场表,结束后返回生成的Excel表头'''
        if type == 0:
            for i in self.shunjingbiao:
                i2 = i[1]
                old_index = index
                index = index
                for i3 in i2:
                    # print(i[0],i3.role)
                    table.write(index, 3, str(i3.script_num), style)
                    table.write(index, 4, i3.time)
                    table.write(index, 5, str(round(i3.pagenum, 3)))
                    # table.write(index,6,i3.main_content)
                    column_index = 8
                    main_role = ''
                    self.all_page_num += i3.pagenum
                    for character in Global_Variables.name_list:
                        if character in self.role[i3.script_num]:
                            table.write(index, column_index, '√', style)
                            main_role += character + '|'
                        column_index += 1
                    main_role = main_role[:-1]
                    self.shunjingbiao_args.append(
                        [i[0], i3.script_num, str(round(i3.pagenum, 3)), i3.main_content, main_role])
                    index += 1
                table.write_merge(old_index, index - 1, 1, 1, i[0], style)
                table.write_merge(old_index, index - 1, 2, 2, '', style)
            return table, index
        else:
            for session in self.session_list:
                table.write(index, 1, session.session_number, style)
                table.write(index, 2, session.session_location, style)
                table.write(index, 3, session.session_time, style)
                table.write(index, 4, str(round(float(len(session.session_content.split('\n'))) / 50.0, 3)), style)
                # table.write(index,5,session.session_main_content)
                column_index = 7
                main_role = ""
                for character in Global_Variables.name_list:
                    if session.session_charactor_dic[character].appearance:
                        table.write(index, column_index, '√', style)
                        main_role += character + '|'
                    column_index += 1
                main_role = main_role[:-1]
                self.shunchangbiao_args.append([session.session_place, session.session_location, session.session_time,
                                                session.session_number,
                                                str(round(float(len(session.session_content.split('\n'))) / 50.0, 3)),
                                                session.session_main_content, main_role])
                index += 1
            return table, index

    def create_shunjingbiao(self):
        wb = Workbook()
        table = wb.add_sheet('顺景表')
        table, index, style = self.create_base_excel(table, type=0)
        width = index
        index = 4
        font = Font
        table, index = self.write_info_into_excel(table, style, index, type=0)
        table.write_merge(index, index, 1, 4, '全片场次总计：')
        table.write(index, 5, str(len(self.session_list)) + '场', style)
        index += 1
        table.write_merge(index, index, 1, 2, "内景：")
        string = ''
        string += str(self.in_place) + '场' + '（'
        for k, v in self.in_place_time_count.items():
            string += k + '：' + str(v) + '场、'
        string = string[:-1] + '）'
        table.write_merge(index, index, 3, width, string)
        index += 1
        table.write_merge(index, index, 1, 2, "外景：")
        string = ''
        string += str(self.out_place) + '场' + '（'
        for k, v in self.out_place_time_count.items():
            string += k + '：' + str(v) + '场、'
        string = string[:-1] + '）'
        table.write_merge(index, index, 3, width, string)
        index += 1
        string = ''
        for i in self.shunjingbiao:
            if len(i[1]) > 1:
                string += i[0] + '：' + str(len(i[1])) + '场' + '、'
        string = string[:-1]
        table.write_merge(index, index, 1, width, string)
        wb.save(self.script_name + '_顺景表.xls')

    def create_shunchangbiao(self):
        wb = Workbook()
        table = wb.add_sheet('顺场表')
        table, index, style = self.create_base_excel(table, type=1)
        width = index
        index = 4
        font = Font
        table, index = self.write_info_into_excel(table, style, index, type=1)
        table.write_merge(index, index, 1, width, '角色场次', style)
        index += 1
        for character in Global_Variables.name_list:
            table.write_merge(index, index, 1, width,
                              character + ':' + str(self.charactor_overral_apear_in_session[character]) + '场')
            index += 1
        wb.save(self.script_name + "_顺场表.xls")

    def create_shunchangjingbiao(self):
        self.create_shunjingbiao()
        self.create_shunchangbiao()


    def extend_sequnce_args(self):
        sequence_scene_id = self.get_sequence_scene_id()
        sequence_screening_id = self.get_sequence_screening_id()
        for i in range(len(self.shunjingbiao_args)):
            self.shunjingbiao_args[i].append(sequence_scene_id)
            self.shunjingbiao_args[i] = tuple(self.shunjingbiao_args[i])
        for i in range(len(self.shunchangbiao_args)):
            self.shunchangbiao_args[i].append(sequence_screening_id)
            self.shunchangbiao_args[i] = tuple(self.shunchangbiao_args[i])



    def showinfo(self, show_session_detail=0, show_line_detail=0):
        for k, v in self.charactor_overrall_word_count_dic.items():
            print(k + str(v))
        if show_session_detail == 1:
            for i in self.session_list:
                i.show_info(show_line_detail=show_line_detail)


if __name__ == "__main__":
    # print(1)
    import time

    # t=time.time()
    # script = Script('白鹿原201708101054.docx', mode=1)
    # print("用时"+str(int(time.time()-t))+"秒")
    # script = Script('让子弹飞201708101126.docx', mode=1)
    # script = Script('疯狂的石头201708101529.docx', mode=1)
    # script.showinfo(show_session_detail=1)
