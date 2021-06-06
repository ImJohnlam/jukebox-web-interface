from abc import ABC, abstractmethod
import contextlib
import wave
import os
import numpy as np
import math
from pydub import AudioSegment
from scipy import signal


class Filter(ABC):
    @abstractmethod
    def apply(self):
        pass

    def interpret_wav(self, raw_bytes, n_frames, n_channels, sample_width, interleaved=True):
        """
        from http://stackoverflow.com/questions/2226853/interpreting-wav-data/2227174#2227174
        """
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


class QuieterFilter(Filter):
    def __init__(self, destination) -> None:
        self.destination = destination

    def apply(self):
        song = AudioSegment.from_wav(self.destination)

        # reduce volume by 10 dB
        song_10_db_quieter = song - 10

        # but let's make him *very* quiet
        song = song - 30

        target = os.path.join('uploads', 'test_docs')
        filename = 'quieter.wav'
        newd = os.path.join(target, filename)
        # save the output
        song.export(newd, "wav")
        return newd


class LowPassFilter(Filter):
    def __init__(self, wav_file, target, filename):
        self.wav_file = wav_file
        self.target = target
        self.filename = filename

    def apply(self):
        cutOffFrequency = 4000.0
        outname = os.path.join(os.path.join(
            self.target, "filtered_" + self.filename))
        with contextlib.closing(wave.open(self.wav_file, 'rb')) as spf:
            sampleRate = spf.getframerate()
            ampWidth = spf.getsampwidth()
            nChannels = spf.getnchannels()
            nFrames = spf.getnframes()

            # Extract Raw Audio from multi-channel Wav File
            sig = spf.readframes(nFrames * nChannels)
            spf.close()
            channels = self.interpret_wav(
                sig, nFrames, nChannels, ampWidth, True)

            # get window size
            # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
            freqRatio = (cutOffFrequency / sampleRate)
            N = int(math.sqrt(0.196196 + freqRatio ** 2) / freqRatio)

            # Use moving average (only on first channel)
            filtered = self.running_mean(channels[0], N).astype(channels.dtype)

            wav_file = wave.open(outname, "w")
            wav_file.setparams((1, ampWidth, sampleRate, nFrames,
                                spf.getcomptype(), spf.getcompname()))
            wav_file.writeframes(filtered.tobytes('C'))
            wav_file.close()
            return outname

    def running_mean(self, x, windowSize):
        """
        from http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
        """
        cumulative_sum = np.cumsum(np.insert(x, 0, 0))
        return (cumulative_sum[windowSize:] - cumulative_sum[:-windowSize]) / windowSize


class EllipticFilter(Filter):
    def __init__(self, wav_file, target, filename):
        self.wav_file = wav_file
        self.target = target
        self.filename = filename

    def apply(self):
        outname = os.path.join(os.path.join(
            self.target, "ell_filtered_" + self.filename))
        with contextlib.closing(wave.open(self.wav_file, 'rb')) as spf:
            sampleRate = spf.getframerate()
            ampWidth = spf.getsampwidth()
            nChannels = spf.getnchannels()
            nFrames = spf.getnframes()

            # Extract Raw Audio from multi-channel Wav File
            sig = spf.readframes(nFrames * nChannels)
            spf.close()
            channels = self.interpret_wav(
                sig, nFrames, nChannels, ampWidth, True)

            # TODO: Take these as params from user
            cutoff_frequency = 4000.0
            max_ripple = 5
            min_attenuation = 40

            sos = signal.ellip(4, max_ripple, min_attenuation, cutoff_frequency,
                               fs=sampleRate, output='sos')
            filtered = signal.sosfilt(sos, channels).astype(channels.dtype)

            wav_file = wave.open(outname, "w")
            wav_file.setparams((1, ampWidth, sampleRate, nFrames,
                                spf.getcomptype(), spf.getcompname()))
            wav_file.writeframes(filtered.tobytes('C'))
            wav_file.close()
            return outname
