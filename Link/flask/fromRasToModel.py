from flask import Flask,request,Response
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import requests
import base64
from io import BytesIO
import numpy as np

app = Flask(__name__)
CORS(app)

#### viola algorithm
def preprocess(image):
        # Convert to grayscale
          gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load the face cascade classifier
          face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Detect faces in the image
          faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Save images with detected faces
          for i, (x, y, w, h) in enumerate(faces):
            # Draw a rectangle around the detected face
            rect = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # crop face region 
            face = image[y:y+h, x:x+w]
            # Resize the face to 105x105 pixels
            resized_face = cv2.resize(face, (105, 105))
          
            return resized_face     
                
####### APP Route
url = 'http://localhost:6000/receive_frame'

cap = cv2.VideoCapture(0)
# define the application factory function
def create_app():

    while cap.isOpened():
        ret, frame = cap.read()
        #standered is 480*640 so we slice index it to 250*250 and : get all channels
        frame = frame[120:120+250,200:200+250, :]
        
        cv2.imshow('Verification', frame)
    
        # Verification trigger
        if cv2.waitKey(10) & 0xFF == ord('v'):
            # Save input image to application_data/input_image folder
            frame = preprocess(frame)
            ret,buffer = cv2.imencode('.jpg',frame)
            frame = np.array(buffer).tobytes()
            print(frame)

            try:
                response = requests.post(url,data = frame , headers = {'content-Type':'image/jpeg'})
                print("Response:",response.text )
            except requests.exceptions.RequestException as e:
                print("Failed")
    #     if cv2.waitKey(10) & 0xFF == ord('q'):
    #         break
    # cap.release()
    # cv2.destroyAllWindows()
        # Yield the frame as a response to the client
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return "Video Streaming Server"


@app.route('/video_feed')
def video_feed():
    return Response(create_app(),mimetype = 'multipart/x-mixed-replace;boundary=frame')
# run the app as usual
if __name__ == "_main_":
   #app.debug = True
   app.run(host="0.0.0.0",host=7000)