"""
    ################################################################################
    Flask application 
    ################################################################################


    @Universidad: Javeriana Cali
    @Facultad: Ingenieri'a y Ciencias
    @Curso: Ana'lisis y Computacio'n Nume'rica
    @Tema: Factorizacio'n SVD
        
    @Autor:
        - Geiler Hipia Meji'a
        - Jair Narvaez Chamarro
        - Juan Villaroel Luengas
        - Laura Benavides Ocampo
        
    @Docente: Andres Felipe Amador Rodriguez
    @Versio'n: 1.0



"""
from bz2 import compress
from flask import (
    Flask, redirect, url_for,
    render_template, session,
    request
    )
import string, random
from svd import *
from werkzeug.utils import secure_filename 

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 32))
app.config['UPLOAD_FOLDER'] = 'static/images'

__m = Manager()


@app.route('/')
def index():
    
    srcLastImageA, srcLastImageB = __m.getSrcLastImages()
    return render_template('index.html',
                            userA = __m.userA,
                            userB = __m.userB,
                            srcLastImageA = srcLastImageA,
                            srcLastImageB = srcLastImageB)

@app.route('/send-image/<string:id>', methods = ['POST', 'GET'])
def sendImage(id):
    if request.method == 'POST':

        try:
            k = int(request.form.get('inputK' + id))
        except:
            k = 100

        file = request.files['inputImage' + id]
        filename = secure_filename(file.filename)

        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
            app.config['UPLOAD_FOLDER'],
            filename)

        file.save(path) # Then save the file
        print("[",path,"]")
        compress = None
        if request.form['send-image'] == 'send-original':
            compress = False
        elif request.form['send-image'] == 'send-compress':
            compress = True
        
        if compress != None:
            __m.send(from_to = id,
                    path = path,
                    compress = compress,
                    k = k)

    return redirect(url_for('index'))


@app.route('/reset')
def reset():
    global __m
    __m = Manager()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True)