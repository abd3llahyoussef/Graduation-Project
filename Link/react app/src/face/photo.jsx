import React from "react";
import axios from "axios";

export default function Data() {
  const openCam = () => {
    const video = document.getElementById("video");
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then((stream) => {
          video.srcObject = stream;
          video.play();
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      alert("Your Device Dose Not Have A Cam");
    }
  };
  const captuerPhoto = async (e) => {
    e.preventDefault();
    const video = document.getElementById("video");
    const capture = document.getElementById("canvas");
    const ctx = capture.getContext("2d");
    ctx.drawImage(video, 0, 0, 200, 200);
    const dataURL = capture.toDataURL("image/jpeg");
    console.log(dataURL);
    const msg = await axios.post("http://40.115.44.233:80/capture", {
      dataURL: dataURL,
    });
    console.log(msg);
    alert(msg.data.isFace);
    if (msg.data.Brightness < 124) {
      alert("Low Brightness");
    }
    // // get the button element
    // const save = document.getElementById("save");

    // // add a click event listener
    // save.addEventListener("click", function () {
    //   // get the image data as a base64 encoded string
    //   const imageData = dataURL;

    //   // create a download link
    //   const link = document.createElement("a");
    //   link.href = imageData;
    //   link.download = "canvas.jpg";

    //   // append the link to the document body
    //   document.body.appendChild(link);

    //   // click the link
    //   link.click();

    //   // remove the link from the document body
    //   document.body.removeChild(link);
  };
  // const send = async () => {
  //   try {
  //     console.log(photo);
  //     await axios.post(
  //       "http://localhost:5000/add",
  //       { image: photo },
  //       { headers: { "Content-Type": "application/json" } }
  //     );
  //   } catch (err) {
  //     console.log(err);
  //   }
  // };
  // const handleCapture = async () => {
  //   try {
  //     const msg = await axios.post("http://localhost:5000/capture", {
  //       activate: "activate",
  //     });
  //     console.log(msg.data);
  //     alert(msg.data);
  //     console.log("Image captured successfully!");
  //   } catch (error) {
  //     console.error("Failed to capture image:", error);
  //   }
  // };
  return (
    <div>
      {/* <div>
        <button className="btn" onClick={handleCapture}>
          Capture Image
        </button>
      </div> */}
      <h3>Take Photo</h3>
      <div className="photo-btn">
        <button onClick={openCam} className="btn">
          <span>Open Cam</span>
        </button>
        <button onClick={captuerPhoto} className="btn">
          <span>Take Photo</span>
        </button>
      </div>
      <video id="video"></video>
      <div id="pic">
        <canvas id="canvas"></canvas>
      </div>
    </div>
  );
}
