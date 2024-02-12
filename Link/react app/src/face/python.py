from flask import Flask,request,jsonify,render_template
from flask_cors import CORS
from PIL import Image
import cv2
import numpy as np
import requests
import json # import os module

app = Flask(__name__)
CORS(app)
video_capture = None
#@app.route('/data', methods=['GET'])
@app.route('/capture', methods=['POST'])

# define the application factory function
def create_app():
    # create the flask app object
    print("hello world")
    userName = "John Doe"

    activate = request.data.decode('utf-8')
    activate = json.loads(activate)
    activate = activate.get('activate')
    print(activate)
    if (activate == 'activate'):
             global video_capture
             video_capture = cv2.VideoCapture(0)
             while video_capture.isOpened():
                     ret, frame = video_capture.read()
                 #standered is 480*640 so we slice index it to 250*250 and : get all channels
                     frame = frame[120:120+250,200:200+250, :]
                    
                     cv2.imshow('Verification', frame)

                        
                         # Verification trigger
                     if cv2.waitKey(10) & 0xFF == ord('v'):
                             # Save input image to application_data/input_image folder
                             frame = frame
                             # Convert to grayscale
                             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                             # Load the face cascade classifier
                             face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

                             # Detect faces in the image
                             faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                             if len(faces) != 0 :
                                  # Save images with detected faces
                                 #for i, (x, y, w, h) in enumerate(faces):
                                     # Draw a rectangle around the detected face
    #                             #   cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #                                 # crop face region 
    #                             #  face = frame[y:y+h, x:x+w]
    #                                 # Resize the face to 105x105 pixels
    #                             # resized_face = cv2.resize(face, (105, 105))
                                  video_capture.release()
                                  cv2.destroyAllWindows()
                                  return 'true'
                             else:
                              return 'false' 
                             
                                
                     if cv2.waitKey(10) & 0xFF == ord('q'):
                      break

# run the app as usual
if __name__ == "_main_":
   app.run()