# coding=utf-8
import jieba
import jieba.posseg as pseg
import Global_Variables

jieba.load_userdict('user_dic.txt')

'''
----------line.py------------
读取的剧本的一行的内容
'''


class Line():
    def __init__(self, line_str, mode=1):
        self.mode = mode
        self.who_said = ''
        self.emotion = 0
        self.positive = []
        self.nagetive = []
        self.emotion_word_dic = {}
        self.content = ''
        self.type = ''
        self.noun = []
        self.verb = []
        self.other_character = []
        self.who_said_no_cut = ""
        if ':' in line_str or '：' in line_str:  # 当有冒号时，认为是一个对话
            self.type = 'talk'
            line_str = line_str.replace('：', ':')
            name = line_str.split(':')[0]
            self.who_said_no_cut = name  # 当剧本不完全是XX:的形式而是带有定语或者别的词的时候，再进行一次切割
            name_words = pseg.cut(name)
            for word in name_words:
                for name in Global_Variables.word_list_dic.keys():
                    self.emotion_word_dic.setdefault(name, [])
                    if word.word in Global_Variables.word_list_dic[name]:
                        # print(name, word.word)
                        self.emotion_word_dic[name].append(word.word)
                '''
                以下为即将废除的代码
                '''
                ##############
                if word.word in Global_Variables.name_list:
                    self.who_said = word.word
                elif word.word in Global_Variables.negative_words:
                    self.nagetive.append(word.word)
                elif word.word in Global_Variables.positive_words:
                    self.positive.append(word.word)
                ################
                if "n" in word.flag:
                    self.noun.append(word.word)
                elif 'v' in word.flag:
                    self.verb.append(word.word)
            self.content = line_str.replace(line_str.split(':')[0] + ':', "")
            # self.content = line_str.strip(name + ':')
            # print(self.content)
        else:
            self.type = 'event'
            self.content = line_str
        cut_words = pseg.cut(self.content)
        for cut_word in cut_words:
            for name in Global_Variables.word_list_dic.keys():
                self.emotion_word_dic.setdefault(name, [])
                if cut_word.word in Global_Variables.word_list_dic[name]:
                    # print(name, cut_word.word)
                    self.emotion_word_dic[name].append(cut_word.word)
            '''
            以下为即将废除的代码
            '''
            ##############
            if cut_word.word in Global_Variables.negative_words:
                self.nagetive.append(cut_word.word)
            if cut_word.word in Global_Variables.positive_words:
                self.positive.append(cut_word.word)
            ################
            if cut_word.word in Global_Variables.name_list:
                self.other_character.append(cut_word.word)
            elif "n" in cut_word.flag:
                self.noun.append(cut_word.word)
            elif 'v' in cut_word.flag:
                self.verb.append(cut_word.word)

    def showInfo(self):
        if self.type == 'talk':
            print(self.who_said + ':' + self.content)
        else:
            print(self.content)
        print('positive:' + str(self.positive))
        print('negative:' + str(self.nagetive))
        print('noun' + str(self.noun))
        print('verb' + str(self.verb))
        print('other_chracter' + str(self.other_character))


if __name__ == "__main__":
    a = 1
    test = Line('可他这是杀鸡给猴看！打狗还得看主人呢! 明明知道我是您的团练教头他还敢打！ 黄四郎:那，你就让他打了？')
    test.showInfo()
