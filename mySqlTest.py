import  MySQLdb
db=MySQLdb.connect(host='localhost',user='root',password='',db='heritage',port=3306)
db.set_character_set('utf8')
c=db.cursor()
# c.execute('insert into test(name) values(\'大伯\')')
# db.commit()
c.execute("""select * from test""")
r=c.fetchall()
c.close()
# r=c.fetchone()
for i in r:
    if type(i)=='bytes':
        print(i.encode('utf-8'))
    print(i)