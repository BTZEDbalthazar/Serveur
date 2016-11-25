import tornado.ioloop
import tornado.web
import logging
import time
import cv2
# import video
import StringIO
import wave
import time
import angus
import base64
import zlib
import subprocess
import os

def decode_output(sound, filename):
	sound = base64.b64decode(sound)
	sound = zlib.decompress(sound)
	with open(filename, "wb") as f:
	    f.write(sound)


conn = angus.connect()
service = conn.services.get_service('text_to_speech', version=1)



class MainHandler(tornado.web.RequestHandler):

	# self.last_react=0
	# self.last_voice=0
	# self.gender=""
	def initialize(self, database):
		self.database = database

	def post(self):
		r= self.request.body
		
		req, value= r.split("=")
		if req == "react":
			self.database["last_react"]=time.time()
			self.database["gender"]=value
		else:
			self.database["last_voice"]=time.time()
		
		diff = self.database["last_react"] - self.database["last_voice"]
		diff=abs(diff)
		# print  "last_react", self.database["last_react"]
		# print  "last_voice", self.database["last_voice"]
		# print diff
		# print req
		if diff < 10 and self.database["last_voice"] != 0 and self.database["last_react"] != 0:
			t= time.time()
			timediff= t - self.database["timeout"]
			# print "timediff",timediff 
			if timediff < 5 :
				 return
		    
			
			self.database["timeout"]=t 
			print "SYNC",self.database["gender"]                                      
			if self.database["gender"] == "male":
				img = cv2.imread("homme.jpg",0)
				cv2.imshow("pub",img )  
				phrase= "Hi man, Look at this beautiful watch!! I'm sure it look very good on you! You have to buy it!"				               
			elif self.database["gender"] == "female":       
				img1 = cv2.imread("femme.jpg",0)
				cv2.imshow("pub",img1 )
				phrase= "Hi girl, Look at this beautiful watch!! I'm sure it look very good on you! You have to buy it!"
			cv2.waitKey(1)
		
			if self.database["lastgender"] != self.database["gender"] :
				job = service.process({'text': phrase, 'lang' : "en-US"})
				decode_output(job.result["sound"], "output.wav")
				subprocess.Popen(["/usr/bin/aplay","./output.wav"])
				# video.play()
				subprocess.Popen(["python", "video.py"])
				# os.system("python video.py")
			self.database["lastgender"]= self.database["gender"]


mydatabase = dict()
mydatabase["last_react"]=0
mydatabase["last_voice"]=0
mydatabase["gender"]=""
mydatabase["timeout"]=0
mydatabase["lastgender"]=""
def make_app():
    return tornado.web.Application(
	[(r"/data/", MainHandler, dict(database=mydatabase) )]
	)

if __name__ == "__main__":
	
    logging.basicConfig()	
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()

