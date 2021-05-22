from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
import requests
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        return path

        return 'ok'


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


