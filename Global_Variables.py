import mySqlDB


def save_userdic_to_file():
    user_dic = mySqlDB.read_lib_thesaurus()
    user_dic_str = ""
    for word in user_dic:
        # print(word)
        user_dic_str += word[0] + ' ' + '1000' + '\n'
    f = open('user_dic.txt', 'w', encoding='utf8')
    f.write(user_dic_str)
    f.close()
    user_dic_convert = convert_userdic(user_dic)
    return user_dic_convert


def convert_userdic(user_dic):
    user_dic_convert = {}
    for section in user_dic:
        # print(section)
        key = section[1].replace(' ', '').replace('\u3000', '')
        user_dic_convert.setdefault(key, [])
        user_dic_convert[key].append(section[0].replace('\u3000', ''))
    # count=0
    # for k,v in user_dic_convert.items():
        # count+=len(v)
        # print(k,v)
    # print(count)
    return user_dic_convert


word_list = save_userdic_to_file()
name_list = []
filename = 'name_bai.txt'
emotion_path = 'emotion\\'
pos_file_name = 'pos.txt'
neg_file_name = 'neg.txt'
puncutation_file = 'punctuation_mark.txt'
time = ['日', '晚上', '昼', '夜', '晨', '凌晨', '清晨', '早晨', '上午', '中午', '正午', '下午', '昏', '傍晚', '佛晓', '黎明', '日出', '日落']
place = ['外', '内']
session_info_title = ['场次序号', '地点', '时间', '场景', '主要人物', '主要人物感情色彩']
file = open(filename, 'r', encoding='utf-8').read().split('\n')
for i in file:
    name_list.append(i.split(' ')[0].strip('\ufeff').strip(' '))
positive_words = set(open(emotion_path + pos_file_name, encoding='utf-8').read().split('\n'))
negative_words = set(open(emotion_path + neg_file_name, encoding='utf-8').read().split('\n'))
punctuation_mark = set(open(puncutation_file, encoding='utf-8').read().split('\n'))
