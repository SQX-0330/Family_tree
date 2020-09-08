import sqlite3


# 插入个人信息
def insert_zi(name, sex, birthday, father, partner, alive, cid):
    """

    :param name: 姓名
    :param sex: 性别
    :param birthday: 出生日期
    :param father: name所指人的父亲
    :param partner: name所指人的伴侣
    :param alive: name所指人是否健在
    :param cid: name所指人的层级编号
    :return: 没有返回值
    """

    try:
        conn = sqlite3.connect("tree")
        curs = conn.cursor()
        s2 = "insert into information (name, sex, birthday, father, partner, alive, cid) " \
             "values('%s','%s','%s','%s','%s','%s','%s')" % (name, sex, birthday, father, partner, alive, cid)
        curs.execute(s2)
        conn.commit()
        return True
    except:
        conn.rollback()
        print("插入出错，已回滚")
        return False
    finally:
        curs.close()
        conn.close()


# 查询家族所有人员的信息
def select_all():
    """
    查询家族内所有成员信息，包括：
    姓名    性别    出生日期    父亲    伴侣  健在   层次编号
    :return: 返回一个包含所有人信息的字符串，
             因为在界面上输出，使用字符串输出
    """
    x = "   姓名\t性别\t出生日期\t父亲\t伴侣\t健在\t层级编号\n"
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    s2 = "select * from information"
    s = curs.execute(s2)
    for i in s:
        x += str(i) + "\n"
    conn.commit()
    curs.close()
    conn.close()
    return x


# 查询个人基本信息
def select_person(name):
    """
    查询指定姓名的人的详细信息，包括：
    姓名    性别    出生日期    父亲    伴侣  健在   层次编号
    :param name: 所要查询的人的姓名
    :return:返回包含个人信息的字符串
    """
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    all_information = "select * from information where name='%s'" % name
    result = curs.execute(all_information)
    conn.commit()
    for i in result:
        information = str(i)
    curs.close()
    conn.close()
    return information


# 查询儿子姓名
def select_son_name(father):

    """
    查找指定姓名人的儿子的姓名

    :param father:指定姓名
    :return: 返回其包含其所有儿子姓名的列表
    """
    list_son = []
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    all_information = "select name from information where father='%s'" % father
    result = curs.execute(all_information)
    for i in result:
        for j in i:
            name = str(j)
            list_son.append(name)
    conn.commit()
    curs.close()
    conn.close()
    return list_son


# 修改个人信息（伴侣的信息）
def update_person_partner(name, partner):
    """
    通过指定人的姓名修改其伴侣信息
    :param name: 指定姓名
    :param partner: 新伴侣的姓名
    :return: 无返回值
    """
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    update_sql = "update information set partner='%s' where name = '%s'" % (partner, name)
    curs.execute(update_sql)
    conn.commit()
    curs.close()
    conn.close()


# 修改个人信息（是否健在的信息）
def update_person_alive(name, alive):
    """
    通过指定人的姓名修改其是否健在
    :param name: 指定姓名
    :param alive: 健在状态信息
    :return: 无返回值
    """
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    update_sql = "update information set alive='%s' where name = '%s'" % (alive, name)
    curs.execute(update_sql)
    conn.commit()
    curs.close()
    conn.close()


# 查询指定姓名的层级编号
def select_person_cid(name):
    """
    查询指定姓名人的层级编号
    :param name:指定姓名
    :return: 返回所查询的层级编号
    """

    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    select_sql = "select cid from information where name='%s'" % name
    curs.execute(select_sql)
    cid = curs.fetchall()
    for i in cid:
        for j in i:
            if type(j) != str:
                new_cid = str(j)
            else:
                new_cid = j
    conn.commit()
    curs.close()
    conn.close()
    return new_cid


# 查询性别
def select_sex(name):
    """
    查询指定姓名人的性别
    :param name: 指定姓名
    :return: 返回指定姓名的人的性别
    """
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    select_sql = "select sex from information where name='%s'" % name
    curs.execute(select_sql)
    cid = curs.fetchall()
    for i in cid:
        for j in i:
            if type(j) != str:
                sex = str(j)
            else:
                sex = j
    conn.commit()
    curs.close()
    conn.close()
    return sex


