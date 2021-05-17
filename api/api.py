import os
from flask import Flask, flash, request, redirect, url_for, session, send_file, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import logging
import json
import time
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import math
import contextlib

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


# from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
def running_mean(x, windowSize):
    cumulative_sum = np.cumsum(np.insert(x, 0, 0))
    return (cumulative_sum[windowSize:] - cumulative_sum[:-windowSize]) / windowSize


# from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

    if sample_width == 1:
        dtype = np.uint8  # unsigned char
    elif sample_width == 2:
        dtype = np.int16  # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)
    return channels


def apply_low_pass_filter(d, target, filename):
    cutOffFrequency = 4000.0
    outname = os.path.join(os.path.join(target, "filtered_" + filename))
    with contextlib.closing(wave.open(d, 'rb')) as spf:
        sampleRate = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()

        # Extract Raw Audio from multi-channel Wav File
        signal = spf.readframes(nFrames * nChannels)
        spf.close()
        channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)

        # get window size
        # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
        freqRatio = (cutOffFrequency / sampleRate)
        N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio)

        # Use moving average (only on first channel)
        filtered = running_mean(channels[0], N).astype(channels.dtype)

        wav_file = wave.open(outname, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filtered.tobytes('C'))
        wav_file.close()
        return wav_file


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
    response = "Whatever you wish to return"
    path = os.path.join(UPLOAD_FOLDER,'test_docs', filename)
    logger.info('about to return: ' + destination)

    # return send_file(destination, as_attachment=True)
    return send_file(apply_low_pass_filter(destination), as_attachment=True)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)
    

CORS(app, expose_headers='Authorization')
