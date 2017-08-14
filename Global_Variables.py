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

def get_ad_word():
    words={}
    for word in mySqlDB.read_lib_ad():
        words.setdefault(word[1],word[0])
    return words

def get_sensitive_word():
    words=[]
    for word in mySqlDB.read_sensitive_words():
        words.append(word[0])
    return words
word_list_dic = save_userdic_to_file()  # 读取数据库的词库，并保存在本地供jieba分词学习（也可以保存在List中，用循环使用addword给jieba提供词库）
name_list = []
filename = 'name_bai.txt'
puncutation_file = 'punctuation_mark.txt'
stopword_file='stop_words.txt'
time = ['日', '晚上', '昼', '夜', '晨', '凌晨', '清晨', '早晨', '上午', '中午', '正午', '下午',
        '昏', '傍晚', '佛晓', '黎明', '日出', '日落']
place = ['外', '内', '室内', '室外', '户内', '户外']
out_place=['外', '室外','户外']
in_place=['内','室内','户内']
session_info_title = ['场次序号', '地点', '时间', '场景', '主要人物', '主要人物感情色彩','内容']
character_biographies = ['编号', '姓名', '性别', '角色', '年龄', '职业', '星座', '血型', '人物背景', '人物性格']
constellation = {'白羊座': 0, '金牛座': 1, '双子座': 2, '巨蟹座': 3, '狮子座': 4, '处女座': 5, '天秤座': 6, '天蝎座': 7, '射手座': 8, '摩羯座': 9,
                 '水瓶座': 10, '双鱼座': 11,
                 '白羊': 0, '金牛': 1, '双子': 2, '巨蟹': 3, '狮子': 4, '处女': 5, '天秤': 6, '天蝎': 7, '射手': 8, '摩羯': 9, '水瓶': 10,
                 '双鱼': 11}
blood = {'A型': 0, 'B型': 1, 'O型': 2, 'AB型': 3,
         'A': 0, 'B': 1, 'O': 2, 'AB': 3}
sensitive_word=get_sensitive_word()
ad_word=get_ad_word()
stop_word=set(open(stopword_file,encoding='utf-8').read().split('\n'))
punctuation_mark = set(open(puncutation_file, encoding='utf-8').read().split('\n'))