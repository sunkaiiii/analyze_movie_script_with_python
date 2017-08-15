# coding=utf-8
import jieba
import jieba.posseg as pseg
import Global_Variables

jieba.load_userdict('user_dic.txt')
for word in Global_Variables.name_list:
    jieba.add_word(word,10000)
for word in Global_Variables.ad_word.keys():
    jieba.add_word(word,1000)
for key,words in Global_Variables.sensitive_word.items():
    for word in words:
        jieba.add_word(word,1000)

'''
----------line.py------------
读取的剧本的一行的内容
'''


class Line():
    def __init__(self, line_str, mode=1):
        self.mode = mode
        self.who_said = ''
        self.emotion = 0
        self.emotion_word_dic = {}
        self.content = ''
        self.type = ''
        self.noun = []
        self.verb = []
        self.other_character = []
        self.sensitive_word={}
        self.ad_word=[]
        self.who_said_no_cut = ""
        if ':' in line_str or '：' in line_str:  # 当有冒号时，认为是一个对话
            self.type = 'talk'
            line_str = line_str.replace('：', ':')
            name = line_str.split(':')[0]
            self.who_said_no_cut = name  # 当剧本不完全是XX:的形式而是带有定语或者别的词的时候，再进行一次切割
            name_words = pseg.cut(name)
            for word in name_words:
                if word.word in Global_Variables.name_list:
                    self.who_said=word.word
                    continue
                for word_name in Global_Variables.word_list_dic.keys():
                    self.emotion_word_dic.setdefault(word_name, [])
                    if word.word in Global_Variables.word_list_dic[word_name]:
                        self.emotion_word_dic[word_name].append(word.word)
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
            for key,words in Global_Variables.sensitive_word.items():
                if(cut_word.word in words):
                    self.sensitive_word.setdefault(key,[])
                    self.sensitive_word[key].append(cut_word.word)
            if cut_word.word in Global_Variables.ad_word.keys():
                self.ad_word.append(cut_word.word)
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
        print('noun' + str(self.noun))
        print('verb' + str(self.verb))
        print('other_chracter' + str(self.other_character))
        print("敏感词"+str(self.sensitive_word))


if __name__ == "__main__":
    a = 1
    test = Line('傻逼')
    test.showInfo()
