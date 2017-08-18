user_dic_file_name="user_dic.txt"
sensitive_word_file="sensitive_words.txt"
def read_user_dic():
    file=open(user_dic_file_name,encoding="utf8").read().split("\n")
    for i in range(len(file)):
        file[i]=file[i].replace("\ufeff","")
    return file

def read_sensitive_word():
    file=open(sensitive_word_file,encoding="utf8").read().split("\n")
    sensitive_dic={}
    for line in file:
        if len(line.split(' '))<2:
            continue
        word_type,word=line.split(" ")
        sensitive_dic.setdefault(word_type,[])
        sensitive_dic[word_type].append(word)
    return sensitive_dic
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


word_list =read_user_dic()
print(word_list)
name_list = []
filename = 'name_bai.txt'
puncutation_file = 'punctuation_mark.txt'
stopword_file='stop_words.txt'
time = ['日', '晚上', '昼', '夜', '晨', '凌晨', '清晨', '早晨', '上午', '中午', '正午', '下午',
        '昏', '傍晚', '佛晓', '黎明', '日出', '日落']
place = ['外', '内', '室内', '室外', '户内', '户外']
out_place=['外', '室外','户外']
in_place=['内','室内','户内']
sensitive_word=read_sensitive_word()
# ad_word=
stop_word=set(open(stopword_file,encoding='utf-8').read().split('\n'))
punctuation_mark = set(open(puncutation_file, encoding='utf-8').read().split('\n'))