# 查询姓名是否已插入
def select_name_insert(name):
    """
    查询指定的姓名是否在数据库中已存在
    :param name: 要插入的姓名
    :return: 已存在返回True----->不可再插入
             不存在返回None------>可插入
    """
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    try:

        all_information = "select * from information where name='%s'" % name
        result = curs.execute(all_information)
        conn.commit()
        for i in result:
            if not None:
                return True
            else:
                return None
    except:
        conn.rollback()
        print("出错")
    finally:
        curs.close()
        conn.close()


# 通过cid查询信息
def select_cid(cid):
    """
    通过层级编号查询所有的信息
    :param cid: 层级编号
    :return: 返回包含所有信息的列表
    """

    list_all = []
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    select_sql = "select * from information where cid='%s'" % cid
    s = curs.execute(select_sql)
    conn.commit()
    for i in s:
        list_all.append(i)
    curs.close()
    conn.close()
    return list_all


# # 清除数据库数据
# def clear_db():
#     """
#     清空数据库表中的所有数据
#     :return: 无返回值
#     """
#     conn = sqlite3.connect("tree")
#     curs = conn.cursor()
#     select_sql = "delete from information"
#     curs.execute(select_sql)
#     conn.commit()
#     curs.close()
#     conn.close()


# 查询父亲名字
def select_father(name):
    """
    查询指定姓名的人的父亲姓名
    :param name: 指定的姓名
    :return: 返回指定人的父亲的姓名
    """
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    select_sql = "select father from information where name='%s'" % name
    result = curs.execute(select_sql)
    conn.commit()
    for i in result:
        for j in i:
            father = str(j)
    curs.close()
    conn.close()
    return father


# 查询伴侣
def select_partner(name):

    """
    查询指定姓名的人的伴侣信息
    :param name: 指定的姓名
    :return: 返回伴侣的姓名
    """
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    select_sql = "select partner from information where name='%s'" % name
    result = curs.execute(select_sql)
    conn.commit()
    for i in result:
        for j in i:
            partner = str(j)
    curs.close()
    conn.close()
    return partner


# 查询同代人
def select_brother(cid):
    """
    通过层级编号查询同辈的人
    :param cid: 层级编号
    :return: 返回同辈所有人的姓名的列表
    """
    list_brother = []
    conn = sqlite3.connect("tree")
    curs = conn.cursor()
    select_sql = "select name from information where cid like '%s'" % cid
    result = curs.execute(select_sql)
    conn.commit()
    for i in result:
        for j in i:
            list_brother.append(str(j))
    curs.close()
    conn.close()
    return list_brother

# 查询通过cid查询名字
def select_name_form_cid(cid):
    """
    查询指定cid的人的姓名
    :param name: 指定的姓名
    :return: 返回指定人的姓名
    """
    try:
        conn = sqlite3.connect("tree")
        curs = conn.cursor()
        select_sql = "select name from information where cid='%s'" % cid
        result = curs.execute(select_sql)
        conn.commit()
        for i in result:
            if i is None:
                return None
            else:

                for j in i:
                    name = str(j)
            return name
    except:
        conn.rollback()
        return None
    finally:
        curs.close()
        conn.close()


# 删除子节点
def delete_son_node(cid):
    """
    :param cid:子节点的cid号  包含通配符%
    :return: 返回是否删除成功
    """
    try:
        conn = sqlite3.connect("tree")
        curs = conn.cursor()
        select_sql = "delete  from information where cid like '%s'" % cid
        curs.execute(select_sql)
        conn.commit()
        return True
    except:
        conn.rollback()
        return None
    finally:
        curs.close()
        conn.close()

# person = ('张三', '男', '1960-1-1', None, '吴霜', 'no', '1')
# person_son = ('张二', '男', '1985-1-1', '张三', '柳筱筱', 'yes', '11')
# person_son1 = ('张小二', '男', '2007-1-1', '张二', '王婉', 'yes', '111')
# insert_zi(*person_son)
#
# insert_zi(*person)
# insert_zi(*person_son1)











