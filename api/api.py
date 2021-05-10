import os
from flask import Flask, flash, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import time

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/time')
def test():
    return {'time': time.time()}

@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    # session['uploadFilePath']=destination
    response="Whatever you wish too return"
    path = os.path.join(UPLOAD_FOLDER,'test_docs', filename)
    logger.info('about to return: ' + destination)
    return send_file(destination, as_attachment=True)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)
    

CORS(app, expose_headers='Authorization')
