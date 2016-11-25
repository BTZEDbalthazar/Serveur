#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import StringIO
import wave
import time
import angus
import pyaudio

CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 2

import  tornado.httpclient
import urllib
http_client = tornado.httpclient.HTTPClient()


def post():
    post_data = { 'data': 'test data' } #A dictionary of your post data
    body = urllib.urlencode(post_data) #Make it into a post request
    http_client.fetch("http://localhost:8889/data/", method='POST', headers=None, body=body)
    print "ok"

def decode_output(sound, filename):
	sound = base64.b64decode(sound)
	sound = zlib.decompress(sound)
	with open(filename, "wb") as f:
	    f.write(sound)

### Index will differ depending on your system
INDEX = 5  # USB Cam


p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
#for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
for i in range (0,numdevices):
    if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
        print "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')        
    if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
        print "Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')
        devinfo = p.get_device_info_by_index(1)
        INDEX=i
print "Selected device is ",devinfo.get('name')

conn = angus.connect()
service = conn.services.get_service('sound_detection', version=1)
service.enable_session()
stream_queue = Queue.Queue()

def callback(in_data, frame_count, time_info, status):
    stream_queue.put(in_data)
    return (in_data, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=INDEX,
                stream_callback=callback)


stream.start_stream()

while(True):

    nb_buffer_available = stream_queue.qsize()
    if nb_buffer_available > 0:
        print "nb buffer available" + str(nb_buffer_available)
        
    if nb_buffer_available == 0:
        time.sleep(0.01)
        continue

    data = stream_queue.get()

    buff = StringIO.StringIO()

    wf = wave.open(buff, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

    job = service.process(
        {'sound': StringIO.StringIO(buff.getvalue()), 'sensitivity': 0.7})
    if job.result["nb_events"]>0: 
	 print job.result
	 post()


stream.stop_stream()
stream.close()
p.terminate()
