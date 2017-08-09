# coding=utf-8
import line
import Global_Variables
import jieba

"""
------------session.py--------------
记录一个场次的内容，里面包含多个行的Line类实体
"""


class Charactor():
    '''
    记录一个场当中演员的信息的类
    '''

    def __init__(self, name=""):
        self.name = name
        self.charactor_worlds = []
        self.charactor_world_amount = 0
        self.charactor_emotion_dic = {}
        for name in Global_Variables.word_list_dic:
            self.charactor_emotion_dic.setdefault(name, [])
        self.appearance = False  # 是否在这个场景出现
        self.charactor_value = 0


class Session():
    def __init__(self, session_content, mode=1):
        '''
        :param session_content: 切割好的一场的所有内容
        :param mode: 0、详细格式的场景信息的切割
                                1、简单格式的剧本场景信息的切割
        '''

        self.mode = mode
        self.session_number = 0
        self.session_time = ''
        self.session_place = ''
        self.session_location = ''
        self.main_people = ""
        self.main_emotion = ""
        self.line_list = []
        self.session_content = ''
        self.session_main_content=''
        self.session_emotion_value=0
        self.session_emotion_words_dic = {}
        self.session_emotion_words_set_dic = {}
        for name in Global_Variables.word_list_dic.keys():
            self.session_emotion_words_dic.setdefault(name, [])
            self.session_emotion_words_set_dic.setdefault(name, set())
        self.session_content = session_content
        self.session_words_amount = 0
        self.session_charactor_dic = {}
        for i in Global_Variables.name_list:  # 使用字典存放场景角色的信息
            self.session_charactor_dic[i] = Charactor(i)
        self.session_all_charactor = []  # 存放未切割的对话人物，可用于寻找主要角色（人工或继续分词）
        self.session_all_charactor_set = set()
        self.read_session_lines()
        self.cal_words_amount()
        self.cal_main_content()

    def read_session_lines(self):
        count = 0  # count记录是否为场景信息，当为0的时候即为场景信息行
        for i in self.session_content.split('\n'):
            if len(str(i).strip('\n').strip(' ')) == 0:
                continue
            if count != 0:
                session_line = line.Line(i, self.mode)
                self.line_list.append(session_line)
                for name, word in session_line.emotion_word_dic.items():
                    self.session_emotion_words_dic[name].extend(word)
                    # print(self.session_emotion_words_dic)
            else:
                if self.mode == 0:
                    session_info = i.strip(' ')
                    session_info = session_info.replace('：', ':')
                    session_info = session_info.split(':')
                    ok = False
                    for index in range(0, len(Global_Variables.session_info_title)):  # 找到切割出来的标头是对应的什么常吃信息
                        if session_info[0].strip('\ufeff') in Global_Variables.session_info_title[index]:
                            ok = True  # 当OK不为True的时候，认为场景信息已经读取完成
                            if index == 0:
                                self.session_number = session_info[1].strip('.').strip('、').strip(' ').strip('\ufeff')
                            elif index == 1:
                                self.session_location = session_info[1].strip(' ')
                            elif index == 2:
                                self.session_time = session_info[1].replace(' ','').replace('\n','')
                            elif index == 3:
                                self.session_place = session_info[1].strip(' ').replace(' ', '').replace('\n', '')
                            elif index == 4:
                                self.main_people = session_info[1].strip(' ')
                            elif index == 5:
                                self.main_emotion = session_info[1].strip(' ')
                    if not ok:
                        count += 1
                else:
                    num = ''
                    for index in range(len(i)):
                        if i[index] >= '0' and i[index] <= '9':
                            num += i[index]
                        elif len(num) > 0:
                            self.session_number = num
                            break
                    session_info = i.replace(num, '').replace('.', '').replace('、', '').replace(" ", '')
                    '''找到对应的日夜内外的文字信息，删除对应的段，最后留下的极为场景地点'''
                    for time in Global_Variables.time.keys():
                        if time in session_info:
                            self.session_time = time
                            session_info = session_info.replace(time, '')
                            break
                    for place in Global_Variables.place.keys():
                        if place in session_info:
                            self.session_place = place
                            session_info = session_info.replace(place, "")
                    self.session_location = session_info
                    count += 1
        for name, word in self.session_emotion_words_dic.items():
            self.session_emotion_words_set_dic[name] = set(word)
            # self.show_info()

    def cal_words_amount(self, charactor_setting=''):
        '''
        计算角色的情感词数
        :param charactor: 默认计算全部角色在这个场的情感词数
                                      如果输入角色名，也可单独计算角色数并返回结果（功能未做）
        :return:
        '''
        if len(charactor_setting) == 0:
            for line in self.line_list:
                for charactor in line.other_character:
                    # print(charactor)
                    self.session_charactor_dic[charactor].appearance = True
                if line.type == 'talk':
                    self.session_all_charactor.append(line.who_said_no_cut)
                    if line.who_said in Global_Variables.name_list:
                        said_word = line.content
                        self.session_charactor_dic[line.who_said].appearance = True
                        self.session_charactor_dic[line.who_said].charactor_worlds.append(said_word)
                        cut_said_word = jieba.cut(said_word)
                        for word in cut_said_word:
                            for name, words in Global_Variables.word_list_dic.items():
                                if word in words:
                                    self.session_charactor_dic[line.who_said].charactor_emotion_dic[name].append(word)
                                    # print(self.session_charactor_dic[line.who_said].charactor_emotion_dic)
                        for i in Global_Variables.punctuation_mark:
                            said_word = said_word.replace(i, '')  # 去除标点符号
                        self.session_charactor_dic[line.who_said].charactor_world_amount += len(said_word)
            for v in self.session_charactor_dic.values():
                self.session_words_amount += v.charactor_world_amount
            self.session_all_charactor_set = set(self.session_all_charactor)

    def cal_main_content(self):
        repeat_character=False
        for line in self.line_list:
            if line.type=='event':
                line_cut=jieba.cut(line.content)
                for word in line_cut:
                    if word in  Global_Variables.name_list and not repeat_character:
                        self.session_main_content+=word
                        repeat_character=True
                    elif word in line.verb:
                        self.session_main_content+=word
                        repeat_character=False
        for word in Global_Variables.stop_word:
            self.session_main_content=self.session_main_content.replace(word,'')
        # for k,v in Global_Variables.word_list_dic.items():
        #     for word in v:
        #         self.session_main_content=self.session_main_content.replace(word,'')

    def show_info(self, show_line_detail=0):
        '''
        :param show_line_detail: 1为显示行具体信息，0为只显示场的信息
        '''
        print('场次编号:' + str(self.session_number))
        print('场次时间:' + str(self.session_time))
        print('室内室外:' + str(self.session_place))
        print('场景地点:' + str(self.session_location))
        print('场景台词数:' + str(self.session_words_amount))
        print('场景情感值:' + str(self.session_emotion_value))
        print('主要内容:'+str(self.session_main_content))
        for Charactor in self.session_charactor_dic.values():
            if len(Charactor.charactor_worlds)>0:
                print(Charactor.name+','+str(Charactor.charactor_worlds))
            for key,values in Charactor.charactor_emotion_dic.items():
                if len(values)>0:
                    print(key+str(values))

        if show_line_detail == 1:
            for line in self.line_list:
                line.showInfo()


if __name__ == "__main__":
    a = open('test.txt', encoding='utf-8').read()
    a = Session(a, mode=1)
    a.show_info()
