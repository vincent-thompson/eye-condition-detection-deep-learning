from flask import Flask

# from models import ___

app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.jpeg']
app.config['UPLOAD_PATH'] = '/Users/vinnythompson/Documents/Metis/project5/website/personal_website/static/uploads'

from personal_website import routes