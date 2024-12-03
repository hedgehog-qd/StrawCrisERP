import pymysql
import config


def checklogin(user, pwd):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT passwd FROM users WHERE user_name="' + user + '"'
    cursor.execute(sql)
    a = cursor.fetchone()
    if a is None:
        print("用户不存在！")
        return 2
    else:
        if a[0] != pwd:
            print("密码错误！")
            return 1
        else:
            print("成功登录！")
            return 0


def getuserdata(user):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT uid, role FROM users WHERE user_name="' + user + '"'
    cursor.execute(sql)
    data = cursor.fetchone()
    return data[0], data[1]


def addUser(user_name, passwd, role):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = 'SELECT COUNT(*) FROM users WHERE user_name="' + user_name + '"'
    cursor.execute(sql)
    data = cursor.fetchone()[0]
    if data != 0:
        return 1  # User already exist
    cursor2 = db.cursor()
    sql2 = "INSERT INTO users SET user_name=\"" + user_name + "\", passwd=\"" + str(
        passwd) + "\", role=\"" + role + "\""
    cursor2.execute(sql2)
    db.commit()
    return 0  # Success


def deleteUser(uid):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "DELETE FROM users WHERE uid=" + str(uid)
    cursor.execute(sql)
    db.commit()


def getUserList():
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def updateUser(uid, user_name, passwd, role):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "UPDATE users SET user_name=\"" + user_name + "\", passwd=\"" + passwd + "\", role=\"" + role + "\" WHERE uid=" + str(
        uid)
    cursor.execute(sql)
    db.commit()


def getAllMaterials():
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "SELECT * FROM materials"
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def getInfoMetaSearch(search):  # search传入一个列表
    result = getAllMaterials()
    if len(search) == 0:
        return result  # 用户没有输入搜索内容，直接返回所有数据
    final_list = result
    for i in search:
        temp_list = []
        for item in final_list:
            str_i = str(i)
            if any(str_i in str(item[j]) for j in range(1, 12)):  # item[1] 到 item[11] 进行遍历
                temp_list.append(item)
        final_list = temp_list
    return final_list


def checkMaterialExists(mpn):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM materials WHERE mpn=\"" + str(mpn) + "\""
    cursor.execute(sql)
    data = cursor.fetchone()
    if data[0] != 0:
        return 1  # 已经存在
    else:
        return 0  # 不存在


def addNewMaterial(m_name, m_class, footprint, quantity, mpn, manufacture, spn, supplier, position, user_comment,
                   buy_time):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "INSERT INTO materials SET m_name=\"" + m_name + "\", m_class=\"" + m_class + "\", footprint=\"" + footprint + \
          "\", quantity=\"" + quantity + "\", mpn=\"" + mpn + "\", manufacture=\"" + manufacture + "\", spn=\"" + spn + \
          "\", supplier=\"" + supplier + "\", position=\"" + position + "\", user_comment=\"" + user_comment + \
          "\", buy_time=\"" + buy_time + "\" "
    cursor.execute(sql)
    db.commit()


def getMaterialInfowithMPN(mpn):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "SELECT * FROM materials WHERE mpn=\"" + mpn + "\""
    cursor.execute(sql)
    data = cursor.fetchone()
    return data


def updateMaterialQuantitywithMPN(mpn, quantity):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "UPDATE materials SET quantity=\"" + str(quantity) + "\" WHERE mpn=\"" + mpn + "\""
    cursor.execute(sql)
    db.commit()


def updateMaterialInfowithMPN(mpn, m_name, m_class, footprint, quantity, manufacture, spn, supplier, position,
                              user_comment, buy_time):
    db = pymysql.connect(host=config.db_host, port=config.db_port, user=config.db_user, password=config.db_passwd,
                         database=config.db_name, charset='utf8')
    print("successfully connected to the database!")
    cursor = db.cursor()
    sql = "UPDATE materials SET m_name=\"" + m_name + "\", m_class=\"" + m_class + "\", footprint=\"" + footprint + \
          "\", quantity=\"" + quantity + "\", manufacture=\"" + manufacture + "\", spn=\"" + spn + \
          "\", supplier=\"" + supplier + "\", position=\"" + position + "\", user_comment=\"" + user_comment + \
          "\", buy_time=\"" + buy_time + "\" WHERE mpn=\"" + str(mpn) + "\""
    cursor.execute(sql)
    db.commit()


def checkoutHaveList(have_list):
    for i in have_list:
        existing_num = getMaterialInfowithMPN(i[0])[4]
        updateMaterialQuantitywithMPN(i[0], int(existing_num) - int(i[2]))
    print("DONE")
