import os
from flask import Flask, flash, request, redirect, url_for, session, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import json
import time
import matplotlib.pyplot as plt
from filters import LowPassFilter, QuieterFilter
from pydub import AudioSegment

from scipy import signal
from scipy.io import wavfile


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

UPLOAD_FOLDER = 'uploads'
SAMPLES_FOLDER = 'samples'
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
    # filter = QuieterFilter(destination)
    output = filter.apply()
    #return send_file(quieter(destination), as_attachment=True)
    return send_file(output,
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

@app.route('/sample_info')
def get_sample_info():
    logger.info("hit sample info")
    return {'samples': [
        {
            'name': 'Example Song',
            'artist': 'Example Artist',
            'src': 'example.wav'
        }
    ]}

@app.route('/sample/<src>')
def get_sample(src):
    path = os.path.join(SAMPLES_FOLDER, src)
    logger.info(f'get sample, path={path}')
    return send_file(path, as_attachment=True)

@app.route('/imagetest', methods=['POST'])
def get_img():
    target = os.path.join(UPLOAD_FOLDER, 'spectrograms')
    if not os.path.isdir(target):
        os.mkdir(target)

    logger.info(f'imagetest target={target}')
    logger.info(f'{request.files}')
    file = request.files['file']
    filename = secure_filename(file.filename)
    logger.info(f'filename={filename}')

    destination = os.path.join(target, filename)
    file.save(destination)


    return send_file('cat.jpg', as_attachment=True)

@app.route('/get_image', methods=['POST'])
def get_image():
    target = os.path.join(UPLOAD_FOLDER, 'spectrograms')
    if not os.path.isdir(target):
        os.mkdir(target)

    logger.info(f'imagetest target={target}')
    logger.info(f'{request.files}')
    file = request.files['file']
    filename = secure_filename(file.filename)
    logger.info(f'filename={filename}')

    destination = os.path.join(target, filename)
    file.save(destination)

    sample_rate, samples = wavfile.read(destination)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    img_filename = os.path.join(target, 'spectrogram.png')
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    # plt.show()
    #saves spectogram as image
    plt.savefig(img_filename)

    if request.args.get('type') == '1':
       filename = 'ok.gif'
    else:
       filename = 'error.gif'
    return send_file(img_filename, mimetype='image/gif')

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)


CORS(app, expose_headers='Authorization')
