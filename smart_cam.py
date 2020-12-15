import threading
from flask import Flask, render_template, Response,request
import cv2
import os
import argparse
import cv2
import numpy as np
import sys
import time
from threading import Thread

app = Flask(__name__)


os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

class Camera(object):
    def __init__(self,camera_link):
        self.video = cv2.VideoCapture(camera_link )
        (self.grabbed, self.frame) = self.video.read()
        Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
 
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


# for local webcam use 
def gen_frames(camera_link):  # generate frame by frame from camera
    camera=camera_link
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video')
def video_feed():
    try:
        camera_url = request.args.get("q")
        #Video streaming route. Put this in the src attribute of an img tag
        return Response(gen_frames(Camera(camera_url)), mimetype='multipart/x-mixed-replace; boundary=frame')
    except:  # This is bad! replace it with proper handling
        pass

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)