# -*-coding:utf-8-*-
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

import DatabaseConnection
import transaction
import string

time = str(datetime.now())

app = Flask(__name__)
app.secret_key = 'asfasfasfasqwerqwr'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/supplier_login', methods=['GET'])
def supplier_login_form():
    return render_template('supplier_login.html')


@app.route('/supplier_login', methods=['POST'])
def supplier_login():
    username = request.form['username']
    password = request.form['password']
    
    (is_valid, supplier_tuple) = DatabaseConnection.exec_supplier_login(username, password)

    if is_valid:
        supplier_id = supplier_tuple[0][0]
        return redirect(url_for('supplier', supplier_id=supplier_id))
    
    flash("The account does not exist, check it again.")
    return redirect('/supplier_login')



@app.route('/staff_login', methods=['GET'])
def staff_login_form():
    return render_template('staff_login.html')


@app.route('/staff_login', methods=['POST'])
def staff_login():
    username = request.form['username']
    password = request.form['password']

    # (is_valid, user_id_tuple = DatabaseConnection.exec_staff_login(username, password)
    (is_valid, user_id, admin_type) = DatabaseConnection.exec_staff_login(username, password)
    if is_valid and admin_type == 1:
        return redirect(url_for('staff_hr_get', user_id=user_id, get_type='hr_main_page'))

    if is_valid and admin_type == 2:
        return redirect(url_for('staff_pd_get', user_id=user_id))

    flash("The account does not exist, please retype it!")
    return redirect('/staff_login')

@app.route('/staff_hr/<user_id>/<get_type>', methods=['GET'])
def staff_hr_get(user_id=None, get_type=None):
    if get_type == 'hr_main_page':
        return render_template('administer_hr.html', user_id=user_id)
    if get_type == 'hr_profile':
        return render_template('administer_hr_info.html', user_id=user_id)
    if get_type == 'hr_show_staff_info':
        items = transaction.fetch_staff_record_for_admin()
        return render_template('administer_hr_employee.html', user_id=user_id, items=items)
    if get_type == 'hr_show_purchase_record':
        items = transaction.fetch_shopping_record_for_admin()
        return render_template('administer_hr_purchase_record.html', user_id=user_id, items=items)


@app.route('/staff_hr/<user_id>/<post_type>', methods=['POST'])
def staff_hr_post(user_id=None, post_type=None):
    if post_type == 'hire_employee':
        employee_name = request.form['employee_name']
        department = int(request.form['employee_department'])
        employee_password = request.form['employee_password']
        employee_idcard = request.form['employee_idcard']
        employee_phone = request.form['employee_phone']
        employee_address = request.form['employee_address']
        employee_position = request.form['employee_position']
        employee_note = request.form['employee_note']
        employee_salary = int(request.form['employee_salary'])
        DatabaseConnection.exec_add_an_employee(employee_name, department, employee_password, employee_idcard, employee_phone,employee_address,employee_position,employee_note,employee_salary)
        return redirect(url_for('staff_hr_get', user_id=user_id, get_type='hr_show_staff_info'))
    if post_type == 'fire_employee':
        fired_staff_list = request.form.getlist('items[]')
        print 'fired_staff_list:', fired_staff_list

        transaction.fire_staffs(fired_staff_list)
        return redirect(url_for('staff_hr_get', user_id=user_id, get_type='hr_show_staff_info'))



@app.route('/staff_pd/<int:user_id>', methods=['GET'])
def staff_pd_get(user_id=None):
    purchlists_num=len(DatabaseConnection.exec_fetch_staff_all_purchase_lists(user_id))
    suppliers_num=len(DatabaseConnection.exec_fetch_all_suppliers_from_supplieracc())
    return render_template("staff_purchase_department.html", user_id=user_id, purchlists_num=purchlists_num,suppliers_num=suppliers_num)

