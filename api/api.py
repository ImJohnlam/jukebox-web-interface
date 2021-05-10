import os
from flask import Flask, flash, request, redirect, url_for, session, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import json
import time

from pydub import AudioSegment


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/time')
def test():
    return {'time': time.time()}

def quieter(d):
    song = AudioSegment.from_wav(d)

    # reduce volume by 10 dB
    song_10_db_quieter = song - 10

    # but let's make him *very* quiet
    song = song - 30

    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    filename = 'quieter.wav'
    newd=os.path.join(target, filename)
    # save the output
    song.export(newd, "wav")
    return newd

@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")    

    file = request.files['file']
    filters = json.loads(request.form['filters'])
    logger.info(f'files ({len(request.files)}) {request.files}')
    logger.info(f'filters {type(filters)} {filters}')

    filename = secure_filename(file.filename)
    destination=os.path.join(target, filename)
    file.save(destination)
    # session['uploadFilePath']=destination
    response="Whatever you wish too return"
    path = os.path.join(UPLOAD_FOLDER,'test_docs', filename)
    logger.info('about to return: ' + destination)

    

    # return send_file(destination, as_attachment=True)
    return send_file(quieter(destination), as_attachment=True)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)
    

CORS(app, expose_headers='Authorization')
