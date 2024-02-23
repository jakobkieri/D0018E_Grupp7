from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import pymysql
import sys
customer_bp = Blueprint('customer', __name__, 
                        template_folder='templates',
                        static_folder='static')

#linux
connection_input = {'host': '172.17.0.2','port': 3306, 'user': 'root','password': 'bingus','database': 'mydb',"charset":'utf8mb4',"cursorclass":pymysql.cursors.DictCursor}

#other (souce: Marcus)
#connection_input = {"host":"localhost","user":'root',"password":'bingus',"database":'mydb',"charset":'utf8mb4',"cursorclass":pymysql.cursors.DictCursor}

@customer_bp.route("/", methods=["GET", "POST"])
def customer():
    connection = pymysql.connect(**connection_input)
    cursor = connection.cursor()
    sql = "SELECT pro_name, pro_img, pro_info, price, pro_ID FROM Products"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result, file=sys.stderr)
    connection.close()
    return render_template("CusMain.html", title= "Customer Main", products = result)

@customer_bp.route("/enter", methods=["GET", "POST"])
def enterProduct():
    if "pro_ID" in request.form:
        currID = request.form['pro_ID']
        session['pro_ID'] = currID
        print(currID, file=sys.stderr)
        return redirect(url_for("customer.product"))
    else:
        return redirect(url_for("customer.customer"))
    
@customer_bp.route("/product", methods=["GET", "POST"])
def product():
    connection = pymysql.connect(**connection_input)
    cursor = connection.cursor()
    sql = "SELECT * FROM Products WHERE pro_ID = " + session["pro_ID"]
    print(sql, file=sys.stderr)
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result, file=sys.stderr)
    connection.close()
    return render_template("CusProduct.html", title= "Customer Product", product = result)


@customer_bp.route("/cart", methods = ["GET", "POST"])
def cart():
    connection = pymysql.connect(**connection_input)
    cursor = connection.cursor()
    sql = "SELECT * FROM Cart JOIN Products ON Products.pro_ID=Cart.pro_ID WHERE Products.pro_ID IN (SELECT `pro_ID` FROM Cart WHERE `acc_e-mail` = '" + session["e-mail"] + "');" # select all products in cart
    cursor.execute(sql)
    result = cursor.fetchall()
    total = 0
    for item in result:  #set price to total price of item in cart
        item["price"] = int(item["price"])*int(item["qty"])
        total += int(item["price"])
    print(result, file=sys.stderr)
    return render_template("CusCart.html", title = "Customer Cart", cartItems = result, total = total)