@app.route('/staff_pd_info_back/<int:user_id>/<info_type>', methods=['GET'])
def staff_pd_info_back(user_id=None, info_type=None):

    if info_type == "Information":
         staff_pd_tuple=DatabaseConnection.exec_fetch_all_information_from_staffacc(user_id)
         return render_template('staff_pd_information.html', user_id=user_id, info_type=info_type, staff_pd_tuple=staff_pd_tuple)
    elif info_type == "Purchase_history":
        staff_pd_tuple=DatabaseConnection.exec_fetch_staff_all_purchase_lists(user_id)
        return render_template('staff_pd_purchase_history.html', user_id=user_id, info_type=info_type, staff_pd_tuple=staff_pd_tuple)
    elif info_type == "Supplier_list":
        staff_pd_tuple=DatabaseConnection.exec_fetch_all_suppliers_from_supplieracc()
        return render_template('staff_pd_supplier_list.html', user_id=user_id, info_type=info_type, staff_pd_tuple=staff_pd_tuple)
    elif info_type == "Add_purchase_list":
        return  render_template('staff_pd_add_purchase_list.html', user_id=user_id)

@app.route('/staff_pd_info_back/<int:user_id>/<info_type>', methods=['POST'])
def staff_pd_info_back_edit(user_id=None, info_type=None):
    if info_type=="Information":
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        note = request.form['note']
        user_id = int(user_id)
        DatabaseConnection.exec_change_the_information_staff(user_id, password, phone, address, note)
        return redirect(url_for('staff_pd_info_back', user_id=user_id, info_type=info_type))

    elif info_type == "Supplier_list":
        val=request.form.get('supp_name', type=str, default='')
        if val != '':
            supp_name = request.form['supp_name']
            supp_psw = request.form['supp_psw']
            supp_contact = request.form['supp_contact']
            supp_phone = request.form['supp_phone']
            supp_mail = request.form['supp_mail']
            supp_addr = request.form['supp_addr']
            supp_note = request.form['supp_note']
            DatabaseConnection.exec_add_a_new_supplier(supp_name, supp_psw, supp_contact, supp_phone, supp_mail, supp_addr, supp_note)
        else:
            supplier_id_list=[int(each) for each in request.form.getlist('suppliers[]')]
            DatabaseConnection.exec_delete_supplier_in_supplieracc(supplier_id_list)

        return redirect(url_for('staff_pd_info_back', user_id=user_id, info_type=info_type))
    elif info_type == "Add_purchase_list":
        item_id=request.form['item_id']
        purchase_id=request.form['purchase_id']
        purchase_price=request.form['purchase_price']
        purchase_quant=request.form['purchase_quant']
        DatabaseConnection.exec_add_a_new_purchlist(item_id, purchase_id, purchase_price, purchase_quant)
        return  render_template('staff_pd_add_purchase_list.html', user_id=user_id)



@app.route('/customer_login', methods=['GET'])
def customer_login_form():
    return render_template('customer_login.html')


@app.route('/customer_login', methods=['POST'])
def customer_login():
    username = request.form['username']
    password = request.form['password']


    (is_valid, user_tuple) = DatabaseConnection.exec_customer_login(username, password)
    if is_valid:
        user_id = user_tuple[0][0]
        return redirect(url_for('customer', user_id=user_id))

    flash("The account does not exist, check it again.")
    return redirect('/customer_login')


@app.route('/customer/<user_id>', methods=['GET'])
def customer(user_id=None):
    items = DatabaseConnection.exec_show_items()
    return render_template("customer.html", user_id=user_id, items=items)


@app.route('/customer/<user_id>/<jump_type>', methods=['GET'])
def customer_form_get_type(user_id=None, jump_type=None):
    #render different html through jump type

    if jump_type == 'customer_info':
        customer_info_list = transaction.show_all_information_of_customer(user_id)
        return render_template('customer_information.html', user_id=user_id, customer_info=customer_info_list)

    if jump_type == 'purchase_history':
        purchase_history = transaction.show_all_purchase_history_of_customer(user_id)
        return render_template('customer_purchase_history.html', user_id=user_id, items=purchase_history)

    if jump_type == 'edit_info':
        return render_template('customer_editinfo.html', user_id=user_id)

    if jump_type == 'submit_complain':
        return render_template('customer_complain.html', user_id=user_id)





