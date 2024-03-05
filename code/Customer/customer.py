from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import pymysql
import sys
from datetime import datetime
customer_bp = Blueprint('customer', __name__, 
                        template_folder='templates',
                        static_folder='static')

#linux
connection_input = {'host': '172.17.0.2','port': 3306, 'user': 'root','password': 'bingus','database': 'mydb',"charset":'utf8mb4',"cursorclass":pymysql.cursors.DictCursor}

#other (souce: Marcus)
connection_input = {"host":"localhost","user":'root',"password":'bingus',"database":'mydb',"charset":'utf8mb4',"cursorclass":pymysql.cursors.DictCursor}


def getConnection():
    return pymysql.connect(**connection_input)


@customer_bp.route("/", methods=["GET", "POST"])
def customer():
    connection = getConnection()
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
    connection = getConnection()
    cursor = connection.cursor()
    sql = "SELECT * FROM Products WHERE pro_ID = %s"
    cursor.execute(sql, (session["pro_ID"]))
    product = cursor.fetchone()
    print(product, file=sys.stderr)
    sql = "SELECT * FROM Reviews WHERE pro_ID = %s"
    cursor.execute(sql, (session["pro_ID"]))
    reviews = list(cursor.fetchall())

    ###Get average rating

    ratings = []
    for review in reviews:
        ratings.append(int(review["nr_stars"]))
    if len(ratings) > 0:
        avg_rev = str(sum(ratings) / len(ratings))
    else:
        avg_rev = "No reviews"
    #print(reviews, file=sys.stderr)
    connection.close()
    return render_template("CusProduct.html", title="Customer Product", product = product, reviews = reviews, user = session["e-mail"], avg_rev = avg_rev)


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
    #print(result, file=sys.stderr)
    return render_template("CusCart.html", title = "Customer Cart", cartItems = result, total = total)

@customer_bp.route("/cart/add", methods=["GET", "POST"])
def addToCart():
    connection = getConnection()
    cursor = connection.cursor()
    sql = "SELECT * FROM Products WHERE pro_ID = %s"
    cursor.execute(sql, (session["pro_ID"]))
    result = cursor.fetchone()
    #print(result, file=sys.stderr)
    qty = result["qty"] 
    if qty > 0:
        sql = "SELECT cart_ID FROM Cart ORDER BY cart_ID DESC LIMIT 0,1" # select the highest current id
        cursor.execute(sql)
        result = cursor.fetchone()
        #print(result, file=sys.stderr)
        if result == None:
            newId = 0
        else:
            newId = int(result["cart_ID"]) + 1 

        # Tried with IF NOT EXISTS, could not get it to work
                
        sql = "SELECT * FROM Cart WHERE pro_ID = " + str(session["pro_ID"]) + " AND `acc_e-mail` = '" + session["e-mail"] + "';"
        cursor.execute(sql)
        result = cursor.fetchone()
        #print(result, file=sys.stderr)
        if result == None:
            sql = "INSERT INTO Cart VALUES (1, '" + session["e-mail"] + "', " + str(session["pro_ID"]) + ", " + str(newId) + ");" 
            cursor.execute(sql)
    connection.commit()
    connection.close()
    return redirect(url_for('customer.product'))


@customer_bp.route("/cart/form", methods=["GET", "POST"])
def cartForm():
    form = request.form
    pro_IDs = list(form.keys())
    if "isOrder" in pro_IDs:
        #If request came frokm submit button
        placeOrder()
        return redirect(url_for('customer.cart'))
    connection = getConnection()
    cursor = connection.cursor()
    print(form, file=sys.stderr)
    for pro_ID in pro_IDs:
        sql = "SELECT * FROM Cart WHERE pro_ID = %s AND `acc_e-mail` = '" + session["e-mail"] + "';"
        cursor.execute(sql, str(pro_ID))
        result = cursor.fetchone()
        newQty = form[pro_ID]
        #print(newQty, file=sys.stderr)
        if newQty == "":
            return redirect(url_for('customer.cart'))
        #print(str(newQty) + " = " + str(result["qty"]), file=sys.stderr)
        if str(newQty) != str(result["qty"]): 
            if int(newQty) > 0:
                sql = "UPDATE Cart SET qty= " + str(newQty) + " WHERE pro_ID = %s AND `acc_e-mail` = '" + session["e-mail"] + "';"
            else: 
                sql = "DELETE FROM Cart WHERE pro_ID = %s AND `acc_e-mail` = '" + session["e-mail"] + "';"
            cursor.execute(sql, str(pro_ID))
    connection.commit()
    connection.close()
    return redirect(url_for('customer.cart'))

