import requests
import json
from PXDetector import PXDetector

motion_url = 'http://localhost:5000/detect_motion'
frame_url = 'http://localhost:5000/get_still'

#Detect motion for 30s:
payload = {'timeout':30,}
r=requests.post(motion_url,json=payload).json()
print(r) 

#Grab still image:
r=requests.post(frame_url) #Returns image as part of response.
with open("test.jpg","wb") as f:
	f.write(r.content)
	f.close()
