from flask import Flask, render_template, redirect, request, url_for, Blueprint, session
from Customer.customer import customer_bp
from Admin.admin import admin_bp
import pymysql

#from itertools import count (???)

app = Flask(__name__)
app.secret_key = "bingus" #secret key for sessions


# Fixing Blueprints     ERROR!?
app.register_blueprint(customer_bp, url_prefix='/customer')
app.register_blueprint(admin_bp, url_prefix='/admin')


'''
@app.route('/')
def index():
    return render_template('login.html')
'''

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        return redirect(url_for('test'))
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        #TODO: (MongoDB -> MySQL)

        '''
        cursor = accounts.find()
        for occ in cursor:
            print("occurences: ")
            print(occ)

        user_tuple = accounts.find_one({"Username": username, "Password":password})
        if not user_tuple:
            return render_template("login.html", error="Invalid username or password")
        '''

        # Sets session data for data regarding that user, before sending onwards
        #print("tuple: ", user_tuple)
        '''
        session['user_id'] = str(user_tuple["_id"])       
        session["username"] = user_tuple["Username"]
        session["role"] = user_tuple["Role"]
        '''

        return redirect(url_for("role_redirect"))

        
    
    # If it's a GET request, render the login form
    return render_template('login.html', error=None)


#redirects depending on the role of user
@app.route("/role_redirect")
def role_redirect():
    if "username" in session:
        role = session["role"]
        if role == "admin":
            return redirect(url_for("admin.admin"))
        if role == "customer":
            return redirect(url_for("customer.customer"))
    return redirect(url_for("login"))


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == "POST":
        return redirect(url_for('home'))
    return render_template('test.html')


@app.route('/img', methods=['POST', 'GET'])
def show_img():
    return render_template("dis_img.html")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()                     # clears everything from session
    return redirect(url_for("login"))


#testing function
def dockerConnect():
    # Replace these values with your actual database connection details
    host = '172.17.0.2'  # or the IP address of your Docker container
    port = 3306         # port number
    user = 'root'
    password = 'bingus'
    database = 'mydb'

    try:
        # Connect to the database
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
    
        with connection.cursor() as cursor:
            #insert test data into database
            #sql_query = "INSERT INTO mydb.Accounts VALUES ('bingus@hotmail.com', 'bingus', 'bingus', '2024-02-01', 0);"
            #cursor.execute(sql_query)

            
            #take data from database, specifically mydb.Accounts
            sql_query = "SELECT * FROM mydb.Accounts;"
            cursor.execute(sql_query)

            # Fetch and print results
            rows = cursor.fetchall()
            if rows:
                print("Fetched data:")
                for row in rows:
                    print(row)
            else:
                print("No data found.")

        # Commit changes to the database
        connection.commit()
    
        # Close connection
        connection.close()
        print('Connection closed')

    except pymysql.Error as e:
        print('Error connecting to MySQL:', e)

# run on
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)