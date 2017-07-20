import jieba
import jieba.posseg as pseg
import Global_Variables
jieba.load_userdict('name.txt')

file=open('name.txt','r',encoding='utf-8')
for name in file.readlines():
    Global_Variables.name_list.append(name.split(' ')[0].strip('\ufeff'))
# print(name_list)
class Line():
    who_said=''
    emotion=0
    positive=[]
    nagetive=[]
    content=''
    type=''
    noun=[]
    verb=[]
    other_character=[]
    def __init__(self,line_str):
        if ':' in line_str:
            self.type='talk'
            name=line_str.split(':')[0]
            if name in Global_Variables.name_list:
                self.who_said=name
                self.content=line_str.strip(name+':')
        else:
            self.type='event'
            self.content=line_str
        cut_words=pseg.cut(self.content)
        for cut_word in cut_words:
            if cut_word.word in Global_Variables.negative_words:
                self.nagetive.append(cut_word.word)
            if cut_word.word in Global_Variables.positive_words:
                self.positive.append(cut_word.word)
            if cut_word.word in Global_Variables.name_list:
                self.other_character.append(cut_word.word)
            elif "n" in cut_word.flag:
                self.noun.append(cut_word.word)
            elif 'v' in cut_word.flag:
                self.verb.append(cut_word.word)

    def showInfo(self):
        print(self.who_said+':'+self.content)
        print('positive:'+str(self.positive))
        print('negative:'+str(self.nagetive))
        print('noun'+str(self.noun))
        print('verb'+str(self.verb))
        print('other_chracter'+str(self.other_character))
if __name__=="__main__":
    a=1
    test=Line('张牧之:老汤你就好好给我看好了')
    test.showInfo()