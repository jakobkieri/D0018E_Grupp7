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
        userMail = request.form["e-mail"]
        password = request.form["password"]

        #dockerCheckCredentials puts data into session if credentials are correct
        if not dockerCheckCredentials(userMail, password):
            return render_template("login.html", error="Invalid email or password")

        print("session data: ", session)
        return redirect(url_for("role_redirect"))
    
    # If it's a GET request, render the login form
    return render_template('login.html', error=None)


#redirects depending on the role of user
@app.route("/role_redirect")
def role_redirect():
    if "acc_name" in session:
        #session["admin"] is defined as a boolean in database
        if session["admin"]:
            return redirect(url_for("admin.admin"))
        else:
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


#(code given by chatGPT but heavily modified)
#it checks if credentials are correct. If they are correct, it adds following to session: user_id (mail), username (username), role (1 if admin)
def dockerCheckCredentials(givenMail, givenPassword):
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
            #sql_query = "INSERT INTO mydb.Accounts VALUES ('bingusBoss@hotmail.com', 'bingusBoss', 'bingusBoss', '2024-02-15', 1);"
            #cursor.execute(sql_query)

            
            #take data from database, specifically mydb.Accounts
            sql_query = "SELECT * FROM mydb.Accounts;"
            cursor.execute(sql_query)

            #validCredentials is returned False if it is not verified by finding mathcing credentials
            validCredentials = False

            # Fetch results
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    if(givenMail == row[0] and givenPassword == row[2]):
                        validCredentials = True

                        session['e-mail'] = row[0]     
                        session["acc_name"] = row[1]
                        session["admin"] = row[4]
                        
            else:
                print("No data found.")
                return validCredentials

        # Commit changes to the database
        connection.commit()
    
        # Close connection
        connection.close()
        print('Connection closed')

        return validCredentials

    except pymysql.Error as e:
        print('Error connecting to MySQL:', e)

# run on
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)