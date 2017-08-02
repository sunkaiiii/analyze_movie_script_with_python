import  MySQLdb
db=MySQLdb.connect(host='192.168.1.130',user='root',password='root',db='fbt',port=3306)
db.set_character_set('utf8')

def write_script_role_info(args):
    c=db.cursor()
    sql="""insert into script_role(name,lines_amount,number_of_appearances) values (%s,%s,%s)"""
    c.executemany(sql,args)
    db.commit()
    c.close()
def get_script_role_id(args):
    c=db.cursor()
    sql="""select id from script_role where name='"""+args+'\''
    c.execute(sql)
    result=c.fetchone()
    c.close()
    return result[0]

def read_lib_thesaurus(type=''):
    if type=='':
        sql="""select word,type_cn from lib_thesaurus"""
    else:
        sql="""select word,type_cn from lib_thesaurus where type_cn='"""+type+'\''
    c=db.cursor()
    c.execute(sql)
    result=c.fetchall()
    c.close()
    return result



if __name__=="__main__":
    print(read_lib_thesaurus())