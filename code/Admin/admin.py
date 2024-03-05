from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from datetime import datetime
import pymysql
import sys

# to upload images
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, 
                        template_folder='templates',
                        static_folder='static')


#linux
#connection_input = {'host': '172.17.0.2','port': 3306, 'user': 'root','password': 'bingus','database': 'mydb',"charset":'utf8mb4',"cursorclass":pymysql.cursors.DictCursor}

#other (souce: Markus)
connection_input = {"host":"localhost","user":'root',"password":'bingus',"database":'mydb',"charset":'utf8mb4',"cursorclass":pymysql.cursors.DictCursor}

def getConnection():
    return pymysql.connect(**connection_input)


@admin_bp.route("/", methods=["GET", "POST"])
def admin():
    connection = getConnection()
    cursor = connection.cursor()
    sql = "SELECT pro_name, pro_img, pro_info, price, pro_ID FROM Products"
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result, file=sys.stderr)
    connection.close()
    return render_template("AdmMain.html", title="Admin Main", products = result)


@admin_bp.route("/add_product", methods=["GET", "POST"])
def addProduct():
    connection = getConnection()
    cursor = connection.cursor()
    sql = "SELECT pro_ID FROM Products ORDER BY pro_ID DESC LIMIT 0,1" # select the highest current id
    cursor.execute(sql)
    result = cursor.fetchone()
    #print(result, file=sys.stderr)
    if result == None:
        newId = 0
    else:
        newId = int(result["pro_ID"]) + 1 
    #print(newId, file=sys.stderr)
    sql = "INSERT INTO Products (pro_ID, pro_name, qty, price) VALUES (" + str(newId) +", 'placeholder', 0, 0)"
    query = cursor.execute(sql)
    connection.commit()
    #print(query, file=sys.stderr)
    connection.close()
    return redirect(url_for('admin.admin')) # Replace with render product page


@admin_bp.route("/delete_product", methods=["GET", "POST"])
def deleteProduct():
    if "pro_ID" in request.form:
        connection = getConnection()
        cursor = connection.cursor()

        product_id = request.form.get('pro_ID')

        try:
            # Start a transaction
            connection.begin()

            # Delete related data first (Orders, Cart, Balance_Changes, Reviews) 
            # Used as a primary key so we cannot set to null :(
            # Maybe point to default deleted object product
            delete_orders_sql = "UPDATE Orders SET pro_ID = 0 WHERE pro_ID = %s"
            cursor.execute(delete_orders_sql, (product_id,))

            delete_carts_sql = "DELETE FROM Cart WHERE pro_ID = %s"
            cursor.execute(delete_carts_sql, (product_id,))

            delete_balcha_sql = "DELETE FROM Balance_Changes WHERE pro_ID = %s"
            cursor.execute(delete_balcha_sql, (product_id,))

            delete_reviews_sql = "DELETE FROM Reviews WHERE pro_ID = %s"
            cursor.execute(delete_reviews_sql, (product_id,))

            # Then delete the product
            delete_product_sql = "DELETE FROM Products WHERE pro_ID = %s"
            cursor.execute(delete_product_sql, (product_id,))

            # Commit changes to the database
            connection.commit()

            return redirect(url_for('admin.admin'))  # Redirect to main admin page after successful deletion

        except Exception as e:
            # Handle exceptions (e.g., database errors)
            print(f"Error deleting product: {e}")
            connection.rollback()
            return "Error deleting product", 500
        finally:
            # Close the database connection
            connection.close()


@admin_bp.route("/product", methods=["GET", "POST"])
def product():
    connection = getConnection()
    cursor = connection.cursor()
    sql = "SELECT * FROM Products WHERE pro_ID = %s"
    cursor.execute(sql, (session["pro_ID"]))
    result = cursor.fetchone()
    print(result, file=sys.stderr)
    sql = "SELECT * FROM Reviews WHERE pro_ID = %s"
    cursor.execute(sql, (session["pro_ID"]))
    reviews = list(cursor.fetchall())
    connection.close()
    return render_template("AdmProduct.html", title="Admin Product", product = result, reviews = reviews)


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

        connection = getConnection()
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

        connection = getConnection()
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

        connection = getConnection()
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

        connection = getConnection()
        cursor = connection.cursor()

        product_id = request.form['pro_ID']
        qty_change = int(request.form['qty_change'])
        old_qty = int(request.form['old_qty'])
        new_qty = old_qty + qty_change
        if new_qty < 0:
            new_qty = 0

        sql = "UPDATE Products SET qty = %s WHERE pro_ID = %s"
        params = (new_qty, product_id)

        cursor.execute(sql, params)
        result = cursor.fetchone()
        #print(result, file=sys.stderr)


        sql = "SELECT change_ID FROM Balance_Changes ORDER BY change_ID  DESC LIMIT 0,1" # select the highest current id
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result, file=sys.stderr)

        if result == None:  # if the result is NONE, then the database is empty
            newId = 0     # if the database is empty, just set result to -1 (the id will then be 0)
        else:
            newId = int(result["change_ID"]) + 1 
        #print(newId, file=sys.stderr)

        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        #print(current_datetime)

        sql = "INSERT INTO Balance_Changes (change_ID, is_purchase, qty, date, `acc_e-mail`, pro_ID) VALUES (" + str(newId) + ", 0, " + str(qty_change) + ", '" + str(current_datetime) + "', '" + session['e-mail'] + "', " + str(product_id) + ")"
        cursor.execute(sql)

        connection.commit()
        connection.close()

        return redirect(url_for("admin.product"))       # Product quantity updated successfully
    else:
        return redirect(url_for('admin.admin'))         # Product not found


