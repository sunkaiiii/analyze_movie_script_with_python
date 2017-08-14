import MySQLdb

"""
----------mySqlDB.py-------------
处理数据库增、删、改、查的请求
"""
# db = MySQLdb.connect(host='192.168.1.130', user='root', password='root', db='fbt', port=3306)
db = MySQLdb.connect(host='127.0.0.1', user='root', db='fbt', port=3306)
db.set_character_set('utf8')  # 不设置这个读取和插入中文时会乱码


def write_script(args):
    c = db.cursor()
    sql = """insert into script(script_name,type,word_count,screenings,version,project_id) values(%s,%s,%s,%s,%s,%s)"""
    c.execute(sql, args)
    db.commit()
    c.close()


def write_script_role_info(args):
    c = db.cursor()
    sql = """insert into script_role(name,number,gender,age,career,constellation,temperament,introduction,script_id,lines_amount,number_of_appearances) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_script_detail_info(args):
    c = db.cursor()
    sql = """insert into script_detail(script_id,screenings,role_id,content, role, period, scene, surroundings, role_number) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_participle_info(args):
    c = db.cursor()
    sql = """insert into participle(word,screenings,script_id,emotion_type,count) values(%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_lib_session_emotionword(args):
    c = db.cursor()
    sql = """insert into lib_session_emotionword(word,emotion_type,who,script_id,screenings) values(%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_sequence_scene(args):
    c = db.cursor()
    sql = """insert into sequence_scene(project_id,script_id,screenings,page_number,version,type,url) values(%s,%s,%s,%s,%s,%s,%s)"""
    c.execute(sql, args)
    db.commit()
    c.close()


def write_sequence_screenings(args):
    c = db.cursor()
    sql = """insert into sequence_screenings(project_id,script_id,screenings,page_number,version,type,url) values(%s,%s,%s,%s,%s,%s,%s)"""
    c.execute(sql, args)
    db.commit()
    c.close()


def write_sequence_scene_detail(args):
    '''写入顺景表详情库'''
    c = db.cursor()
    sql = """insert into sequence_scene_detail(scene,screenings,page_number,content,main_role,sequence_scene_id) values(%s,%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_sequence_screenings_detail(args):
    '''写入顺场表详情库'''
    c = db.cursor()
    sql = """insert into sequence_screenings_detail(surrounding,scene,time,screenings,page_number,content,main_role,sequence_screenings_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_session_ad_words(args):
    c = db.cursor()
    sql = """insert into session_ad_words(screnning,word,count,script_id) values(%s,%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def write_implanted_ad(args):
    c = db.cursor()
    sql = """insert into implanted_ad(ad_id,appearances,script_id) values(%s,%s,%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def upadte_sequence_scene(args):
    c = db.cursor()
    sql = """update  sequence_scene set sequence_screenings_id=(select id from sequence_screenings where script_id=%s LIMIT 1) where script_id=%s"""
    c.execute(sql, args)
    db.commit()
    c.close()


def update_sequence_screenings(args):
    c = db.cursor()
    sql = """update sequence_screenings set sequence_scene_id=(select id from sequence_scene where script_id=%s LIMIT 1) where script_id=%s"""
    c.execute(sql, args)
    db.commit()
    c.close()


def get_script_role_id(args):
    c = db.cursor()
    sql = """select id from script_role where name='""" + args + '\''
    c.execute(sql)
    result = c.fetchone()
    c.close()
    if result is None:
        return -1
    return int(result[0])


def get_project_id(args):
    c = db.cursor()
    sql = """select id from project where project_name=%s"""
    c.execute(sql, args)
    result = c.fetchone()
    c.close()
    return result[0]


def get_script_id(args):
    c = db.cursor()
    sql = """select id from script where version=%s"""
    c.execute(sql, args)
    result = c.fetchone()
    c.close()
    return result[0]


def get_sequence_scene_id(args):
    c = db.cursor()
    sql = """select id from sequence_scene where script_id=%s"""
    c.execute(sql, args)
    result = c.fetchone()
    c.close()
    return result[0]


def get_sequence_screenings_id(args):
    c = db.cursor()
    sql = """select id from sequence_screenings where script_id=%s"""
    c.execute(sql, args)
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


def read_lib_ad():
    sql = """select id,key_words from lib_ad_key_words"""
    c = db.cursor()
    c.execute(sql)
    result = c.fetchall()
    c.close()
    return result


def read_sensitive_words():
    sql = """select sensitive_word from sensitive_word"""
    c = db.cursor()
    c.execute(sql)
    result = c.fetchall()
    c.close()
    return result


def insert_ad_words(args):
    c = db.cursor()
    sql = """insert into lib_ad_key_words(key_words) values(%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


def insert_sensitive_words(args):
    c = db.cursor()
    sql = """insert into sensitive_word(sensitive_word) values(%s)"""
    c.executemany(sql, args)
    db.commit()
    c.close()


if __name__ == "__main__":
    result = read_lib_ad()
    for word in result:
        print(word[0])
