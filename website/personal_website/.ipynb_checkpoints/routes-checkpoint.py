import os, shutil
import imghdr
from flask import render_template, url_for, request, redirect, flash, abort, send_from_directory
from personal_website import app
from werkzeug.utils import secure_filename







def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route("/")
@app.route("/home")
def home():
	files = os.listdir(app.config['UPLOAD_PATH'])
	return render_template('home.html', files=files)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/", methods = ['POST'])
@app.route("/home", methods = ['POST'])
def upload_file():
	folder = app.config['UPLOAD_PATH']
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        print(uploaded_file.filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or file_ext != validate_image(uploaded_file.stream):
            abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            return redirect(url_for('home'))

@app.route('/uploads/<filename>')
def upload(filename):
	try:
		return send_from_directory(app.config['UPLOAD_PATH'], filename)
	except FileNotFoundError:
		abort(404)