# -*-coding:utf-8-*-
import pymysql
from datetime import datetime

ifudan_host = '10.221.137.167'
dom_host = '192.168.1.4'
cloud_host = '123.206.132.235'

class Connection(object):
    def connect_database(self):
        self.connection = pymysql.connect(host=cloud_host,
                                          user='root',
                                          db='new_test',
                                          passwd='dbpj1008',
                                          port=4040,
                                          charset="utf8"
                                          )
        self.cursor = self.connection.cursor()

    def disconnect_database(self):
        self.cursor.close()
        self.connection.close()

    def exec_query(self, sql):
        self.cursor.execute(sql)

    def exec_update(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def fetch_cursor(self):
        return self.cursor.fetchall()

database = Connection()

#login functions:

def exec_staff_login(username, password):
    database.connect_database()
    sql = "SELECT staffacc.staff_id, staff_rank.staff_type FROM staffacc, staff_rank WHERE staffacc.staff_id = staff_rank.staff_id and staff_name='%s' AND staff_psw='%s'"
    data = (username, password)
    database.exec_query(sql % data)
    values = database.fetch_cursor()
    database.disconnect_database()

    if values:
        user_id = values[0][0]
        admin_type = values[0][1]
        return (True, user_id, admin_type)

    else:
        return (False, 0, 0)

def exec_customer_login(username, password):
    database.connect_database()
    sql = "SELECT mem_id FROM memberacc WHERE mem_name='%s' AND mem_psw='%s'"
    data = (username, password)
    database.exec_query(sql % data)
    values = database.fetch_cursor()
    database.disconnect_database()
    if values:
        return (True, values)
    else:
        return (False, 0)

def exec_supplier_login(username, password):
    database.connect_database()
    sql = "SELECT supp_id FROM supplieracc WHERE supp_name='%s' AND supp_psw='%s'"
    data = (username, password)
    database.exec_query(sql % data)
    values = database.fetch_cursor()
    database.disconnect_database()
    if values:
        return (True, values)
    else:
        return (False, 0)

#register functions:

def exec_register_customer(username, password, email):
    database.connect_database()

    sql = "SELECT * FROM memberacc WHERE mem_name='%s'"
    database.exec_query(sql % username)
    values = database.fetch_cursor()
    if values:  # if values is not empty, it indicates that username has been registered
        database.disconnect_database()
        return False
    else:
        time = str(datetime.now())  # insert a new customer
        sql = "INSERT INTO memberacc(mem_name, mem_psw, mem_mail, mem_regtime, mem_point) VALUES('%s','%s','%s','%s',0)"
        data = (username, password, email, time)
        database.exec_update(sql % data)
        database.disconnect_database()
        return True

def exec_add_a_new_supplier(supp_name, supp_psw, supp_contact, supp_phone, supp_mail, supp_addr, supp_note):
    database.connect_database()
    time = str(datetime.now())
    # add a new supplier
    sql = "INSERT INTO supplieracc(supp_name, supp_psw, supp_regtime, supp_contact, supp_phone, supp_mail, supp_addr, supp_note) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"
    data = (supp_name, supp_psw, time, supp_contact, supp_phone, supp_mail, supp_addr, supp_note)
    database.exec_update(sql % data)
    database.disconnect_database()

#fetch&show functions:

def exec_fetch_all_information_from_staffacc(staff_id):
    database.connect_database()
    sql = "SELECT * FROM staffacc WHERE staff_id='%d'"
    database.exec_query(sql % staff_id)
    values = database.fetch_cursor()
    database.disconnect_database()
    return values

def exec_fetch_all_information_from_customer(user_id):
    database.connect_database()
    sql = "SELECT * FROM memberacc WHERE mem_id='%d'"
    database.exec_query(sql % user_id)
    values = database.fetch_cursor()
    database.disconnect_database()
    return values

def exec_fetch_all_suppliers_from_supplieracc():
    database.connect_database()
    sql = "SELECT supp_id, supp_name, supp_regtime, supp_contact, supp_phone, supp_mail, supp_addr, supp_note FROM supplieracc"
    database.exec_query(sql)
    suppliers = database.fetch_cursor()
    database.disconnect_database()
    return suppliers

def exec_fetch_all_information_from_supplier(supp_id):
    #显示指定供应商的所有信息
    database.connect_database()
    sql = "SELECT * FROM supplieracc WHERE supp_id='%d'"
    database.exec_query(sql % supp_id)
    values = database.fetch_cursor()
    database.disconnect_database()
    return values

def exec_fetch_all_complaints():
    database.connect_database()
    sql = "SELECT * FROM complaint"
    database.exec_query(sql)
    complaints = database.fetch_cursor()
    database.disconnect_database()
    return complaints

def exec_fetch_staff_all_purchase_lists(staff_id):
    #返回经手人为staff_id的所有订单信息
    database.connect_database()
    sql = "SELECT purchase.purchase_id, supp_id, staff_id, purchase_time, purchase_note, item_name, purchase_quant, purchase_price, purchase_quant*purchase_price FROM purchase, purchlist, item WHERE staff_id='%d' AND purchase.purchase_id=purchlist.purchase_id AND purchlist.item_id=item.item_id"
    database.exec_query(sql % staff_id)
    lists = database.fetch_cursor()
    database.disconnect_database()
    return lists

def exec_fetch_supplier_all_purchase_lists(supp_id):
    #返回供货商为supp_id的所有订单信息
    database.connect_database()
    sql = "SELECT purchase.purchase_id, item_name, purchase_quant, purchase_price, purchase_quant*purchase_price FROM purchase, purchlist, item WHERE supp_id='%d' AND purchase.purchase_id=purchlist.purchase_id AND purchlist.item_id=item.item_id"
    database.exec_query(sql % supp_id)
    lists = database.fetch_cursor()
    database.disconnect_database()
    return lists

def exec_fetch_one_shopping_records(mem_id):
    # 二维数组返回mem_id的购买记录（item_id, shop_id, item_price, item_number）
    database.connect_database()
    sql = "SELECT item_name, shopping.shop_id, item.item_price, item_quant FROM shoplist, shopping, item WHERE item.item_id = shoplist.item_id and shopping.shop_id=shoplist.shop_id AND mem_id='%d'"
    database.exec_query(sql % mem_id)
    items = database.fetch_cursor()
    database.disconnect_database()
    return items

def exec_fetch_all_from_table_shoplist():
    # 二维数组返回所有shoplist
    database.connect_database()
    sql = "SELECT * FROM shoplist"
    database.exec_query(sql)
    shoplists = database.fetch_cursor()
    database.disconnect_database()
    return shoplists

def exec_fetch_all_from_table_staffacc():
    #二维数组返回所有员工的id,name,phone,salary
    database.connect_database()
    sql = "SELECT staff_id, staff_name, staff_phone, staff_salary FROM staffacc"
    database.exec_query(sql)
    staffs = database.fetch_cursor()
    database.disconnect_database()
    return staffs

def exec_show_items():
    database.connect_database()
    sql = "SELECT * FROM item"
    database.exec_query(sql)
    values = database.fetch_cursor()
    database.disconnect_database()
    return values

def exec_show_purchase(supplier_id):
    database.connect_database()
    sql = "SELECT * FROM purchase WHERE supp_id='%d'"
    database.exec_query(sql % supplier_id)
    purchases = database.fetch_cursor()
    database.disconnect_database()
    return purchases

def exec_show_purchase_list(purchase_id):
    database.connect_database()
    sql = "SELECT * FROM purchlist WHERE purchase_id='%d'"
    database.exec_query(sql % purchase_id)
    purchase_list = database.fetch_cursor()
    database.disconnect_database()
    return  purchase_list

def exec_show_storage_imformation(store_id):
    database.connect_database()
    sql = "SELECT * FROM storage WHERE store_id='%d'"
    database.exec_query(sql % store_id)
    storage = database.fetch_cursor()
    database.disconnect_database()
    return storage

def exec_show_store_list(store_id):
    database.connect_database()
    sql = "SELECT item_id, number FROM storelist WHERE store_id='%d'"
    database.exec_query(sql % store_id)
    storage = database.fetch_cursor()
    database.disconnect_database()
    return storage

#delete functions:

def exec_delete_supplier_in_supplieracc(supp_id_list):
    # 删除指定列表中的所有供应商相关信息
    database.connect_database()
    for certain_supplier in supp_id_list:
        sql = "DELETE FROM supplieracc WHERE supp_id='%d'"
        database.exec_update(sql % certain_supplier)
    database.disconnect_database()

def exec_delete_complain_in_complain_list(comp_id_list):
    # 删除指定投诉编号的投诉信息
    database.connect_database()
    for certain_complaint in comp_id_list:
        sql = "DELETE FROM complaint WHERE comp_id='%d'"
        database.exec_update(sql % certain_complaint)
    database.disconnect_database()

def exec_delete_staffs_in_table_staffacc_and_staffrank(fired_staff_list):
    # 删除所有fired_staff_list中的员工的相关信息
    database.connect_database()
    for certain_staff in fired_staff_list:
        sql = "DELETE FROM staffacc WHERE staff_id='%d'"
        database.exec_update(sql % certain_staff)
        sql = "DELETE FROM staff_rank WHERE staff_id='%d'"
        database.exec_update(sql % certain_staff)
    database.disconnect_database()

#add functions:

def exec_add_new_complain_to_complain_list(mem_id, comp_type, comp_content):
    database.connect_database()
    time = str(datetime.now())  # insert a new complaint
    sql = "INSERT INTO complaint(mem_id, comp_type, comp_content, comp_time) VALUES('%d','%d','%s','%s')"
    data = (mem_id, comp_type, comp_content, time)
    database.exec_update(sql % data)
    database.disconnect_database()

def exec_add_a_new_purchase(supplier_id, staff_id, purchase_note):
    database.connect_database()
    time = str(datetime.now())
    # add a new purchase
    sql = "INSERT INTO purchase(supp_id, staff_id, purchase_time, purchase_note) VALUES('%d','%d','%s','%s')"
    data = (supplier_id, staff_id, time, purchase_note)
    database.exec_update(sql % data)
    database.disconnect_database()

def exec_add_a_new_purchlist(item_id, purchase_id, purchase_price, purchase_quant):
    database.connect_database()
    # add a new purchlist
    sql = "INSERT INTO purchlist VALUES('%d','%d','%.2f','%d')"
    data = (item_id, purchase_id, purchase_price, purchase_quant)
    database.exec_update(sql % data)
    database.disconnect_database()

def exec_add_new_shopping_record(mem_id):
    database.connect_database()
    time = str(datetime.now())
    # insert a new shopping record
    sql = "INSERT INTO shopping(mem_id, shop_time) VALUES('%d','%s')"
    data = (mem_id,time)
    database.exec_update(sql % data)
    # return the shop_id
    sql = "SELECT max(shop_id) FROM shopping"
    database.exec_query(sql)
    shop_id = database.fetch_cursor()[0][0]
    database.disconnect_database()
    return shop_id

def exec_add_new_shopping_list(shop_id, order_list):
    database.connect_database()
    time = str(datetime.now())
    # insert a new shopping list
    for current_item in order_list:
        item_id = current_item[0]
        item_quantity = current_item[1]
        sql = "SELECT item_price FROM item WHERE item_id = '%d'"
        database.exec_query(sql % item_id)
        item_price = database.fetch_cursor()[0][0]
        sql = "INSERT INTO shoplist VALUES('%d','%d','%.2f','%d')"
        data = (item_id, shop_id, item_price, item_quantity)
        database.exec_update(sql % data)
    database.disconnect_database()

#change functions:

def exec_change_the_credit_customer(user_id, credits):
    database.connect_database()
    sql = "UPDATE memberacc SET mem_point = mem_point + '%d' WHERE mem_id='%d'"
    data = (credits, user_id)
    database.exec_update(sql % data)
    database.disconnect_database()

def exec_change_the_information_staff(id, password, phone, address, note):
    database.connect_database()
    sql = "UPDATE staffacc SET staff_psw ='%s',staff_phone='%s',staff_addr='%s',staff_note='%s' WHERE staff_id='%d'"
    data = (password, phone, address, note, id)
    database.exec_update(sql % data)
    database.disconnect_database()

def exec_change_the_information_supplier(id, password, contact, phone, email, address, note):
    database.connect_database()
    sql = "UPDATE supplieracc SET supp_psw ='%s',supp_contact='%s',supp_phone='%s',supp_mail='%s',supp_addr='%s',supp_note='%s' WHERE supp_id='%d'"
    data = (password, contact, phone, email, address, note, id)
    database.exec_update(sql % data)
    database.disconnect_database()

def exec_change_the_information_customor(user_id, password, phone, email, note):
    database.connect_database()
    sql = "UPDATE memberacc SET mem_psw ='%s', mem_phone='%s', mem_mail='%s', mem_note='%s' WHERE mem_id='%d'"
    data = (password, phone, email, note, user_id)
    database.exec_update(sql % data)
    database.disconnect_database()

#other functions:

def exec_find_item_in_storage(item_id):
    database.connect_database()
    sql = "SELECT * number FROM storelist WHERE item_id='%d'"
    database.exec_query(sql % item_id)
    storage = database.fetch_cursor()
    database.disconnect_database()
    return storage

def exec_search_matched_from_table_items(search_string):
    # 二维数组返回所有商品名称中包含search_string的商品清单
    database.connect_database()
    sql = "SELECT * FROM item WHERE item_name LIKE '%%%s%%' "
    database.exec_query(sql % search_string)
    items = database.fetch_cursor()
    database.disconnect_database()
    return items

def exec_add_an_employee(employee_name, department, employee_password, employee_idcard, employee_phone,employee_address,employee_position,employee_note,employee_salary):
    database.connect_database()
    hiredate = str(datetime.now())
    sql = "INSERT INTO staffacc(staff_name, dept_id, staff_psw, staff_idcard, staff_phone, staff_addr, staff_pos, staff_hiredate, staff_note, staff_salary) VALUES('%s','%d','%s','%s','%s','%s','%s','%s','%s','%d')"
    data = (employee_name, department, employee_password, employee_idcard, employee_phone,employee_address,employee_position, hiredate, employee_note,employee_salary)
    database.exec_update(sql % data)
    database.disconnect_database()