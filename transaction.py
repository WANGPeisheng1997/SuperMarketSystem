# -*-coding:utf-8-*-
import DatabaseConnection


def show_all_items_for_customer():
    items = DatabaseConnection.exec_show_items()
    return items


def process_purchase(user_id_string, id_list_string, number_list_string):
    # TODO 没额外说明的就没有返回值
    user_id = int(user_id_string)
    id_list = map(eval, id_list_string)
    number_list = map(eval, number_list_string)
    # print id_list
    # print number_list
    shop_id = DatabaseConnection.exec_add_new_shopping_record(user_id)
    # order_list = zip(id_list, number_list)
    # print order_list
    number2_list = []
    for id in id_list:
        number2_list.append(3)

    print number2_list
    order_list = zip(id_list, number2_list)
    print order_list
    DatabaseConnection.exec_add_new_shopping_list(shop_id, order_list)
    DatabaseConnection.exec_change_the_credit_customer(user_id, 10)



def process_complain(user_id_string, complain_type_string, complain_content):
    user_id = int(user_id_string)
    complain_type = int(complain_type_string)
    print 'kkk'
    DatabaseConnection.exec_add_new_complain_to_complain_list(user_id, complain_type, complain_content)
    print 'mmm'

def process_edit_customer_info(user_id_string, password, telephone, email, notes):
    user_id = int(user_id_string)
    DatabaseConnection.exec_change_the_information_customor(user_id, password, telephone, email, notes)


def process_search_itmes_for_customer(search_string):
    # TODO 返回给我满足商品名称与search_string部分匹配的items的二维数组
    match_items = DatabaseConnection.exec_search_matched_from_table_items(search_string)
    return match_items


def show_all_information_of_customer(user_id_string):
    user_id = int(user_id_string)
    print user_id
    customer_info_tuple = DatabaseConnection.exec_fetch_all_information_from_customer(user_id)
    customer_info_list = [''] * 10
    customer_info_list[0] = str(customer_info_tuple[0][0])
    customer_info_list[1] = str(customer_info_tuple[0][1])
    customer_info_list[2] = str(customer_info_tuple[0][2])
    customer_info_list[3] = str(customer_info_tuple[0][3])
    customer_info_list[4] = str(customer_info_tuple[0][4])
    customer_info_list[5] = str(customer_info_tuple[0][5])
    customer_info_list[6] = str(customer_info_tuple[0][6])
    customer_info_list[7] = str(customer_info_tuple[0][7])
    return customer_info_list


def show_all_purchase_history_of_customer(user_id_string):
    user_id = int(user_id_string)
    # TODO 返回编号为user_id的用户的购买历史二维数组，格式为item_id, shop_id, item_price, item_number
    history = DatabaseConnection.exec_fetch_one_shopping_records(user_id)
    return history


def fetch_shopping_record_for_admin():
    pass
    # TODO 返回给我所有shopping（从shoplist中）
    items = DatabaseConnection.exec_fetch_all_from_table_shoplist()
    return items


def fetch_staff_record_for_admin():
    pass
    # TODO 返回给我staffacc中的信息, id, acco
    items = DatabaseConnection.exec_fetch_all_from_table_staffacc()
    return items

def fire_staffs(fired_staff_list_string):
    # TODO 不返回，传入的是要删除的staff的id的列表
    fired_staff_list = map(eval, fired_staff_list_string)
    DatabaseConnection.exec_delete_staffs_in_table_staffacc_and_staffrank(fired_staff_list)