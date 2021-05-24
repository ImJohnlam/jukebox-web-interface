import os
from flask import Flask, flash, request, redirect, url_for, session, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import json
import time
import matplotlib.pyplot as plt
from filters import LowPassFilter, QuieterFilter, EllipticFilter
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


@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    target = os.path.join(UPLOAD_FOLDER, 'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")

    file = request.files['file']
    filters = json.loads(request.form['filters'])
    logger.info(f'files ({len(request.files)}) {request.files}')
    logger.info(f'filters {type(filters)} {filters}')

    filename = secure_filename(file.filename)
    destination = os.path.join(target, filename)
    file.save(destination)
    # session['uploadFilePath']=destination
    response = "Whatever you wish to return"
    path = os.path.join(UPLOAD_FOLDER, 'test_docs', filename)
    logger.info('about to return: ' + destination)
    filter = LowPassFilter(destination, target, filename)
    ell_filter = EllipticFilter(destination, target, file)
    # filter = QuieterFilter(destination)
    output = filter.apply()
    ell_output = ell_filter.apply()
    #return send_file(quieter(destination), as_attachment=True)
    return send_file(ell_output,
                     as_attachment=True)


@app.route('/filters')
def get_filters():
    return {'filters': [
        {
            'name': 'Low Pass Filter',
            'params': [
                {
                    'type': 'numeric',
                    'name': 'Cutoff Frequency',
                    'value': 8000.,
                    'upper_bound': 22090.,
                    'lower_bound': 8.
                }
            ]
        }
    ]}
    
if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)


CORS(app, expose_headers='Authorization')
