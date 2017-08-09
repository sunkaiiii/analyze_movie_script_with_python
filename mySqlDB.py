import MySQLdb

"""
----------mySqlDB.py-------------
处理数据库增、删、改、查的请求
"""
db = MySQLdb.connect(host='192.168.1.130', user='root', password='root', db='fbt', port=3306)
db.set_character_set('utf8')  # 不设置这个读取和插入中文时会乱码


def write_script_role_info(args):
    c = db.cursor()
    sql = """insert into script_role(name,number,gender,age,career,constellation,temperament,introduction,script_id,lines_amount,number_of_appearances) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_script_detail_info(args):
    c = db.cursor()
    sql = """insert into script_detail(script_id,script_number,content, role, period, scene, surroundings, role_number) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_participle_info(args):
    c = db.cursor()
    sql = """insert into participle(word,screenings,version) values(%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_lib_session_emotionword(args):
    c = db.cursor()
    sql = """insert into lib_session_emotionword(word,word_type,who,script_id,script_number) values(%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_sequence_scene_detail(args):
    '''写入顺景表详情库'''
    c = db.cursor()
    sql = """insert into sequence_scene_detail(scene,script_number,page_number,content) values(%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_sequence_screenings_detail(args):
    '''写入顺场表详情库'''
    c = db.cursor()
    sql = """insert into sequence_screenings_detail(surrounding,scene,script_number,page_number,content) values(%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def get_script_role_id(args):
    c = db.cursor()
    sql = """select id from script_role where name='""" + args + '\''
    c.execute(sql)
    result = c.fetchone()
    c.close()
    return result[0]


def read_lib_thesaurus(type=''):
    if type == '':
        sql = """select word,type_cn from lib_thesaurus"""
    else:
        sql = """select word,type_cn from lib_thesaurus where type_cn='""" + type + '\''
    c = db.cursor()
    c.execute(sql)
    result = c.fetchall()
    c.close()
    return result


if __name__ == "__main__":
    # print(read_lib_thesaurus())
    write_script_detail_info([('14', '1412sdfdsfs', '123|1234', '1', '内', '2', '3')])
