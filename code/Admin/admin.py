from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import pymysql
import sys
admin_bp = Blueprint('admin', __name__, 
                        template_folder='templates',
                        static_folder='static')

host = 'localhost'



@admin_bp.route("/", methods=["GET", "POST"])
def admin():
    connection = pymysql.connect(host=host,
                             user='root',
                             password='bingus',
                             database='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT pro_name, pro_img, pro_info, price, pro_ID FROM Products"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result, file=sys.stderr)
    connection.close()
    return render_template("AdmMain.html", title="Admin Main", products = result)




@admin_bp.route("/add_product", methods=["GET", "POST"])
def addProduct():
    connection = pymysql.connect(host=host,
                    user='root',
                    password='bingus',
                    database='mydb',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT pro_ID FROM Products ORDER BY pro_ID DESC LIMIT 0,1" # select the highest current id
    cursor.execute(sql)
    result = cursor.fetchone()
    newId = int(result["pro_ID"]) + 1 
    print(newId, file=sys.stderr)
    sql = "INSERT INTO Products (pro_ID, pro_name, qty, price) VALUES (" + str(newId) +", 'placeholder"+str(newId)+"', 0, 0)"
    query = cursor.execute(sql)
    connection.commit()
    #print(query, file=sys.stderr)
    connection.close()
    return redirect(url_for('admin.admin')) #replace with render product page
   

@admin_bp.route("/product", methods=["GET", "POST"])
def product():
    connection = pymysql.connect(host=host,
                             user='root',
                             password='bingus',
                             database='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT * FROM Products WHERE pro_ID = %s"
    cursor.execute(sql, (session["pro_ID"]))
    result = cursor.fetchone()
    print(result, file=sys.stderr)
    connection.close()
    return render_template("AdmProduct.html", title="Admin Product", product = result)


@admin_bp.route("/enter", methods=["GET", "POST"])
def enterProduct():
    if "pro_ID" in request.form:
        currID = request.form['pro_ID']
        session['pro_ID'] = currID
        print(currID, file=sys.stderr)
        return redirect(url_for("admin.product"))
    else:
        return redirect(url_for("admin.admin"))


@admin_bp.route('/change_name', methods=["GET", "POST"])
def change_name():
    if "pro_ID" in request.form and "new_name" in request.form:

        connection = pymysql.connect(host=host,
                             user='root',
                             password='bingus',
                             database='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

        product_id = request.form['pro_ID']
        new_name = request.form['new_name']

        sql = "UPDATE Products SET pro_name = %s WHERE pro_ID = %s"
        params = (new_name, product_id)

        cursor.execute(sql, params)
        result = cursor.fetchone()
        print(result, file=sys.stderr)
        connection.commit()
        connection.close()

        return redirect(url_for("admin.product"))       # Product name updated successfully
    else:
        return redirect(url_for('admin.admin'))         # Product not found


@admin_bp.route('/change_info', methods=["GET", "POST"])
def change_info():
    if "pro_ID" in request.form and "new_info" in request.form:

        connection = pymysql.connect(host=host,
                             user='root',
                             password='bingus',
                             database='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

        product_id = request.form['pro_ID']
        new_info = request.form['new_info']

        sql = "UPDATE Products SET pro_info = %s WHERE pro_ID = %s"
        params = (new_info, product_id)

        cursor.execute(sql, params)
        result = cursor.fetchone()
        print(result, file=sys.stderr)
        connection.commit()
        connection.close()

        return redirect(url_for("admin.product"))       # Product information updated successfully
    else:
        return redirect(url_for('admin.admin'))         # Product not found


@admin_bp.route('/update_price', methods=["GET", "POST"])
def update_price():
    if "pro_ID" in request.form and "new_price" in request.form:

        connection = pymysql.connect(host=host,
                             user='root',
                             password='bingus',
                             database='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

        product_id = request.form['pro_ID']
        new_price = request.form['new_price']

        sql = "UPDATE Products SET price = %s WHERE pro_ID = %s"
        params = (new_price, product_id)

        cursor.execute(sql, params)
        result = cursor.fetchone()
        print(result, file=sys.stderr)
        connection.commit()
        connection.close()

        return redirect(url_for("admin.product"))       # Product price updated successfully
    else:
        return redirect(url_for('admin.admin'))         # Product not found

@admin_bp.route('/change_qty', methods=["GET", "POST"])
def change_qty():
    if "pro_ID" in request.form and "qty_change" in request.form and "old_qty" in request.form:

        connection = pymysql.connect(host=host,
                             user='root',
                             password='bingus',
                             database='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

        product_id = request.form['pro_ID']
        qty_change = int(request.form['qty_change'])
        old_qty = int(request.form['old_qty'])
        new_qty = old_qty + qty_change

        sql = "UPDATE Products SET qty = %s WHERE pro_ID = %s"
        params = (new_qty, product_id)

        cursor.execute(sql, params)
        result = cursor.fetchone()
        print(result, file=sys.stderr)
        connection.commit()
        connection.close()

        return redirect(url_for("admin.product"))       # Product quantity updated successfully
    else:
        return redirect(url_for('admin.admin'))         # Product not found


@admin_bp.route('/change_image', methods=["GET", "POST"])
def change_image():
    if "pro_ID" in request.form and "newImg" in request.form:

        connection = pymysql.connect(host=host,
                             user='root',
                             password='bingus',
                             database='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()

        product_id = request.form['pro_ID']
        newImg = request.form['newImg']
        new_image_path = "/../static/images/" + newImg   # Adjust this path according to your directory structure

        sql = "UPDATE Products SET pro_img = %s WHERE pro_ID = %s"
        params = (new_image_path, product_id)

        cursor.execute(sql, params)
        result = cursor.fetchone()
        print(result, file=sys.stderr)
        connection.commit()
        connection.close()

        return redirect(url_for("admin.product"))       # Product image updated successfully
    else:
        return redirect(url_for('admin.admin'))         # Product not found
