import os

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from segmentation_alg import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/fernando/Documentos/UFT/9 Período/Estagio Supervisionado/Estagio'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'tiff'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file(name = None):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
            return redirect(url_for('imagem_upada', filename=filename))
    return render_template("upload.html", name=name) 

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploaded/<filename>')
def imagem_upada(filename):
    img_seg = main(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], img_seg)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
