from flask import Flask, render_template, redirect, request, url_for, Blueprint, session
from Customer.customer import customer_bp
from Admin.admin import admin_bp

#from itertools import count (???)

app = Flask(__name__)


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


# run on
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)