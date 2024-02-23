from flask import Flask, render_template, redirect, request, url_for, Blueprint, session
from Customer.customer import customer_bp
from Admin.admin import admin_bp
import pymysql
import hashlib

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

#linux
connection_input = {'host': '172.17.0.2','port': 3306, 'user': 'root','password': 'bingus','database': 'mydb'}

#other (souce: Marcus)
#connection_input = {"host":"localhost","user":'root',"password":'bingus',"database":'mydb',"charset":'utf8mb4',"cursorclass":pymysql.cursors.DictCursor}

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        return redirect(url_for('test'))
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        userMail = request.form["e-mail"]
        
        #sha3-256 digest of password (from chatGPT) to check with stored hash of password
        password = (request.form["password"]).encode('utf-8')
        hash_object = hashlib.sha3_256()
        hash_object.update(password)
        password = hash_object.hexdigest()
        #---

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

@app.route('/createAccount', methods=['POST', 'GET'])
def createAccount():
    # If it's a GET request, render the login form
    if request.method=="GET":
        return render_template("createAccount.html")
    
    #"POST": proceed with account creation
    newMail = request.form["e-mail"]
        
        
    if databaseFindEmail(newMail):
        return render_template("createAccount.html", error="Email not available")
        

    try:
        # Connect to the database and put in new account
        connection = pymysql.connect(**connection_input)
        with connection.cursor() as cursor:
            sql_query = "INSERT INTO mydb.Accounts VALUES (%s, %s, %s, %s, %s);"

            #sha3-256 digest of password (from chatGPT) to check with stored hash of password
            password = (request.form["password"]).encode('utf-8')
            hash_object = hashlib.sha3_256()
            hash_object.update(password)
            password = hash_object.hexdigest()
            #---

            values = (request.form["e-mail"], request.form["acc_name"], password, request.form["date_created"], request.form["admin"])
            cursor.execute(sql_query, values)

            #testing -->
            #take data from database, specifically mydb.Accounts
            sql_query = "SELECT * FROM mydb.Accounts;"
            cursor.execute(sql_query)

            # Fetch results
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print("Found:  ",  row)

            #<--
    
            # Commit changes to the database
            connection.commit()

            # Close connection
            connection.close()

            #the specifics of message sent back is unimportant, it can be changed without changing
            return render_template("login.html", message="Account Created Successfully")

    except pymysql.Error as e:
        print('Account Creation: Error connecting to MySQL:', e)
        return render_template("login.html", error="account creation error")



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

def databaseFindEmail(givenMail):
    try:
        # Connect to the database
        connection = pymysql.connect(**connection_input)
        with connection.cursor() as cursor:
            #take data from database, specifically mydb.Accounts
            sql_query = "SELECT * FROM mydb.Accounts;"
            cursor.execute(sql_query)

            #validCredentials is returned False if it is not verified by finding mathcing credentials
            alreadyExists = False

            # Fetch results
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    if(givenMail == row[0]):
                        alreadyExists = True

                        session['e-mail'] = row[0]     
                        session["acc_name"] = row[1]
                        session["admin"] = row[4]
                        
            else:
                print("Account Creation: No data found.")

        # Commit changes to the database
        connection.commit()
    
        # Close connection
        connection.close()

        return alreadyExists

    except pymysql.Error as e:
        print('Account Creation: Error connecting to MySQL:', e)

        



#(code given by chatGPT but heavily modified)
#it checks if credentials are correct. If they are correct, it adds following to session: user_id (mail), username (username), role (1 if admin)
def dockerCheckCredentials(givenMail, givenPassword):
    try:
        # Connect to the database
        connection = pymysql.connect(**connection_input)
    
        with connection.cursor() as cursor:
            ##insert test data into database -->
            ##sha3_256 of "bingusBoss" = "8c3307a4ed0336f039a2f295db21c4c664088ec1aa6e0a8961b68fb86556936d"
            #sql_query = "INSERT INTO mydb.Accounts VALUES ('bingusBoss@hotmail.com', 'bingusBoss', '8c3307a4ed0336f039a2f295db21c4c664088ec1aa6e0a8961b68fb86556936d', '2024-02-15', 1);"
            #cursor.execute(sql_query)
            #
            ##sha3_256 of "bingus" = "b7171fb59379c940a27e2c7f4bf333797861eb30aed93bae8cc32e1c38a671d2"
            #sql_query = "INSERT INTO mydb.Accounts VALUES ('bingus@hotmail.com', 'bingus', 'b7171fb59379c940a27e2c7f4bf333797861eb30aed93bae8cc32e1c38a671d2', '2024-02-1', 0);"
            #cursor.execute(sql_query)
            #
            #sql_query = "INSERT INTO `mydb`.`Products` (`pro_ID`, `pro_name`, `pro_img`, `pro_info`, `qty`, `price`) VALUES ('0', 'Attans Banan', 'varukorg.png', 'Det är en attans banan', '0', '500');"
            #cursor.execute(sql_query)
            #sql_query = "INSERT INTO `mydb`.`Products` (`pro_ID`, `pro_name`, `pro_img`, `pro_info`, `qty`, `price`) VALUES ('1', 'Holy Goblin Banan', 'profile_a.png', 'Det är en holy goblin banan.', '10', '300');"
            #cursor.execute(sql_query)
            ##<--
            
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
                print("Login: No data found.")

        # Commit changes to the database
        connection.commit()
    
        # Close connection
        connection.close()
        #print('Login: Connection closed')

        return validCredentials

    except pymysql.Error as e:
        print('Login: Error connecting to MySQL:', e)

# run on
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)