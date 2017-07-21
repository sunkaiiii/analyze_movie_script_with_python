

a={}
a['asd']=1
if a.setdefault('asd',0)==0:
    print(a)

a['asd']+=1
print(a)