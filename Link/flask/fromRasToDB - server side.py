from flask import Flask,request
from flask_cors import CORS
import cv2
import numpy as np
import base64 # import os module
#import psycopg2
from PIL import Image
import mysql.connector
import base64

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

            cursor.execute("INSERT INTO biometric_data (clientId, face) VALUES (%s, %s)",
                           (bio_id, file_path))
            # Commit the changes to the database
            conn.commit()
            return "saved"
        except (Exception, mysql.connector.Error) as error:
            print("Error while inserting data in biometrics table:", error)
            return "Not saved"
        finally:
            # Close the cursor and connection objects
            cursor.close()
            conn.close()
    finally:
        # Since we do not have to do anything here, we will pass
        pass
####### APP Route
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
