from flask import Flask, request, send_file
from PIL import Image
import cv2
import numpy as np
import io

app = Flask(_name_)

# load the face cascade classifier
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# handle file upload
@app.route("/upload", methods=["POST"])
def upload():
    # get the image from the request
    image = request.files["image"]

    # convert the image to a numpy array
    image = np.array(Image.open(image))

    # convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # detect faces using the cascade classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # convert the image back to PIL format
    image = Image.fromarray(image)

    # save the image to a buffer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")

    # return the image as a response
    return send_file(buffer, mimetype="image/jpeg")

if _name_ == "_main_":
    app.run(debug=True)