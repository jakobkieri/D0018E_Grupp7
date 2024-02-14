from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
import pymysql
import sys
admin_bp = Blueprint('admin', __name__, 
                        template_folder='templates',
                        static_folder='static')



@admin_bp.route("/", methods=["GET", "POST"])
def admin():
    return render_template("AdmMain.html")



@admin_bp.route("/add_product", methods=["GET", "POST"])
def addProduct():
    connection = pymysql.connect(host='localhost',
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