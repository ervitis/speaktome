#!/usr/bin/env python
# -*- coding: utf-8 -*-


from speaktome.stm_listener import SmAudio


def capture_signal():
    import signal
    signal.signal(signal.SIGINT, signal_handler)


def signal_handler(signal, frame):
    print('App stopped')
    exit(0)


def main():
    listener = SmAudio()

    with listener as source:
        source.record()


if __name__ == '__main__':
    capture_signal()
    main()
