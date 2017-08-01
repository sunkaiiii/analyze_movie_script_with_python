# coding=utf-8
import line
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy as sp
import Global_Variables
import jieba

"""
------------session.py--------------
记录一个场次的内容，里面包含多个行的Line类实体
"""

clf = joblib.load('emotion_model.model')
count_vec = TfidfVectorizer(binary=False, decode_error='ignore')
x_train = sp.load('train_data.npy')


class Charactor():
    '''
    记录一个场当中演员的信息的类
    '''

    def __init__(self, name=""):
        self.name = name
        self.charactor_worlds = []
        self.charactor_world_amount = 0
        self.charactor_positive_emotion = []
        self.charactor_nagetive_emotion = []
        self.charactor_emotion = []
        self.appearance = False  # 是否在这个场景出现
        self.charactor_value = 0


class Session():
    def __init__(self, session_content, mode=1):
        '''
        :param session_content: 切割好的一场的所有内容
        :param mode: 0、读取场次内容的顺序为场景位置、时间、内外
                                1、读取场次你内容的顺序为时间，内外，场景位置
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
        self.session_positive_words = []
        self.session_negative_words = []
        self.session_emotion_words = []
        self.session_positive_words_set = ()
        self.session_negative_words_set = ()
        self.session_emotion_words_set = ()
        self.session_positive_value = ''
        self.session_negative_value = ''
        self.session_emotion_value = ''
        self.session_content = session_content
        self.session_words_amount = 0
        self.session_charactor_dic = {}
        for i in Global_Variables.name_list:  # 使用字典存放场景角色的信息
            self.session_charactor_dic[i] = Charactor(i)
        self.session_all_charactor = []  # 存放未切割的对话人物，可用于寻找主要角色（人工或继续分词）
        self.session_all_charactor_set = set()
        self.read_session_lines()
        self.cal_words_amount()
        self.compare_emotion()

    def read_session_lines(self):
        count = 0
        for i in self.session_content.split('\n'):
            if len(str(i).strip('\n').strip(' ')) == 0:
                continue
            if count != 0:
                session_line = line.Line(i, self.mode)
                self.line_list.append(session_line)
                self.session_positive_words.extend(session_line.positive)
                self.session_negative_words.extend(session_line.nagetive)
                self.session_emotion_words.extend(session_line.positive)
                self.session_emotion_words.extend(session_line.nagetive)
            else:
                if self.mode == 0:
                    session_info = i.strip(' ')
                    session_info = session_info.replace('：', ':')
                    session_info = session_info.split(':')
                    ok = False
                    for index in range(0, len(Global_Variables.session_info_title)):
                        if session_info[0].strip('\ufeff') in Global_Variables.session_info_title[index]:
                            ok = True
                            if index == 0:
                                self.session_number = session_info[1].strip('.').strip('、').strip(' ').strip('\ufeff')
                            elif index == 1:
                                self.session_location = session_info[1].strip(' ')
                            elif index == 2:
                                self.session_place = session_info[1].strip(' ')
                            elif index == 3:
                                self.session_time = session_info[1].strip(' ')
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
                    for time in Global_Variables.time:
                        if time in session_info:
                            self.session_time=time
                            session_info=session_info.replace(time,'')
                            break
                    for place in Global_Variables.place:
                        if place in session_info:
                            self.session_place=place
                            session_info=session_info.replace(place,"")
                    self.session_location=session_info
                    count += 1
        self.session_positive_words_set = set(self.session_positive_words)
        self.session_negative_words_set = set(self.session_negative_words)
        self.session_emotion_words_set = set(self.session_emotion_words)
        # self.show_info()

    def cal_words_amount(self, charactor=''):
        '''
        计算角色的情感词数
        :param charactor: 默认计算全部角色在这个场的情感词数
                                      如果输入角色名，也可单独计算角色数并返回结果（功能未做）
        :return:
        '''
        if len(charactor) == 0:
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
                            if word in Global_Variables.positive_words:
                                self.session_charactor_dic[line.who_said].charactor_positive_emotion.append(word)
                                self.session_charactor_dic[line.who_said].charactor_emotion.append(word)
                            if word in Global_Variables.negative_words:
                                self.session_charactor_dic[line.who_said].charactor_nagetive_emotion.append(word)
                                self.session_charactor_dic[line.who_said].charactor_emotion.append(word)
                        for i in Global_Variables.punctuation_mark:
                            said_word = said_word.replace(i, '')  # 去除标点符号
                        self.session_charactor_dic[line.who_said].charactor_world_amount += len(said_word)
            for v in self.session_charactor_dic.values():
                self.session_words_amount += v.charactor_world_amount
            self.session_all_charactor_set = set(self.session_all_charactor)

    def compare_emotion(self):
        value = float(len(self.session_positive_words)) ** 1.75 * 2.55
        self.session_positive_value = value
        value = float(len(self.session_negative_words)) ** 1.75 * 2.55
        self.session_negative_value = value
        value = self.session_positive_value - self.session_negative_value
        self.session_emotion_value = value

        '''角色情感用类似的方法'''
        for name, charactor in self.session_charactor_dic.items():
            value = len(charactor.charactor_positive_emotion) ** 1.75 * 2.55 - len(
                charactor.charactor_nagetive_emotion) ** 1.75 * 2.55
            self.session_charactor_dic[name].charactor_value = value

    def show_info(self, show_line_detail=0):
        '''
        :param show_line_detail: 1为显示行具体信息，0为只显示场的信息
        '''
        print('场次编号:' + str(self.session_number))
        print('场次时间:' + str(self.session_time))
        print('室内室外:' + str(self.session_place))
        print('场景地点:' + str(self.session_location))
        print('场景积极词:' + str(self.session_positive_words_set))
        print('场景消极词:' + str(self.session_negative_words_set))
        print('场景全部情感词:' + str(self.session_emotion_words_set))
        print('场景台词数:' + str(self.session_words_amount))
        print('场景情感值:' + str(self.session_emotion_value))
        if show_line_detail == 1:
            for line in self.line_list:
                line.showInfo()


if __name__ == "__main__":
    a = open('test.txt', encoding='utf-8').read()
    a = Session(a, mode=1)
    a.show_info()
