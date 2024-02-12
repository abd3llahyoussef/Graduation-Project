from flask import Flask,request
from flask_cors import CORS
import cv2
import numpy as np
import base64 # import os module
#import psycopg2
from PIL import Image
import mysql.connector
import base64
from io import BytesIO
from tensorflow import keras
from keras import layers,Model
import tensorflow as tf
import os

app = Flask(__name__)
CORS(app)


# def create_connection():
#     # Connect to the MySQL database
#     # Pass your database name, username, password,
#     # hostname, and port number
#     conn = mysql.connector.connect(
#         database='GraduationProject',
#         user='admin',
#         password='mo3badah2023',
#         host='my-nodejs-database-instance-1.c1dsu1fi8pdh.us-east-1.rds.amazonaws.com',
#         port='3306'
#     )
#     # Get the cursor object from the connection object
#     curr = conn.cursor()
#     return conn, curr

def create_connection():
    # Connect to the MySQL database
    # Pass your database name, username, password,
    # hostname, and port number
    conn = mysql.connector.connect(
         database='GraduationProject',
         user='admin',
         password='mo3badah2023',
         host='my-nodejs-database-instance-1.c1dsu1fi8pdh.us-east-1.rds.amazonaws.com',
         port='3306'
    )
    # Get the cursor object from the connection object
    curr = conn.cursor()
    return conn, curr

def read_img(bio_id):
    try:
        conn, cursor = create_connection()
        try:
            query = "SELECT face FROM biometrics WHERE bio_id=%s"
            cursor.execute(query, (bio_id,))
            res = cursor.fetchone()[0]
            # decode image and convert it to jpg extension
            print(res)
            missing_padding = 4 - len(res) % 4
            if missing_padding:
                res += b'=' * missing_padding # add padding
                decoded = base64.b64decode(res)
                print(decoded)
            photo_image = Image.open(BytesIO(decoded))
            rgb_image = photo_image.convert("RGB")
            print(rgb_image)
            f = BytesIO()
            rgb_image.save(f,format='JPEG')
            f.seek(0)
            image_jpg = Image.open(f)
            final_image = np.array(image_jpg)
            print(final_image)
            conn.commit()
            return final_image
        except (Exception, mysql.connector.Error) as error:
            print("Error while selecting data from biometrics table:", error)
        finally:
            # Close the cursor and connection objects
            cursor.close()
            conn.close()
    finally:
        # Since we do not have to do anything here, we will pass
        pass

def read_img_rasp(image):
    photo_image = Image.open(BytesIO(image))
    rgb_image = photo_image.convert("RGB")
    print(rgb_image)
    f = BytesIO()
    rgb_image.save(f,format='JPEG')
    f.seek(0)
    image_jpg = Image.open(f)
    final_image = np.array(image_jpg)
    print(final_image)
    return final_image

#build a distance layer
# Siamese L1 Distance class
class L1Dist(layers.Layer):
    
    # Init method - inheritance #self to operate on itself 
    # # **kwargs to use this as a part of bigger model(exporting & importing & specific key word)
    def __init__(self, **kwargs):
        super().__init__()
       
    ###### Magic happens here - similarity calculation
    def call(self, input_embedding, validation_embedding):
        return tf.math.abs(input_embedding - validation_embedding)
    
 # Reload model 
siamese_model = tf.keras.models.load_model('siamesemodelv2 END new v37 enhancment with 4000 colored.h5', custom_objects={'L1Dist':L1Dist})
   
####### Model Route
@app.route('/receive_frame',methods=['POST'])
# define the application factory function
def create_app():
        # create the flask app object
   # Get the image data from the request
    image_data = request.data
    # Build results array
    results = []
    input = read_img(8)
    validation_img = read_img_rasp(image_data)
    print(input) 
    print(validation_img)   
        # Make Predictions (put arrays in another sets of array)
    result = siamese_model.predict(list(np.expand_dims([input, validation_img], axis=1)))
    results.append(result)
    
    # Detection Threshold: Metric above which a prediciton is considered positive (50%=1)
    #sum all the examples that pass detection_threshold
    detection = np.sum(np.array(results) > 0.53)
    
    # Verification Threshold: Proportion of positive predictions / total positive samples 
    verification = detection / 1
    verified = verification > 0.8
    print(verified)
    print(results)
    return results, verified




def write_image(bio_id, file_path):
    try:
        
        # Read database configuration
        conn, cursor = create_connection()
        try:
            # Execute the INSERT statement
            # Convert the image data to base64 encoding
            cursor.execute("INSERT INTO biometrics (bio_id, face) VALUES (%s, %s)",
                           (bio_id, file_path))
            # Commit the changes to the database
            conn.commit()
        except (Exception, mysql.connector.Error) as error:
            print("Error while inserting data in biometrics table:", error)
        finally:
            # Close the cursor and connection objects
            cursor.close()
            conn.close()
    finally:
        # Since we do not have to do anything here, we will pass
        pass


####### APP Route
@app.route('/capture', methods=['POST'])

# define the application factory function
def create_app():
    # create the flask app object
   # Get the image data from the request
    image_data = request.json
    image_data = image_data.get('dataURL')
    # Remove the prefix and decode the base64 data
    # Decode the base64 image data and convert it to OpenCV format
    _, encoded_image = image_data.split(",", 1)
    decoded_image = cv2.imdecode(np.frombuffer(base64.b64decode(encoded_image), np.uint8), -1)
    ####### Viola-Jones Algorithm to detect face 
    gray = cv2.cvtColor(decoded_image, cv2.COLOR_BGR2GRAY)
            # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) != 0 :
        for i, (x, y, w, h) in enumerate(faces):
                # Draw a rectangle around the detected face
            cv2.rectangle(decoded_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # crop face region 
            face = decoded_image[y:y+h, x:x+w]
                # Resize the face to 105x105 pixels
            resized_face = cv2.resize(face, (105, 105))
            print(resized_face)
        # Convert the image to JPEG format
            _, buffer = cv2.imencode(".jpg", resized_face)
            # Convert the image buffer to base64 string
            base64_data = base64.b64encode(buffer).decode("utf-8")
            ############# brightness algorithm
            img = Image.fromarray(gray)
            # Get the mean brightness value
            brightness = int(round(img.getextrema()[0] + img.getextrema()[1])/2)
            print("Brightness: ", brightness)
            #write_image("10f16905-5d78-46d0-86c4-f4f0c25263ec",resized_face)
            write_image(9,base64_data)
            return {'isFace':'true','Brightness':brightness}
    else:
            return {'isFace':'false'}



####### fromRasToDB Route
@app.route('/receive_frame_ras', methods=['POST'])

# define the application factory function
def create_app():
        # create the flask app object
   # Get the image data from the request
    image_data = request.data
    # Remove the prefix and decode the base64 data
    # Decode the base64 image data and convert it to OpenCV format
    decoded_image = cv2.imdecode(np.frombuffer(base64.b64decode(image_data), np.uint8), -1)

    if(write_image("10f16905-5d78-46d0-86c4-f4f0c25263ec",decoded_image) == "saved"):
        return "saved"
    else :
        return "Not saved"
# run the app as usual
if __name__ == "_main_":
   app.run()
