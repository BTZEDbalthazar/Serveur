#!/bin/python
# -*- coding: utf-8 -*-

'''
Faire un programme qui se connecte à la web-camera, envoie les images sur angus.ai et affiche une publicité homme /ou/ femme selon le sexe de la personne qui se présente devant la caméra.

Site développeur angus.ai: http://angus-doc.readthedocs.io/en/latest/

'''
#!/usr/bin/env python
import StringIO
import angus
import numpy as np
import cv2
import Queue
import StringIO
import wave
import time
import  tornado.httpclient
import urllib
http_client = tornado.httpclient.HTTPClient()

def handle_request():
	pass
def post(gender):
        
	post_data = { 'react': gender } #A dictionary of your post data
	body = urllib.urlencode(post_data) #Make it into a post request
	http_client.fetch("http://localhost:8889/data/", method='POST', headers=None, body=body)
      
if __name__ == '__main__':    
    ### Web cam index might be different from 0 on your setup.
    stream_index = 0 
    cap = cv2.VideoCapture(stream_index)
    
    ### Index will differ depending on your system
    INDEX = 4  # USB Cam

    if not cap.isOpened():
        print "Cannot open stream of index " + str(stream_index)
        exit(1)

    print "Video stream is of resolution " + str(cap.get(3)) + " x " + str(cap.get(4))

    conn = angus.connect()
    service = conn.services.get_service("age_and_gender_estimation", version=1)
    service.enable_session()
	
    """    
    p = pyaudio.PyAudio()
    streamaudio = p.open(format=FORMAT,
         channels=CHANNELS,
         rate=RATE,
         input=True,
         frames_per_buffer=CHUNK,
         input_device_index=INDEX,
         stream_callback=callback)
   

    conn1 = angus.connect()
    service1 = conn.services.get_service('sound_detection', version=1)
    service1.enable_session()
    stream_queue = Queue.Queue()
    
    streamaudio.start_stream()      
    """
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not frame == None:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret, buff = cv2.imencode(".png", gray)
		buff = StringIO.StringIO(np.array(buff).tostring())

		job = service.process({"image": buff})
		res = job.result

		if res['nb_faces'] > 0:           
			for i in range(0,res['nb_faces']):
			    roi = res['faces'][i]['roi']
			    cv2.rectangle(frame, (int(roi[0]), int(roi[1])), 
						 (int(roi[0] + roi[2]), int(roi[1] + roi[3])), 
						 (0,255,0))
			    age = res['faces'][i]['age']
			    gender = res['faces'][i]['gender']
			    cv2.putText(frame, "(age, gender) = (" + '%.1f'%age + ", " + str(gender) + ")", 
					(int(roi[0]), int(roi[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255))

			    post(gender)
			    """            	                     
			    if gender == "male":
			    	img = cv2.imread("homme.jpg",0)
				cv2.imshow("pub",img )                      
			    elif gender == "female":       
				img1 = cv2.imread("femme.jpg",0)
				cv2.imshow("pub",img1 )
			    """       
		cv2.imshow('Original', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
		   break
                 

    service.disable_session()

    cap.release()
    cv2.destroyAllWindows()

  
