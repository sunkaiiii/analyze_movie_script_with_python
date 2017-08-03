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


word_list_dic = save_userdic_to_file()
# print(word_list_dic)
name_list = []
filename = 'name_bai.txt'
puncutation_file = 'punctuation_mark.txt'
time = {'日':1, '晚上':2, '昼':3, '夜':4, '晨':5, '凌晨':6, '清晨':7, '早晨':8, '上午':9, '中午':10, '正午':11, '下午':12, '昏':13, '傍晚':14, '佛晓':15, '黎明':16, '日出':17, '日落':18}
place = {'外':1, '内':2}
session_info_title = ['场次序号', '地点', '时间', '场景', '主要人物', '主要人物感情色彩']
# file = open(filename, 'r', encoding='utf-8').read().split('\n')
# for i in file:
#     name_list.append(i.split(' ')[0].strip('\ufeff').strip(' '))
punctuation_mark = set(open(puncutation_file, encoding='utf-8').read().split('\n'))
