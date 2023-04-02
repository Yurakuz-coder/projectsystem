from flask import Blueprint, render_template

pages = Blueprint('pages', __name__, template_folder='templates')

@pages.route('/', methods=['GET'])
def index():
    return render_template("index.html")
