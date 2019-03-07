import cv2
import imutils
import datetime
import requests
from requests.auth import HTTPDigestAuth
import time
import numpy as np


class PXDetector():

    def __init__(self,
        still = 'ISAPI/Streaming/Channels/101/picture',
        video = 'Streaming/Channels/101',
        host='10.0.1.51',
        usr='admin',
        pwd='Code-Modules'
        ):

        self.usr=usr
        self.pwd=pwd
        self.still_url = 'http://' + host + '/' + still
        self.video_url =  'rstp://'+usr+':'+pwd+'@'+host+'/'+video
        

    def get_still(self):
        rsp=requests.get(self.still_url, auth=HTTPDigestAuth(self.usr, self.pwd))
        return rsp.content

    def get_frame(self):
        #Grab a still frame
        frame = self.get_still()
        frame = np.asarray(bytearray(frame), dtype="uint8")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        return frame

    def detect_motion(self, timeout=60,return_frame=False):
        startTime=time.time()
        avg = None

        while time.time()-startTime < timeout:
            #Grab frame:
            frame=self.get_frame()
            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)         
            # if the first frame is None, initialize it
            if avg is None:
                avg = gray.copy().astype("float")
                continue
            # compute the absolute difference between the current frame and
            # first frame
            cv2.accumulateWeighted(gray, avg, 0.5)
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
            thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]         
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            # loop over the contours
            detection=False
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < 500:
                    continue
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                detection = True
                now = datetime.datetime.now()
                cv2.imwrite('motion_latest.jpg',frame)
            
            if detection:
                return now

        return None