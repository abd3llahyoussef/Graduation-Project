from flask import Flask,request
from flask_cors import CORS
import cv2
import numpy as np
import base64 # import os module
#import psycopg2
from PIL import Image
import mysql.connector
import base64
import json

app = Flask(__name__)
CORS(app)

# import psycopg2
# import base64
# from PIL import Image,ImageFile
# from io import BytesIO
# def create_connection():
#     # Connect to the database
#     # using the psycopg2 adapter.
#     # Pass your database name ,# username , password , 
#     # hostname and port number
#     conn = psycopg2.connect(dbname='recog',
#                             user='postgres',
#                             password='postgres',
#                             host='localhost',
#                             port='5432')
#     # Get the cursor object from the connection object
#     curr = conn.cursor()
#     return conn, curr
# def write_image(bio_id,file_path):
#     try:
#         # Read database configuration
#         conn, cursor = create_connection()
#         try:           
#             # Execute the INSERT statement
#             # Convert the image data to Binary
#             cursor.execute("INSERT INTO biometrics\
#             (bio_id,face) " +
#                     "VALUES(%s,%s)",
#                     (bio_id,psycopg2.Binary(drawing),))
#             #print(psycopg2.Binary(drawing))
#             # Commit the changes to the database
#             conn.commit()
#         except (Exception, psycopg2.DatabaseError) as error:
#             print("Error while inserting data in biometrics table", error)
#         finally:
#             # Close the connection object
#             conn.close()
#     finally:
#         # Since we do not have to do
#         # anything here we will pass
#         pass
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
        database='biometric',
        user='root',
        password='root',
        host='localhost',
        port='3306'
    )
    # Get the cursor object from the connection object
    curr = conn.cursor()
    return conn, curr

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


# run the app as usual
if __name__ == "_main_":
   app.run()