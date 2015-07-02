# -*- coding: utf-8 -*-


import os
from ctypes import CFUNCTYPE, cdll
from contextlib import contextmanager

try:
    import pyaudio
except ImportError:
    print('Install the portaudio library and execute the next command with pip')
    print('pip install --allow-external pyaudio --allow-unverified pyaudio pyaudio')
    exit(1)


ERROR_HANDLER_FUNC = CFUNCTYPE(None)


def py_error_handler():
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


CHUNK = 1024
AUDIO_FORMAT = pyaudio.paInt16
STEREO = 2
MONO = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILE = 'temp.wav'


class SmAudio:

    def __init__(
            self,
            audio_format=AUDIO_FORMAT,
            chunk=CHUNK,
            rate=RATE,
            record_seconds=RECORD_SECONDS,
            channels=MONO
    ):
        self.audio_format = audio_format
        self.chunk = chunk
        self.rate = rate
        self.record_seconds = record_seconds
        self.channels = channels
        self.audio = None
        self.stream = None
        self.path = os.path.dirname(os.path.abspath(__file__))
        self._temp_path = os.path.join(self.path, 'temp')
        self._temp_file = os.path.join(self._temp_path, WAVE_OUTPUT_FILE)

    def __enter__(self):
        with noalsaerr():
            self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.audio_format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def record(self):
        print('Recording...')
        frames = list()
        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            frames.append(self.stream.read(self.chunk))
        self._save_into_file(frames)
        print('Finished')

    def _save_into_file(self, frames):
        import wave

        self._create_temp_folder()

        f = wave.open(self._temp_file, 'wb')
        f.setnchannels(self.channels)
        f.setsampwidth(self.audio.get_sample_size(self.audio_format))
        f.setframerate(self.rate)
        f.writeframes(b''.join(frames))
        f.close()

    def _create_temp_folder(self):
        if not os.path.exists(self._temp_path):
            os.mkdir(self._temp_path)

    def remove_temp_file(self):
        os.remove(self._temp_file)
