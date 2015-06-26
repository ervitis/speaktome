#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pyaudio
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


ROOT = 'voxforge-es-0.2'
LM = ROOT + '/etc/voxforge_es_sphinx.transcription.test.lm'
DIC = ROOT + '/etc/voxforge_es_sphinx.dic'
HMM = ROOT + '/model_parameters/voxforge_es_sphinx.cd_ptm_3000/'


def main():
    abspath = os.path.dirname(os.path.abspath(__file__))
    abspath = os.path.join(abspath, '..')

    model_dir = os.path.join(abspath, 'model')

    hmm = os.path.join(model_dir, HMM)
    print(hmm)
    lm = os.path.join(model_dir, LM)
    print(lm)
    dic = os.path.join(model_dir, DIC)
    print(dic)

    config = Decoder.default_config()
    config.set_string('-hmm', hmm)
    config.set_string('-lm', lm)
    config.set_string('-dict', dic)
    decoder = Decoder(config)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    in_speech_bf = True
    decoder.start_utt()
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
            try:
                if decoder.hyp().hypstr != '':
                    print('Partial decoding result:', decoder.hyp().hypstr)
            except AttributeError:
                pass
            if decoder.get_in_speech():
                sys.stdout.write('.')
                sys.stdout.flush()
            if decoder.get_in_speech() != in_speech_bf:
                in_speech_bf = decoder.get_in_speech()
                if not in_speech_bf:
                    decoder.end_utt()
                    try:
                        if decoder.hyp().hypstr != '':
                            print('Stream decoding result:', decoder.hyp().hypstr)
                    except AttributeError:
                        pass
                    decoder.start_utt()
        else:
            break
    decoder.end_utt()
    print('An Error occured:', decoder.hyp().hypstr)


if __name__ == '__main__':
    main()