@app.route('/customer/<user_id>/<post_type>', methods=['POST'])
def customer_process_post(user_id=None, post_type=None):
    print 'successfully jump!'

    # process different posted message through post_type, then jump back to the previous html.
    #处理购买提交
    if post_type == 'purchase':
        print 'hhh'
        id_list = request.form.getlist('items[]')
        number_list = request.form.getlist('quantity[]')

        transaction.process_purchase(user_id, id_list, number_list)


    #处理搜索信息
    if post_type == 'search':
        search_string = request.form.get('search', default="")
        print search_string
        items = transaction.process_search_itmes_for_customer(search_string)
        print items
        return render_template('customer_search_items.html', user_id=user_id, items=items)

    #处理编辑个人信息提交
    if post_type == 'edit_info':
        print 'successful post edit_customer!'
        password = request.form['edit_customer_password']
        print 'successful post password'
        telephone = request.form['edit_customer_telephone']
        email = request.form['edit_customer_email']
        notes = request.form['edit_customer_notes']
        transaction.process_edit_customer_info(user_id, password, telephone, email, notes)


    #处理投诉提交
    if post_type == 'complain':
        complain_type_string = request.form['complain_type']
        complain_content = request.form['complain_content']
        transaction.process_complain(user_id, complain_type_string, complain_content)
        print 'lll'

    return redirect(url_for('customer', user_id=user_id))



@app.route('/customer_information/<user_id>')
def customer_information(user_id=None):
    # TODO customer_info = fetch_all_information_from_customer(user_id)
    return render_template('customer_information.html', user_id=user_id)


@app.route('/customer_complain/<user_id>', methods=['GET'])
def complain_form(user_id=None):
    return render_template('customer_complain.html', user_id=user_id)


@app.route('/customer_complain/<user_id>', methods=['POST'])
def complain(user_id=None):
    # TODO complain_list = request.form['']
    # transaction.process_complain(user_id, complain_list)
    return render_template('customer.html', user_id=user_id)


@app.route('/supplier/<int:supplier_id>',methods=['GET'])
def supplier(supplier_id=None):
    orders_num=len(DatabaseConnection.exec_fetch_supplier_all_purchase_lists(supplier_id))
    complains_num=len(DatabaseConnection.exec_fetch_all_complaints())
    return render_template("supplier.html",supplier_id=supplier_id,orders_num=orders_num, complains_num=complains_num)


@app.route('/supplier_info_back/<int:supplier_id>/<info_type>', methods=['GET'])
def supplier_info_back(supplier_id=None, info_type=None):

    if info_type == "Information":
        supplier_tuple=DatabaseConnection.exec_fetch_all_information_from_supplier(supplier_id)
        return render_template('supplier_information.html', supplier_id=supplier_id, info_type=info_type, supplier_tuple=supplier_tuple)
    elif info_type == "Orders":
        supplier_tuple=DatabaseConnection.exec_fetch_supplier_all_purchase_lists(supplier_id)
        return render_template('supplier_orders.html', supplier_id=supplier_id, info_type=info_type, supplier_tuple=supplier_tuple)
       #return render_template('supplier_orders.html', supplier_id=supplier_id)
    elif info_type == "After_sale_service":
        supplier_tuple=DatabaseConnection.exec_fetch_all_complaints()
        return render_template('supplier_after_sale_service.html', supplier_id=supplier_id, info_type=info_type, supplier_tuple=supplier_tuple)
        #return render_template('supplier_after_sale_service.html', supplier_id=supplier_id)

@app.route('/supplier_info_back/<int:supplier_id>/<info_type>', methods=['POST'])
def supplier_info_back_edit(supplier_id=None, info_type=None):
    if info_type=="Information":
        password = request.form['password']
        contect = request.form['contect']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        note = request.form['note']
        supplier_id = int(supplier_id)
        DatabaseConnection.exec_change_the_information_supplier(supplier_id,password, contect, phone, email, address, note)
        return redirect(url_for('supplier_info_back', supplier_id=supplier_id, info_type=info_type))
    elif info_type == "After_sale_service":
        complaint_id_list=[int(each) for each in request.form.getlist('complains[]')]
        print complaint_id_list
        DatabaseConnection.exec_delete_complain_in_complain_list(complaint_id_list)
        return redirect(url_for('supplier_info_back', supplier_id=supplier_id, info_type=info_type))
    





@app.route('/registeration', methods=['GET'])
def registeration_form():
    return render_template('registeration.html')


@app.route('/registeration', methods=['POST'])
def registeration():
    username = request.form['username']
    password = request.form['password']
    retype_password = request.form['retype_password']
    email = request.form['email']

    if retype_password != password:
        flash("The password is not consistent!")
        return redirect('/registeration')

    is_valid = DatabaseConnection.exec_register_customer(username, password, email)
    if is_valid:
        return redirect('/customer_login')
    else:
        flash("The username has been registered, Please Try again")
        return redirect('/registeration')


#
# @app.route()
# def logout():
#     pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
