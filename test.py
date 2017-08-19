file=open("ad.txt",encoding="utf8").read().split('\n')
ad_dic={}
for word in file:
    word=word.split("|")
    if(len(word)>=1):
        for w in word:
            ad_dic.setdefault(w.replace("\ufeff",""),0)
            ad_dic[w.replace("\ufeff","")]+=1
ad_dic=sorted(ad_dic.items(),key=lambda x:x[1],reverse=True)
print(ad_dic)
words=""
for word in ad_dic:
    if(word[1]>0):
        words+=word[0]+'\n'
f=open("ad1.txt",'w',encoding="utf8")
f.write(words)
f.close()