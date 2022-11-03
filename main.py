import os
from turtle import color
import matplotlib
from Realsense.realsense_depth import *
from Realsense.realsense import *
from Algorithm.main import *
import cv2
import time
import argparse
import requests


import sys
from PIL import Image
from io import BytesIO

matplotlib.use('TKAgg')
# Disable tensorflow output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

#def send_data(color_frame):


    #img = Image.fromarray(np.uint8(color_frame)).convert('RGB')
    #byte_io = BytesIO()
    #img.save(byte_io, 'png')
    #byte_io.seek(0)
    #requests.post('http://localhost:5000/recieve_mjpeg',params={'color_frame':byte_io})



def main(_argv):
    parser = argparse.ArgumentParser()
    # Initialize Camera Intel Realsense
    dc = DepthCamera()

    Debug_flag = 1

    # Parse arguments
    cv2.namedWindow("Video")
    cv2.namedWindow("Video_Depth")

    # Load saved CV model
    model = get_model()

    # Initialize Algorithm
    oldCords = None
    depth = None

    while True:
        # Start Video Capture
        ret, depth_frame, color_frame = dc.get_frame()

        # If frame is not empty
        if ret:
            #cv2.imshow("Video", color_frame)
           # cv2.imshow("Video_Depth", depth_frame)
            #send_data(color_frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

            # Get coordinates from color frame
            coordinates = get_coordinates(color_frame, model)

    
            if coordinates != None:
                start_point = (coordinates[0], coordinates[1])
  

                end_point = (coordinates[2], coordinates[3])
                color = (255, 0, 0)
                thickness = 2
                color_frame = cv2.rectangle(color_frame, start_point, end_point, color, thickness)
                #color_frame = cv2.circle(color_frame, (coordinates[0],coordinates[1]), radius=20, color=(0, 0, 255), thickness=-1)
                #color_frame = cv2.circle(color_frame, (coordinates[2],coordinates[3]), radius=20, color=(0, 0, 255), thickness=-1)

            cv2.imshow("Video", color_frame)
            cv2.imshow("Video_Depth", depth_frame)

            if coordinates != None:
                # Get Median Depth from depth frame
                depth = process_frame(
                    depth_frame, coordinates[0], coordinates[1], coordinates[2], coordinates[3])

                # Debug mode
                if Debug_flag == 1:
                    print(coordinates)
                    #print(coordinates)
                    print(depth)


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])