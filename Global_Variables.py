name_list=[]
emotion_path='emotion\\'
pos_file_name='pos.txt'
neg_file_name='neg.txt'
positive_words=open(emotion_path+pos_file_name,encoding='utf-8').read().split('\n')
negative_words=open(emotion_path+neg_file_name,encoding='utf-8').read().split('\n')
# print(positive_words)