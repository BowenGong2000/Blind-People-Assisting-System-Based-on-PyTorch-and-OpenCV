import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
from flask import Flask, Response
from flask import request


import io
from PIL import Image



# app = Flask(__name__)
# @app.route("/")
# def hello_world():
#     return "<p>Hello, test!</p>"



# def gather_img():
#     while True:
#         time.sleep(0.2)
#         img = np.random.randint(0, 255, size=(128, 128, 3), dtype=np.uint8)
#         _, frame = cv2.imencode('.jpg', img)
#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
# @app.route("/mjpeg")
# def mjpeg():
#     return Response(gather_img(), mimetype='multipart/x-mixed-replace; boundary=frame')



app = Flask(__name__)
@app.route("/")
def hello_world():
    return """
    <body style="background: black;">
        <div style="width: 240px; margin: 0px auto;">
            <img src="/mjpeg" />
        </div>
    </body>
    """
output = None


# setup camera and resolution

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

output = None

def get_frame():
    _, img = cam.read()
    _, frame = cv2.imencode('.jpg', img)
    global output
    output = frame



def gather_img():
    while True:
        time.sleep(0.1)
        # _, img = cam.read()
        # _, frame = cv2.imencode('.jpg', img)
        get_frame()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + output.tobytes() + b'\r\n')


@app.route("/mjpeg")
def mjpeg():
    return Response(gather_img(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/recieve_mjpeg",methods=['GET','POST'])
def recieve_mjpeg():
    # if request.methods == 'POST':
    print("hello")
    # print(request.data)
    # print(request.args)
    data= request.args
    print(np.array(data['color_frame']))

    im = Image.frombuffer("I;16", (5, 10), data['color_frame'], "raw", "I;12")
    im.save('hello.png')

    # print(request.form)
    # print(request.files)
    # print(request.values)
    # print(request.json)

        


app.run(host='0.0.0.0', threaded=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

# http://127.0.0.1:5000/