import cv2,random
videolist = ["TAGHeuer.avi","TAGHeuer2.avi","TAGHeuer3.avi"]
def playfile(filename):  
    video = cv2.VideoCapture(filename)
    print "Could not open video file"
    while True:
        ret, frame = video.read()
        if ret == True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break

    video.release()
    cv2.destroyAllWindows()

def play():
     i= random.randint(0,len(videolist)-1)

     f=videolist[i]
     print f
     playfile(f)

play()