@admin_bp.route('/change_image', methods=["GET", "POST"])
def change_image():
    if "pro_ID" in request.form and "newImg" in request.form:

        connection = getConnection()
        cursor = connection.cursor()

        product_id = request.form['pro_ID']
        newImg = request.form['newImg']

        sql = "UPDATE Products SET pro_img = %s WHERE pro_ID = %s"
        params = (newImg, product_id)

        cursor.execute(sql, params)
        result = cursor.fetchone()
        print(result, file=sys.stderr)
        connection.commit()
        connection.close()

        return redirect(url_for("admin.product"))       # Product image updated successfully
    else:
        return redirect(url_for('admin.admin'))         # Product not found


@admin_bp.route('/upload_image', methods=["GET", "POST"])
def upload_image():
    if "pro_ID" in request.form and "file" in request.files:

        file = request.files['file']

        if file.filename == "":
            return redirect(url_for('admin.admin'))     # No selected file

        '''
        # Get the UPLOAD_FOLDER configuration value from current_app.config
        UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

        file_path = os.path.join(app.root_path, 'static', UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(file_path)
        '''

        return redirect(url_for("admin.product"))       # Product image uploaded successfully
    else:
        return redirect(url_for('admin.admin'))         # Product/Image not found

@admin_bp.route("/enterOrderHistory", methods=["GET", "POST"])
def enterOrderHistory():
    try:
        # Connect to the database
        connection = pymysql.connect(**connection_input)
        
        #take order data from database
        with connection.cursor() as cursor:
            
            #take order_IDs -->
            sql_query = "SELECT * FROM mydb.Orders;"
            cursor.execute(sql_query)

            # Fetch results
            rows = cursor.fetchall()

            #create list of all order_IDs
            order_IDs = []
            if rows:
                
                for row in rows:
                    if not (row["ord_ID"] in order_IDs):
                        order_IDs.append(row["ord_ID"])
            else:
                print("enterOrderHistory, get order_IDs: No data found.")
            
            print("order_IDs: ", order_IDs)
            #<--
                
            #take and assemble parts of orders (from heavily modified chatGPT response) -->
            orders = []
            for ID in order_IDs:
                new_order = []
                ord_ID = ID
                total_qty = 0
                total_price = 0
                acc_email = ""

                sql_query = "SELECT * FROM mydb.Orders WHERE ord_ID = %s"
                cursor.execute(sql_query, (ID,))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        total_qty = total_qty + row["qty"]
                        total_price = total_price + row["price"]
                        acc_email = row["acc_e-mail"]

                else:
                    print("enterOrderHistory, get order parts: No data found.")
                
                new_order = {"ord_ID": ord_ID, "total_qty": total_qty, "total_price": total_price, "acc_e-mail":acc_email}    
                print("new_order ID: ", ID, " with content: ", new_order)
                orders.append(new_order)
                
            #<--

        print("orders: ", orders)
        # Commit changes to the database
        connection.commit()
    
        # Close connection
        connection.close()
        #print('Login: Connection closed')

        return render_template("AdmOrderHistory.html", title="Order History", orders = orders)

    except pymysql.Error as e:
        print('Login: Error connecting to MySQL:', e)
        return redirect(url_for("admin.admin"))
    

@admin_bp.route("/enterOrder", methods=["POST"])
def enterOrder():
    if "order_ID" in request.form:
        currID = request.form['order_ID']
        session['order_ID'] = currID
        print("order_ID:  ", currID, " ———— file=sys.stderr: ",  file=sys.stderr)
        return redirect(url_for("admin.order"))
    else:
        return redirect(url_for("admin.admin"))