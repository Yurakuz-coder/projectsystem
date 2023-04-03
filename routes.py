from flask import Blueprint, render_template, request
import hashlib


pages = Blueprint('pages', __name__, template_folder='templates')

@pages.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    login = request.form.get['login']
    password = request.form['pass']
    passw = hashlib.md5(password.encode())
    rendered_pass = passw.hexdigest()

