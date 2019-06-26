import os

from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from segmentation_alg import *
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = '/home/fernando/Documentos/UFT/9 Período/Estagio Supervisionado/Estagio'
UPLOAD_FOLDER_STATIC = '/home/fernando/Documentos/UFT/9 Período/Estagio Supervisionado/Estagio/static'
# UPLOAD_FOLDER_IMAGENS = '/home/fernando/Documentos/UFT/9 Período/Estagio Supervisionado/Estagio/imagens'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'tiff'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_STATIC'] = UPLOAD_FOLDER_STATIC
# app.config['UPLOAD_FOLDER_IMAGENS'] = UPLOAD_FOLDER_IMAGENS



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
            # name of image
            filename = secure_filename(file.filename)
            
            # open parameter
            openpar = request.form['open']

            # segmentation parameter
            segpar = request.form['seg']
            

            file.save(os.path.join(UPLOAD_FOLDER_STATIC, filename))
            return redirect(url_for('uploaded_image', filename=filename, openpar=openpar, segpar=segpar))

    return render_template("upload.html", name=name) 


@app.route('/uploaded/<filename>')
def send_image(filename):
    return send_from_directory(UPLOAD_FOLDER, "resultado_final.png")


@app.route('/uploaded/<filename>', methods=['GET', 'POST'])
@app.route('/uploaded/<filename>/<int:openpar>', methods=['GET', 'POST'])
@app.route('/uploaded/<filename>/<int:openpar>/<int:segpar>', methods=['GET', 'POST'])
def uploaded_image(filename, openpar=3, segpar=1):
    
    main(filename, openpar, segpar)
    res = "resultado"+str(openpar)+str(segpar)+filename
    return render_template("gallery.html", imagem=filename, resultado=res, es=openpar, seg=segpar)
    
    
if __name__ == "__main__":
    # Não faço a mínima ideia do que seja isso
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)

    app.run(port=5000, debug=True, use_reloader=True)

