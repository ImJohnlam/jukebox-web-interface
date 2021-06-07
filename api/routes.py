import io
import random

import os
from flask import Flask, flash, request, redirect, url_for, session, send_file, jsonify, Response
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import json
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from filters import Filter
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
    filter_options = json.loads(request.form['filters'])
    logger.info(f'files ({len(request.files)}) {request.files}')
    logger.info(f'filters {type(filter_options)} {filter_options}')

    filename = secure_filename(file.filename)
    destination = os.path.join(target, filename)
    file.save(destination)
    # session['uploadFilePath']=destination
    response = "Whatever you wish to return"
    path = os.path.join(UPLOAD_FOLDER, 'test_docs', filename)
    logger.info('about to return: ' + destination)
    
    
    logger.info('before apply')
    if filter_options:
        filter_class = Filter.get_filter_class(filter_options['name'])
        filter = filter_class(destination, target, filename, filter_options['params'])
        output = filter.apply()
        logger.info(filter_options['params'])
    else:
        output = destination
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
                    'value': 4000.,
                    'upper_bound': 22090.,
                    'lower_bound': 8.
                }
            ]
        },
        {
            'name': 'Elliptic Filter',
            'params': [
                {
                    'type': 'numeric',
                    'name': 'Cutoff Frequency',
                    'value': 4000.,
                    'upper_bound': 22090.,
                    'lower_bound': 8.
                },
                {
                    'type': 'numeric',
                    'name': 'Max Ripple',
                    'value': 5.
                },
                {
                    'type': 'numeric',
                    'name': 'Min Attenuation',
                    'value': 40.
                }
            ]
        }
    ]}


@app.route('/sample_info')
def get_sample_info():
    logger.info("hit sample info")
    return {'samples': [
        {
            'name': 'Pink Panther Example',
            'artist': 'Hari',
            'src': 'pink_panther.wav'
        },
        {
            'name': 'Piano Example',
            'artist': 'John',
            'src': 'piano.wav'
        }
    ]}

@app.route('/sample/<src>')
def get_sample(src):
    path = os.path.join(SAMPLES_FOLDER, src)
    logger.info(f'get sample, path={path}')
    return send_file(path, as_attachment=True)

# @app.route('/imagetest', methods=['POST'])
# def get_img():
#     target = os.path.join(UPLOAD_FOLDER, 'spectrograms')
#     if not os.path.isdir(target):
#         os.mkdir(target)

#     logger.info(f'imagetest target={target}')
#     logger.info(f'{request.files}')
#     file = request.files['file']
#     filename = secure_filename(file.filename)
#     logger.info(f'filename={filename}')

#     destination = os.path.join(target, filename)
#     file.save(destination)


#     return send_file('cat.jpg', as_attachment=True)

@app.route('/get_image', methods=['POST'])
def get_image():
    target = os.path.join(UPLOAD_FOLDER, 'spectrograms')
    if not os.path.isdir(target):
        os.mkdir(target)

    logger.info(f'get_image target={target}')
    logger.info(f'{request.files}')
    file = request.files['file']
    filename = secure_filename(file.filename)
    logger.info(f'filename={filename}')

    destination = os.path.join(target, filename)
    file.save(destination)

    """
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    
    """

    """
    sample_rate, samples = wavfile.read(destination)
    frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

    img_filename = os.path.join(target, 'spectrogram.png')
    # plt.figure()
    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    # plt.show()
    #saves spectogram as image
    plt.savefig(img_filename)
    plt.close()
    """
    samplingFrequency, signalData = wavfile.read(destination)

    img_filename = os.path.join(target, 'spectrogram.png')
    plt.title('Spectrogram')    
    Pxx, freqs, bins, im = plt.specgram(signalData,Fs=samplingFrequency,NFFT=512)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.xlim(left=0,right=17)
    plt.savefig(img_filename)
    plt.close()

    if request.args.get('type') == '1':
       filename = 'ok.gif'
    else:
       filename = 'error.gif'
    return send_file(img_filename, mimetype='image/gif')

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0", use_reloader=False)


CORS(app, expose_headers='Authorization')
