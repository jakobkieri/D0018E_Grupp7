from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        return redirect(url_for('test'))
    return render_template('home.html')


@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == "POST":
        return redirect(url_for('home'))
    return render_template('test.html')


@app.route('/img', methods=['POST', 'GET'])
def show_img():
    return render_template("dis_img.html")

#run on
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)