from flask import Blueprint, render_template, request, redirect
import hashlib
from models.models import *

pages = Blueprint('pages', __name__, template_folder='templates')

@pages.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    login = request.form['login']
    password = request.form['pass']
    passw = hashlib.md5(password.encode())
    rendered_pass = passw.hexdigest()
    role = request.form['role']
    if role == "sheffofprojects":
        data_workers = sessions.query(sheffofprojects, positions).join(positions).filter(sheffofprojects.Login == login).first()
        return redirect('/admin/reg_shefforg')


@pages.route('/admin/reg_shefforg', methods=['GET', 'POST'])
def reg_shefforg():
    if request.method == "GET":
        return render_template("registration.html")

