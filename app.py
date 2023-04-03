from flask import Flask
from dotenv import load_dotenv
from pathlib import Path
from os import getenv, getcwd
import os

from models.database import init_db
from routes import pages

load_dotenv()
FULL_PATH_FOLDER = Path(getcwd(), 'static', 'files')
UPLOAD_FOLDER = Path('/static', 'files')
app = Flask(__name__)
app.register_blueprint(pages)
init_db()
app.secret_key = os.urandom(20).hex()


if __name__ == '__main__':
    app.run(debug=True, port=(getenv('PORT') or 5000))