def placeOrder():
    connection = getConnection()
    cursor = connection.cursor()
    form = request.form
    print(form, file=sys.stderr)

    ### Get latest order id

    sql = "SELECT ord_ID FROM Orders ORDER BY ord_ID DESC LIMIT 0,1" # select the highest current id
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        newId = 0
    else:
        newId = int(result["ord_ID"]) + 1 

    sql = "SELECT * FROM Cart WHERE `acc_e-mail` = '" + session["e-mail"] + "';"
    cursor.execute(sql)
    result = cursor.fetchall() 

    #print(result, file=sys.stderr)

    for cartItem in result:
        sql = "SELECT * FROM Products WHERE pro_ID = " + str(cartItem["pro_ID"]) + ";"
        cursor.execute(sql)
        proResult = cursor.fetchone()
        if cartItem["qty"] > proResult["qty"]:
            return ### Abort order
        else:
            ### Change qty of product

            newQty = int(proResult["qty"]) - int(cartItem["qty"])
            sql = "UPDATE Products SET qty = " + str(newQty) + " WHERE pro_ID = " + str(cartItem["pro_ID"]) + ";"
            cursor.execute(sql)

            ### Insert balance change

            ### Get latest id

            sql = "SELECT change_ID FROM Balance_Changes ORDER BY change_ID DESC LIMIT 0,1" # select the highest current id
            cursor.execute(sql)
            result = cursor.fetchone()
            #print(result, file=sys.stderr)
            if result == None:
                newId = 0
            else:
                newId = int(result["change_ID"]) + 1 
            
            current_datetime = datetime.now()
            current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            sql = "INSERT INTO Balance_Changes VALUES (" + str(newId) + ", 0, " + str(cartItem["qty"]) + ", '" + str(current_datetime) + "', '" + session["e-mail"] + "', "+ str(cartItem["pro_ID"]) + ");"
            cursor.execute(sql)    
            
            ### Insert order
            
            price = int(cartItem["qty"]) * int(proResult["price"])
            sql = "INSERT INTO mydb.Orders (`ord_ID`, `qty`, `price`, `acc_e-mail`, `pro_ID`) VALUES (" + str(newId) + ", " + str(cartItem["qty"]) + ", " + str(price) + ", '" + session["e-mail"] + "', " + str(cartItem["pro_ID"]) + ");"
            cursor.execute(sql)

            ### Delete cart item

            sql = "DELETE FROM Cart WHERE cart_ID = " + str(cartItem["cart_ID"]) + ";"
            cursor.execute(sql)
            connection.commit()
    connection.close()


@customer_bp.route("/product/addReview", methods=["POST", "GET"])
def addReview():
    print(request.form, file=sys.stderr)
    connection = getConnection()
    cursor = connection.cursor()
    productId = session["pro_ID"]
    userMail = session["e-mail"]
    stars = request.form["rating"]
    content = request.form["content"]
    sql = "SELECT * FROM Reviews WHERE pro_ID = " + productId + " AND `acc_e-mail` = '" + userMail + "';"
    cursor.execute(sql)
    review = cursor.fetchone()

    if review:
        reviewId = review["re_ID"]
        sql = "UPDATE Reviews SET `nr_stars` = " + str(stars) + ", comment = '" + content + "' WHERE re_ID = " + str(reviewId) + ";"
        cursor.execute(sql)
    else: 
        sql = "SELECT re_ID FROM Reviews ORDER BY re_ID DESC LIMIT 0,1" # select the highest current id
        cursor.execute(sql)
        result = cursor.fetchone()
        #print(result, file=sys.stderr)
        if result == None:
            newId = 0
        else:
            newId = int(result["re_ID"]) + 1 
        date = datetime.now()
        date = date.strftime("%y/%m/%d")
        sql = "INSERT INTO Reviews VALUES (" + str(newId) + ", '" + content + "', " + str(stars) + ", '" + str(date) + "', '" + userMail + "', " + str(productId) + ");"
        cursor.execute(sql) 
    connection.commit()
    connection.close()
    return redirect(url_for("customer.product"))

@customer_bp.route("/product/delReview", methods=["POST", "GET"])
def delReview():
    connection = getConnection()
    cursor = connection.cursor()
    productId = session["pro_ID"]
    email = session["e-mail"]
    sql = "DELETE FROM Reviews WHERE pro_ID = " + str(productId) + " AND `acc_e-mail` = '" + email + "';"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return redirect(url_for("customer.product"))